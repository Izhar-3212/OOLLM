"""
Run the eval suite against an Ollama model (e.g. the quantized `mini-me`).

Mirror of 13_run_evals.py but swaps the generation backend from transformers
to Ollama, so we can measure whether Q4_K_M quantization cost any accuracy.
Everything else is held identical for a fair comparison:
  - same eval_questions.json
  - same BM25 retrieval + query expansion + eval.retrieval_top_k
  - same system/context + user prompt (mini-me's Modelfile TEMPLATE reproduces
    the TinyLlama chat format, so the prompt matches the transformers eval)
  - deterministic decoding (temperature 0, repeat_penalty 1.0) to match the
    transformers eval's greedy mode (do_sample=False, no penalty)

Output format is identical to 13_run_evals.py, so scripts/14_score_evals_v3.py
scores it unchanged. Env vars: OLLAMA_MODEL (default mini-me), EXPAND_QUERY.
"""
import json
import os
import sys
import time
from datetime import datetime

import requests
from rank_bm25 import BM25Okapi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

CFG = rag_lib.load_config()
EVAL = CFG["eval"]
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", CFG["inference"]["ollama_model"])
EXPAND_QUERY = os.environ.get("EXPAND_QUERY", "1") != "0"
OLLAMA_URL = "http://localhost:11434/api/generate"

print(f"[Ollama eval] model={OLLAMA_MODEL}  expansion={'ON' if EXPAND_QUERY else 'OFF'}  "
      f"top_k={EVAL['retrieval_top_k']}", flush=True)

with open("knowledge_base.json", encoding="utf-8") as f:
    data = json.load(f)
docs = data["docs"]
bm25 = BM25Okapi(data["tokenized_corpus"])
print(f"Loaded {len(docs)} chunks", flush=True)

with open("evals/eval_questions.json", encoding="utf-8-sig") as f:
    questions = json.load(f)
print(f"Loaded {len(questions)} questions", flush=True)

SYSTEM = (
    "You are Mini Me, an expert Agile Project Management assistant. "
    "Use the following context to answer the user's question accurately. "
    "If the context doesn't contain the answer, use your general Agile knowledge.\n\n"
    "CONTEXT:\n{context}"
)


def search(query, top_k=None):
    if top_k is None:
        top_k = EVAL["retrieval_top_k"]
    q_tokens = rag_lib.expand_query(query) if EXPAND_QUERY else rag_lib.tokenize(query)
    scores = bm25.get_scores(q_tokens)
    top = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    return [docs[i]["text"] for i in reversed(top)]


def get_answer(question):
    context = "\n\n---\n\n".join(search(question))
    resp = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "system": SYSTEM.format(context=context),
        "prompt": question,
        "stream": False,
        "options": {
            "temperature": 0,        # greedy, matches transformers eval (do_sample=False)
            "repeat_penalty": 1.0,   # no penalty, matches transformers eval
            "num_predict": EVAL["max_new_tokens"],
        },
    }, timeout=300)
    resp.raise_for_status()
    return resp.json()["response"].strip()


def main():
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    t0 = time.time()
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {q['question'][:50]}...", flush=True)
        answer = get_answer(q["question"])
        results.append({
            "id": q["id"],
            "category": q["category"],
            "question": q["question"],
            "expected_keywords": q["expected_keywords"],
            "difficulty": q["difficulty"],
            "mini_me_answer": answer,
            "timestamp": timestamp,
            "backend": f"ollama:{OLLAMA_MODEL}",
        })
        preview = answer[:100] + "..." if len(answer) > 100 else answer
        print(f"   {preview}", flush=True)

    out = f"evals/eval_results_ollama_{timestamp}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone in {time.time() - t0:.0f}s. Saved: {out}")
    print(f"Score with: python scripts/14_score_evals_v3.py {out}")


if __name__ == "__main__":
    main()
