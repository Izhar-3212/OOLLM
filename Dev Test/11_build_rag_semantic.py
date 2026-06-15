import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

print("Starting Semantic RAG build...", flush=True)

def semantic_chunk(content, source_file):
    """Chunk by paragraphs and sections instead of arbitrary character counts"""
    chunks = []
    chunk_id = 0
    
    # Split by double newlines (paragraphs)
    paragraphs = content.split('\n\n')
    
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If adding this paragraph exceeds 600 chars, save current chunk
        if len(current_chunk) + len(para) > 600 and current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "source": source_file,
                "chunk_id": chunk_id
            })
            chunk_id += 1
            current_chunk = para + "\n\n"
        else:
            current_chunk += para + "\n\n"
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "source": source_file,
            "chunk_id": chunk_id
        })
    
    return chunks

# Load and chunk documents
print("Processing documents...", flush=True)
docs = []
for f in Path("./knowledge").glob("*.md"):
    content = f.read_text(encoding='utf-8')
    chunks = semantic_chunk(content, f.name)
    docs.extend(chunks)

print(f"Found {len(docs)} chunks.", flush=True)

# Tokenize for BM25
print("Tokenizing...", flush=True)
def tokenize(text):
    return re.findall(r'\w+', text.lower())

tokenized_corpus = [tokenize(doc["text"]) for doc in docs]

# Build BM25 index
print("Building BM25 index...", flush=True)
bm25 = BM25Okapi(tokenized_corpus)

# Save to disk
print("Saving knowledge base...", flush=True)
data_to_save = {
    "docs": docs,
    "tokenized_corpus": tokenized_corpus
}
with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f)

print("DONE! Semantic RAG system built successfully.", flush=True)