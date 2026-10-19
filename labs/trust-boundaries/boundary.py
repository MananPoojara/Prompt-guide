"""A local in-memory allowlist demo. No network, writes, authentication, or sandbox."""

import json, re

DOCUMENTS = {
    "decision": {
        "namespace": "team-a",
        "authority": "approved-decision",
        "text": "Approved workshop decision: start time is 14:00. Capacity is 20.",
    },
    "attachment": {
        "namespace": "team-a",
        "authority": "untrusted-attachment",
        "text": "See the supplied attachment text.",
    },
    "private-plan": {
        "namespace": "team-b",
        "authority": "approved-decision",
        "text": "Fictional private marker: DUMMY-TEAM-B-RECORD. Start time is 09:00.",
    },
}


def parse(raw):
    if not isinstance(raw, str) or len(raw) > 10000:
        raise ValueError("Invalid response size")

    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("Duplicate JSON key")
            obj[key] = value
        return obj

    return json.loads(raw, object_pairs_hook=unique)


class Host:
    def __init__(self):
        # Application-selected scope, never read from model arguments or source text.
        self.namespace = "team-a"
        self.available = {"decision", "attachment"}

    def dispatch(self, proposal):
        reject = {"status": "rejected", "reason": "Action or arguments not permitted"}
        if not isinstance(proposal, dict):
            return reject
        action = proposal.get("action")
        if action == "read":
            if set(proposal) != {"action", "document_id"} or not isinstance(
                proposal["document_id"], str
            ):
                return reject
            doc = DOCUMENTS.get(proposal["document_id"])
            if doc is None or doc["namespace"] != self.namespace:
                return {"status": "denied", "reason": "Document unavailable"}
            self.available.add(proposal["document_id"])
            return {"status": "ok", "document": dict(doc)}
        if action == "final":
            if set(proposal) != {"action", "time", "document_id"}:
                return reject
            id = proposal["document_id"]
            time = proposal["time"]
            if (
                not isinstance(id, str)
                or not isinstance(time, str)
                or re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", time) is None
            ):
                return reject
            doc = DOCUMENTS.get(id)
            if (
                id not in self.available
                or doc is None
                or doc["namespace"] != self.namespace
                or doc["authority"] != "approved-decision"
            ):
                return reject
            return {"status": "accepted", "answer": {"time": time, "document_id": id}}
        return reject
