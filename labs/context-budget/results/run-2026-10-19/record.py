"""Record tokenizer-measured truncation and context packing, without running a model."""

import argparse, hashlib, json
from pathlib import Path
from packing import pack, truncate

ROOT = Path(__file__).resolve().parent
MODEL = "distilbert/distilgpt2"
REVISION = "2290a62682d06624634c1f46a6ad5be0f47f38aa"
CAPACITY = 112
RESERVE = 16
INSTRUCTION = "Answer only from the supplied approved decision. If evidence is missing, say insufficient evidence. Do not invent a time."
EVIDENCE = "Approved decision: the Cedar library workshop starts at 14:00. This replaces the earlier proposal."
QUESTION = "Question: What is the approved start time of the Cedar library workshop?"
DISTRACTOR = "Background archive: the reading room has wooden tables and a display of local history books. Staff discussed posters, refreshments, shelf labels, volunteer badges, and stationery. These background details do not specify an approved workshop time."


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--offline", action="store_true")
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL, revision=REVISION, local_files_only=a.offline
    )
    encode = lambda text: tokenizer.encode(text, add_special_tokens=False)
    docs = [{"id": "approved", "text": EVIDENCE}] + [
        {"id": f"archive-{i}", "text": DISTRACTOR} for i in range(1, 4)
    ]
    full = "\n\n".join([INSTRUCTION, *[d["text"] for d in docs], QUESTION])
    ids = encode(full)
    packed = pack(
        INSTRUCTION, QUESTION, docs, CAPACITY, RESERVE, lambda text: len(encode(text))
    )
    records = []
    for name, token_ids in [
        ("full", ids),
        ("prefix", truncate(ids, CAPACITY - RESERVE, "prefix")),
        ("suffix", truncate(ids, CAPACITY - RESERVE, "suffix")),
        ("packed", encode(packed["text"])),
    ]:
        decoded = tokenizer.decode(token_ids, clean_up_tokenization_spaces=False)
        records.append(
            {
                "condition": name,
                "ids": token_ids,
                "pieces": [
                    tokenizer.decode([t], clean_up_tokenization_spaces=False)
                    for t in token_ids
                ],
                "text": decoded,
                "input_tokens": len(token_ids),
                "within_budget": len(token_ids) + RESERVE <= CAPACITY,
                "retained": {
                    "instruction": INSTRUCTION in decoded,
                    "evidence": EVIDENCE in decoded,
                    "question": QUESTION in decoded,
                },
            }
        )
    hashes = {}
    for name in ["record.py", "packing.py", "PROTOCOL.md"]:
        raw = (ROOT / name).read_bytes()
        (a.output / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    data = {
        "model": MODEL,
        "revision": REVISION,
        "capacity": CAPACITY,
        "reserve": RESERVE,
        "sha256": hashes,
        "documents": docs,
        "packing": packed,
        "records": records,
    }
    (a.output / "data.json").write_text(json.dumps(data, indent=2) + "\n")
    for row in records:
        print(row["condition"], row["input_tokens"], row["retained"])


if __name__ == "__main__":
    main()
