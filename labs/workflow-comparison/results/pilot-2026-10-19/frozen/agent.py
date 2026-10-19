"""Small read-only tool dispatcher. Model output is untrusted input."""

import re


def initial(limit):
    return {"limit": limit, "calls": 0, "read": [], "history": [], "done": False}


def act(state, decision, docs):
    if not isinstance(decision, dict) or not isinstance(decision.get("action"), str):
        return {"error": "Expected an action object"}
    action = decision["action"]
    fields = {
        "search": {"action", "query"},
        "read": {"action", "id"},
        "final": {"action", "answers"},
    }
    if action not in fields or set(decision) != fields[action]:
        return {"error": "Unknown action or invalid arguments"}
    if action == "search":
        query = decision["query"]
        if not isinstance(query, str) or not query.strip() or len(query) > 500:
            return {"error": "Invalid query"}
        words = set(re.findall(r"\w+", query.lower()))
        ranked = sorted(
            docs,
            key=lambda d: (-sum(d["text"].lower().count(w) for w in words), d["id"]),
        )
        return {
            "documents": [{k: v for k, v in d.items() if k != "text"} for d in ranked]
        }
    if action == "read":
        if not isinstance(decision["id"], str):
            return {"error": "Invalid document id"}
        doc = next((d for d in docs if d["id"] == decision["id"]), None)
        if doc is None:
            return {"error": "Unknown document id"}
        if doc["id"] not in state["read"]:
            state["read"].append(doc["id"])
        return {"document": doc}
    answers = decision["answers"]
    if not isinstance(answers, list) or not answers:
        return {"error": "Expected answers array"}
    for answer in answers:
        if not isinstance(answer, dict) or set(answer) != {
            "id",
            "answer",
            "status",
            "sources",
        }:
            return {"error": "Invalid answer shape"}
        sources = answer["sources"]
        if not isinstance(sources, list) or not all(
            isinstance(s, str) and s in state["read"] for s in sources
        ):
            return {"error": "Citations must refer to documents read in this run"}
    state["done"] = True
    return {"accepted": True, "answers": answers}
