"""Whole-chunk evidence packing and deliberately narrow reference checks."""


def pack(chunks, order, count_tokens, budget):
    if budget <= 0:
        raise ValueError("budget must be positive")
    selected = []
    packet = ""
    for i in order:
        chunk = chunks[i]
        candidate = "\n\n".join(f"[{c['id']}]\n{c['text']}" for c in selected + [chunk])
        if count_tokens(candidate) <= budget:
            selected.append(chunk)
            packet = candidate
    return selected, packet, count_tokens(packet)


def normalize(value):
    return " ".join(value.split()).casefold()


def grade(output, query, chunks):
    result = {
        "schema_valid": False,
        "answer_correct": False,
        "quote_in_selected_chunk": False,
        "reference_in_quote": False,
        "supported": False,
    }
    if not isinstance(output, dict) or set(output) != {
        "status",
        "answer",
        "chunk_id",
        "quote",
    }:
        return result
    if output["status"] == "insufficient_evidence":
        result["schema_valid"] = all(
            output[k] is None for k in ["answer", "chunk_id", "quote"]
        )
        return result
    if output["status"] != "answered" or not all(
        isinstance(output[k], str) and output[k].strip()
        for k in ["answer", "chunk_id", "quote"]
    ):
        return result
    result["schema_valid"] = True
    result["answer_correct"] = normalize(output["answer"]) in [
        normalize(a) for a in query["answers"]
    ]
    chunk = next((c for c in chunks if c["id"] == output["chunk_id"]), None)
    result["quote_in_selected_chunk"] = (
        chunk is not None and output["quote"] in chunk["text"]
    )
    result["reference_in_quote"] = normalize(query["evidence"]) in normalize(
        output["quote"]
    )
    result["supported"] = all(
        result[k]
        for k in ["answer_correct", "quote_in_selected_chunk", "reference_in_quote"]
    )
    return result
