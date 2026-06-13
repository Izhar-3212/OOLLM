import sys

print("Step 1: Pathlib", flush=True)
from pathlib import Path

print("Step 2: ChromaDB", flush=True)
import chromadb

print("Step 3: Sentence Transformers", flush=True)
from sentence_transformers import SentenceTransformer

print("SUCCESS: All imports worked!", flush=True)