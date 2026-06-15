import json
import re
import torch
import os
from datetime import datetime
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from rank_bm25 import BM25Okapi

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

# A/B toggle: set EXPAND_QUERY=0 to disable query expansion in retrieval.
EXPAND_QUERY = os.environ.get("EXPAND_QUERY", "1") != "0"
print(f"[A/B] Query expansion: {'ON' if EXPAND_QUERY else 'OFF'}", flush=True)

CFG = rag_lib.load_config()
EVAL = CFG["eval"]

# Silence Hugging Face warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

print("="*60)
print("🧪 Running Mini Me Evaluation Suite")
print("="*60)

# 1. Load Knowledge Base
print("\n[1/4] Loading knowledge base...", flush=True)
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)
docs = data["docs"]
tokenized_corpus = data["tokenized_corpus"]
bm25 = BM25Okapi(tokenized_corpus)
print(f"✓ Loaded {len(docs)} chunks", flush=True)

# 2. Load Mini Me
print("\n[2/4] Loading Mini Me...", flush=True)
llm_tokenizer = AutoTokenizer.from_pretrained("./models/merged")
llm_model = AutoModelForCausalLM.from_pretrained("./models/merged")
print("✓ Mini Me loaded", flush=True)

# 3. Load Eval Questions
print("\n[3/4] Loading evaluation questions...", flush=True)
with open("evals/eval_questions.json", "r", encoding="utf-8-sig") as f:
    eval_questions = json.load(f)
print(f"✓ Loaded {len(eval_questions)} questions", flush=True)

# Helper functions
def tokenize(text):
    return re.findall(r'\w+', text.lower())

def search_knowledge_base(query, top_k=None):
    if top_k is None:
        top_k = EVAL["retrieval_top_k"]
    # A=plain query, B=synonym-expanded (controlled by EXPAND_QUERY env var).
    q_tokens = rag_lib.expand_query(query) if EXPAND_QUERY else rag_lib.tokenize(query)
    scores = bm25.get_scores(q_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    top_indices.reverse()
    return [docs[i]["text"] for i in top_indices]

def get_answer(question):
    context_chunks = search_knowledge_base(question)
    context = "\n\n---\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": "You are Mini Me, an expert Agile Project Management assistant. "
                       "Use the following context to answer the user's question accurately. "
                       "If the context doesn't contain the answer, use your general Agile knowledge.\n\n"
                       f"CONTEXT:\n{context}"
        },
        {"role": "user", "content": question}
    ]

    prompt = llm_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = llm_tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = llm_model.generate(
            **inputs,
            max_new_tokens=EVAL["max_new_tokens"],
            do_sample=EVAL["do_sample"],
            pad_token_id=llm_tokenizer.eos_token_id
        )

    return llm_tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    ).strip()

# 4. Run the Tests
print("\n[4/4] Running evaluation tests...", flush=True)
results = []
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for i, q in enumerate(eval_questions, 1):
    print(f"\n[{i}/{len(eval_questions)}] Testing: {q['question'][:50]}...", flush=True)
    
    answer = get_answer(q['question'])
    
    result = {
        "id": q["id"],
        "category": q["category"],
        "question": q["question"],
        "expected_keywords": q["expected_keywords"],
        "difficulty": q["difficulty"],
        "mini_me_answer": answer,
        "timestamp": timestamp
    }
    results.append(result)
    
    # Show a preview
    preview = answer[:100] + "..." if len(answer) > 100 else answer
    print(f"   Answer: {preview}", flush=True)

# 5. Save Results
output_file = f"evals/eval_results_{timestamp}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n" + "="*60)
print(f"✅ Evaluation complete! Results saved to: {output_file}")
print("="*60)
print(f"\nNext step: Run scripts/14_score_evals_v3.py to see the scores!")