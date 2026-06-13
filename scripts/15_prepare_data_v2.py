"""
Build the v2 training dataset:
- Dedupe the Agile QA data (duplicates previously leaked across train/test).
- Split into train/test BY QUESTION before any expansion, so no question
  appears on both sides.
- For each QA pair, emit two examples:
    1. closed-book: plain question -> answer
    2. RAG-grounded: question + top-3 BM25 chunks in the system prompt
       (the exact prompt format used at inference) -> answer
Saves a DatasetDict to ./data/training/agile_v2_dataset
"""
import json
import random
import re

from datasets import Dataset, DatasetDict
from rank_bm25 import BM25Okapi

SEED = 42
TEST_FRACTION = 0.1
TOP_K = 3

SYSTEM_PLAIN = "You are Mini Me, an expert Agile Project Management assistant."
SYSTEM_RAG = (
    "You are Mini Me, an expert Agile Project Management assistant. "
    "Use the following context to answer the user's question accurately. "
    "If the context doesn't contain the answer, use your general Agile knowledge.\n\n"
    "CONTEXT:\n{context}"
)


def tokenize(text):
    return re.findall(r'\w+', text.lower())


def main():
    print("Loading QA data...")
    with open("data/training/agile_pm_qa.json", encoding="utf-8") as f:
        raw = json.load(f)
    print(f"  {len(raw)} raw examples")

    # Dedupe by normalized instruction (keep first occurrence)
    seen = set()
    qa_pairs = []
    for item in raw:
        key = " ".join(item["instruction"].strip().lower().split())
        if key in seen:
            continue
        seen.add(key)
        question = item["instruction"].strip()
        if item.get("input"):
            question = f"{question}\n{item['input'].strip()}"
        qa_pairs.append({"question": question, "answer": item["output"].strip()})
    print(f"  {len(qa_pairs)} after dedupe")

    print("Loading BM25 knowledge base...")
    with open("knowledge_base.json", encoding="utf-8") as f:
        kb = json.load(f)
    docs = kb["docs"]
    bm25 = BM25Okapi(kb["tokenized_corpus"])

    def retrieve(query):
        scores = bm25.get_scores(tokenize(query))
        top = sorted(range(len(scores)), key=lambda i: scores[i])[-TOP_K:]
        return [docs[i]["text"] for i in reversed(top)]

    # Split by question BEFORE expansion so closed-book and RAG variants of
    # the same question always land on the same side.
    random.seed(SEED)
    random.shuffle(qa_pairs)
    n_test = max(1, int(len(qa_pairs) * TEST_FRACTION))
    test_pairs, train_pairs = qa_pairs[:n_test], qa_pairs[n_test:]

    def expand(pairs, desc):
        rows = []
        for i, pair in enumerate(pairs):
            rows.append({
                "system": SYSTEM_PLAIN,
                "user": pair["question"],
                "assistant": pair["answer"],
            })
            context = "\n\n---\n\n".join(retrieve(pair["question"]))
            rows.append({
                "system": SYSTEM_RAG.format(context=context),
                "user": pair["question"],
                "assistant": pair["answer"],
            })
            if (i + 1) % 100 == 0:
                print(f"  {desc}: {i + 1}/{len(pairs)} questions expanded")
        return rows

    print("Building grounded examples (train)...")
    train_rows = expand(train_pairs, "train")
    print("Building grounded examples (test)...")
    test_rows = expand(test_pairs, "test")

    random.shuffle(train_rows)

    dataset = DatasetDict({
        "train": Dataset.from_list(train_rows),
        "test": Dataset.from_list(test_rows),
    })
    dataset.save_to_disk("./data/training/agile_v2_dataset")

    print(f"\nSaved: {len(train_rows)} train / {len(test_rows)} test examples")
    print("Done.")


if __name__ == "__main__":
    main()
