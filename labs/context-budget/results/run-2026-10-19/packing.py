"""Budget plain-text context explicitly; never silently drop required segments."""


def pack(instruction, question, documents, capacity, reserve, count):
    if (
        type(capacity) is not int
        or type(reserve) is not int
        or capacity <= 0
        or not 0 <= reserve < capacity
    ):
        raise ValueError("Require positive capacity and 0 <= reserve < capacity")
    if len({d["id"] for d in documents}) != len(documents):
        raise ValueError("Document IDs must be unique")
    budget = capacity - reserve

    def assemble(selected):
        return "\n\n".join([instruction, *[d["text"] for d in selected], question])

    selected = []
    if count(assemble(selected)) > budget:
        raise ValueError("Required instructions and question exceed the input budget")
    omitted = []
    for document in documents:
        if count(assemble(selected + [document])) <= budget:
            selected.append(document)
        else:
            omitted.append(document["id"])
    result = assemble(selected)
    return {
        "text": result,
        "selected": [d["id"] for d in selected],
        "omitted": omitted,
        "input_tokens": count(result),
        "input_budget": budget,
        "reserved_output_tokens": reserve,
    }


def truncate(ids, budget, side):
    if budget <= 0 or side not in ["prefix", "suffix"]:
        raise ValueError("Require positive budget and prefix or suffix")
    return ids[:budget] if side == "prefix" else ids[-budget:]
