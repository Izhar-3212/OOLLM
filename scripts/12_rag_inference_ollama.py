import json
import os
import re
import sys
import requests
from rank_bm25 import BM25Okapi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

# Minimum top BM25 score for retrieval to count as relevant (BM25 is unbounded).
# Below this, the query found nothing useful -> friendly fallback, no hallucination.
RELEVANCE_THRESHOLD = 5.0

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

def search_knowledge_base(query, top_k=3):
    scores = bm25.get_scores(rag_lib.expand_query(query))
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    top_indices.reverse()
    # Return (chunk dict, score) pairs for source attribution.
    return [(docs[i], float(scores[i])) for i in top_indices]

def get_answer_from_ollama(prompt):
    """Get answer from Ollama API"""
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'qwen3.5:4b',
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.7,
                'num_predict': 200
            }
        }
    )
    return response.json()['response']

def chat_with_mini_me(user_input):
    # 1. Find relevant Agile docs as (chunk dict, score) pairs.
    results = search_knowledge_base(user_input)

    # Relevance gate: if the best chunk is below threshold, retrieval found
    # nothing useful -- redirect instead of hallucinating from junk context.
    if rag_lib.top_score(results) < RELEVANCE_THRESHOLD:
        return rag_lib.FALLBACK_MESSAGE

    context = "\n\n---\n\n".join(chunk["text"] for chunk, _ in results)

    # 2. Build the prompt (Qwen is a general instruct model; raw format is fine)
    prompt = f"""You are Mini Me, an expert Agile Project Management assistant.
Use the following context to answer the user's question accurately.
Do not make up facts. If the context doesn't contain the answer, say you don't know.

CONTEXT:
{context}

USER QUESTION: {user_input}

MINI ME ANSWER:"""

    # 3. Get response from Ollama
    response = get_answer_from_ollama(prompt)

    # Extract just the answer part
    if "MINI ME ANSWER:" in response:
        answer = response.split("MINI ME ANSWER:")[-1].strip()
    else:
        answer = response.strip()

    # 4. Append source attribution (what was retrieved, not a verified citation).
    return f"{answer}\n\n{rag_lib.format_sources(results)}"

# Main Loop
print("\n" + "="*60)
print("🤖 Mini Me RAG (Ollama) is ready! (Type 'quit' to exit)")
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
