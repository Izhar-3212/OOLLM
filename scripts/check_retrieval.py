"""
Retrieval-only check: for each eval question, does the retrieved context
contain the expected keywords? Measures the RAG ceiling without the LLM.
"""
import json
import os
import re
import sys
from rank_bm25 import BM25Okapi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)
docs = data["docs"]
bm25 = BM25Okapi(data["tokenized_corpus"])

with open("evals/eval_questions.json", "r", encoding="utf-8-sig") as f:
    questions = json.load(f)


def tokenize(text):
    return re.findall(r'\w+', text.lower())


def search(query, top_k=5):
    scores = bm25.get_scores(rag_lib.expand_query(query))
    top = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    return [docs[i] for i in reversed(top)]


total_found = total_kw = 0
for q in questions:
    chunks = search(q["question"])
    context = " ".join(c["text"] for c in chunks).lower()
    found = [k for k in q["expected_keywords"]
             if re.search(r'\b' + re.escape(k.lower()) + r'\b', context)]
    missing = [k for k in q["expected_keywords"] if k not in found]
    total_found += len(found)
    total_kw += len(q["expected_keywords"])
    sources = ", ".join(sorted({c["source"] for c in chunks}))
    status = "OK " if len(found) == len(q["expected_keywords"]) else ("part" if found else "MISS")
    print(f"[{status}] Q{q['id']} {q['question'][:48]}")
    print(f"       keywords in context: {len(found)}/{len(q['expected_keywords'])}"
          + (f"  missing: {missing}" if missing else ""))
    print(f"       sources: {sources}")

print(f"\nRetrieval ceiling: {total_found}/{total_kw} keywords "
      f"({total_found / total_kw * 100:.0f}%) present in top-5 context")
