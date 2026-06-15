import os
import re
import sys
from collections import Counter

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib

PRINT_PREFIX = "[RAG] "
TOKEN_RE = re.compile(r"\b[\w'-]+\b")

CFG = rag_lib.load_config()
INF = CFG["inference"]
# Minimum top cosine similarity for retrieval to count as relevant (TF-IDF, 0-1).
# Below this, the query found nothing useful -> friendly fallback, no hallucination.
RELEVANCE_THRESHOLD = INF["relevance_threshold_tfidf"]


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def build_bow_vector(text: str, vocab: dict[str, int], idf: torch.Tensor) -> torch.Tensor:
    counts = Counter(tokenize(text))
    vector = torch.zeros(len(vocab), dtype=torch.float32)
    for token, count in counts.items():
        if token in vocab:
            vector[vocab[token]] = count * idf[vocab[token]]

    norm = vector.norm()
    return vector / norm if norm > 0 else vector


def load_knowledge_base():
    print(f"{PRINT_PREFIX}Loading RAG components...", flush=True)
    kb = torch.load("knowledge_base.pt", weights_only=False)
    docs = kb["docs"]
    db_embeddings = kb["embeddings"]
    vocab = kb.get("vocab", {})
    idf = kb.get("idf", None)
    print(f"{PRINT_PREFIX}Loaded {len(docs)} chunks.", flush=True)
    return docs, db_embeddings, vocab, idf

docs, db_embeddings, vocab, idf = load_knowledge_base()


def load_llm():
    print("Loading Mini Me (LLM)...", flush=True)
    llm_tokenizer = AutoTokenizer.from_pretrained("./models/merged", local_files_only=True)
    llm_model = AutoModelForCausalLM.from_pretrained("./models/merged", local_files_only=True)

    if llm_tokenizer.pad_token is None:
        llm_tokenizer.pad_token = llm_tokenizer.eos_token
    llm_model.config.pad_token_id = llm_tokenizer.eos_token_id

    gen_config = llm_model.generation_config
    gen_config.max_new_tokens = INF["max_new_tokens"]
    gen_config.max_length = None
    gen_config.temperature = INF["temperature"]
    gen_config.top_p = INF["top_p"]
    gen_config.top_k = INF["top_k"]
    gen_config.do_sample = INF["do_sample"]
    gen_config.repetition_penalty = INF["repetition_penalty"]

    print("Mini Me ready!", flush=True)
    return llm_tokenizer, llm_model, gen_config


llm_tokenizer, llm_model, gen_config = load_llm()

def get_embedding(text):
    if not vocab or idf is None:
        raise ValueError("Knowledge base is missing the local TF-IDF vocabulary metadata.")
    # Synonym-expand the query so abbreviations/synonyms match KB wording.
    return build_bow_vector(rag_lib.expand_query_text(text), vocab, idf).unsqueeze(0)

def search_knowledge_base(query, top_k=None):
    if top_k is None:
        top_k = INF["retrieval_top_k"]
    query_emb = get_embedding(query)
    # Calculate cosine similarity between the query vector and saved chunk embeddings.
    similarities = F.cosine_similarity(query_emb, db_embeddings, dim=1)
    # Return the top k as (chunk dict, relevance score) pairs for attribution.
    top = similarities.topk(top_k)
    return [(docs[i], float(s)) for s, i in zip(top.values, top.indices)]

def chat_with_mini_me(user_input):
    # 1. Find relevant Agile docs as (chunk dict, relevance score) pairs.
    results = search_knowledge_base(user_input)

    # Relevance gate: if the best chunk is below threshold, retrieval found
    # nothing useful -- redirect instead of hallucinating from junk context.
    if rag_lib.top_score(results) < RELEVANCE_THRESHOLD:
        return rag_lib.FALLBACK_MESSAGE

    context = "\n\n---\n\n".join(chunk["text"] for chunk, _ in results)

    # 2. Build the prompt in the same chat format the model was fine-tuned on
    messages = [
        {
            "role": "system",
            "content": "You are Mini Me, an expert Agile Project Management assistant. "
                       "Use the following context to answer the user's question accurately. "
                       "If the context doesn't contain the answer, use your general Agile knowledge.\n\n"
                       f"CONTEXT:\n{context}"
        },
        {"role": "user", "content": user_input}
    ]
    prompt = llm_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # 3. Generate response
    inputs = llm_tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = llm_model.generate(**inputs, generation_config=gen_config)

    # Decode only the newly generated tokens
    answer = llm_tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    ).strip()

    # 4. Append source attribution (what was retrieved, not a verified citation).
    return f"{answer}\n\n{rag_lib.format_sources(results)}"

def main():
    print("\n" + "="*60)
    print("🤖 Mini Me RAG is ready! (Type 'quit' to exit)")
    print("="*60 + "\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        print("Mini Me: ", end="", flush=True)
        response = chat_with_mini_me(user_input)
        print(response)
        print()


if __name__ == "__main__":
    main()