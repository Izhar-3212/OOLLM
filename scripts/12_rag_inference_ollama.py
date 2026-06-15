import json
import os
import re
import sys
import requests
from rank_bm25 import BM25Okapi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

CFG = rag_lib.load_config()
INF = CFG["inference"]
# Minimum top BM25 score for retrieval to count as relevant (BM25 is unbounded).
# Below this, the query found nothing useful -> friendly fallback, no hallucination.
RELEVANCE_THRESHOLD = INF["relevance_threshold_bm25"]

print("Loading RAG components...", flush=True)

# 1. Load Knowledge Base
print("Loading knowledge base...", flush=True)
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

docs = data["docs"]
tokenized_corpus = data["tokenized_corpus"]
bm25 = BM25Okapi(tokenized_corpus)
print(f"✓ Loaded {len(docs)} chunks", flush=True)

# 2. Helper functions
def tokenize(text):
    return re.findall(r'\w+', text.lower())

def search_knowledge_base(query, top_k=None):
    if top_k is None:
        top_k = INF["retrieval_top_k"]
    scores = bm25.get_scores(rag_lib.expand_query(query))
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    top_indices.reverse()
    # Return (chunk dict, score) pairs for source attribution.
    return [(docs[i], float(scores[i])) for i in top_indices]

SYSTEM = (
    "You are Mini Me, an expert Agile Project Management assistant. "
    "Use the following context to answer the user's question accurately. "
    "If the context doesn't contain the answer, use your general Agile knowledge.\n\n"
    "CONTEXT:\n{context}"
)


def get_answer_from_ollama(system, prompt):
    """Generate via Ollama using the model's own chat template (system + user)."""
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': INF["ollama_model"],
            'system': system,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': INF["temperature"],
                'num_predict': INF["ollama_num_predict"],
            },
        },
        timeout=300,
    )
    response.raise_for_status()
    return response.json()['response']

def chat_with_mini_me(user_input):
    # 1. Find relevant Agile docs as (chunk dict, score) pairs.
    results = search_knowledge_base(user_input)

    # Relevance gate: if the best chunk is below threshold, retrieval found
    # nothing useful -- redirect instead of hallucinating from junk context.
    if rag_lib.top_score(results) < RELEVANCE_THRESHOLD:
        return rag_lib.FALLBACK_MESSAGE

    context = "\n\n---\n\n".join(chunk["text"] for chunk, _ in results)

    # 2. Generate (mini-me-q8's Modelfile TEMPLATE reproduces the TinyLlama
    #    chat format, so we just pass system + user and let Ollama format it).
    answer = get_answer_from_ollama(SYSTEM.format(context=context), user_input).strip()

    # 3. Append source attribution (what was retrieved, not a verified citation).
    return f"{answer}\n\n{rag_lib.format_sources(results)}"

# Main Loop
print("\n" + "="*60)
print(f"🤖 Mini Me is ready! [{INF['ollama_model']} via Ollama] (Type 'quit' to exit)")
print("="*60 + "\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        print("Mini Me: ", end="", flush=True)
        response = chat_with_mini_me(user_input)
        print(response)
        print()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Ollama is running: ollama serve\n")
