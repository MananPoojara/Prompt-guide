"""Local teaching state machine; no model-visible approval or apply operation."""

import re
from gate import digest, sha, Rejected

BEFORE = "Start: 13:00\nCapacity: 20\n"
EXPECTED = "Start: 14:00\nCapacity: 20\n"


def initial():
    return dict(
        limit=6,
        calls=0,
        pending=False,
        phase="running",
        fault_used=False,
        read=[],
        history=[],
        before_sha256=sha(BEFORE.encode()),
        proposal=None,
        resolved_evidence=None,
    )


def recover(state):
    if state["pending"]:
        raise ValueError(
            "A reserved call has an uncertain outcome; inspect it, do not automatically retry"
        )
    if not 0 <= state["calls"] <= state["limit"] == 6:
        raise ValueError("Invalid call budget")
    return state


def reserve(state):
    recover(state)
    if state["phase"] != "running" or state["calls"] >= state["limit"]:
        raise ValueError("Run is stopped or budget exhausted")
    state["calls"] += 1
    state["pending"] = True


def dispatch(state, action, documents):
    invalid = dict(error="invalid_action", retryable=False)
    if state["phase"] != "running" or not isinstance(action, dict):
        return invalid
    kind = action.get("action")
    fields = {
        "search": {"action", "query"},
        "read": {"action", "id"},
        "propose": {"action", "target", "before_sha256", "content", "evidence"},
        "unresolved": {"action", "reason"},
    }
    if not isinstance(kind, str) or kind not in fields or set(action) != fields[kind]:
        return invalid
    allowed = [d for d in documents if d["scope"] == "team-a" and d["current"]]
    if kind == "search":
        if not isinstance(action["query"], str) or not 0 < len(action["query"]) <= 200:
            return invalid
        terms = set(re.findall(r"\w+", action["query"].lower()))
        ranked = sorted(
            allowed,
            key=lambda d: (
                -len(terms & set(re.findall(r"\w+", d["text"].lower()))),
                d["id"],
            ),
        )
        return dict(
            documents=[dict(id=d["id"], revision=d["revision"]) for d in ranked]
        )
    if kind == "read":
        doc = next((d for d in allowed if d["id"] == action["id"]), None)
        if doc is None:
            return dict(error="unavailable", retryable=False)
        if not state["fault_used"]:
            state["fault_used"] = True
            return dict(error="temporary_unavailable", retryable=True)
        if doc["id"] not in state["read"]:
            state["read"].append(doc["id"])
        return dict(document=doc)
    if kind == "unresolved":
        if (
            not isinstance(action["reason"], str)
            or not action["reason"].strip()
            or len(action["reason"]) > 1000
        ):
            return invalid
        state["phase"] = "unresolved"
        return dict(status="unresolved", reason=action["reason"])
    proposal = {k: action[k] for k in ("target", "before_sha256", "content")}
    try:
        digest(proposal)
    except Rejected:
        return invalid
    if proposal["before_sha256"] != state["before_sha256"]:
        return invalid
    evidence = action["evidence"]
    if (
        not isinstance(evidence, dict)
        or set(evidence) != {"document_id", "revision", "quote"}
        or not all(isinstance(v, str) for v in evidence.values())
    ):
        return invalid
    doc = next(
        (
            d
            for d in allowed
            if d["id"] == evidence["document_id"]
            and d["id"] in state["read"]
            and d["revision"] == evidence["revision"]
        ),
        None,
    )
    quote = evidence["quote"]
    if doc is None or not quote or doc["text"].count(quote) != 1:
        return dict(error="evidence_not_resolved", retryable=False)
    start = doc["text"].index(quote)
    state["resolved_evidence"] = dict(**evidence, start=start, end=start + len(quote))
    state["proposal"] = proposal
    state["phase"] = "awaiting_review"
    return dict(
        status="awaiting_review",
        proposal_digest=digest(proposal),
        resolved_evidence=state["resolved_evidence"],
    )
