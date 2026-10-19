"""Inspectable host decisions and descriptive accounting for three execution strategies."""

QUESTIONS = [
    {"id": "start", "question": "What is the approved club start time (HH:MM)?"},
    {
        "id": "capacity",
        "question": "What is the approved attendance capacity (string)?",
    },
    {"id": "registration", "question": "What registration details are approved?"},
]


def select_current(documents):
    return [document for document in documents if document["status"] == "current"]


def initial_payload(strategy, documents):
    if strategy not in ["single", "fixed"]:
        raise ValueError("Expected single or fixed")
    return {
        "questions": QUESTIONS,
        "documents": documents if strategy == "single" else select_current(documents),
    }


def summarize(calls):
    return {
        "calls": len(calls),
        "process_successes": sum(c["status"] == 0 for c in calls),
        "sum_call_seconds": round(sum(c["elapsed_seconds"] for c in calls), 3),
        "request_characters": sum(c["request_characters"] for c in calls),
    }
