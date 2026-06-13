import math
import re
from collections import Counter
from pathlib import Path

import torch

PRINT_PREFIX = "[RAG] "
TOKEN_RE = re.compile(r"\b[\w'-]+\b")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def build_tfidf_embeddings(docs: list[dict]) -> tuple[torch.Tensor, dict[str, int], torch.Tensor]:
    all_tokens = Counter()
    for item in docs:
        all_tokens.update(tokenize(item["text"]))

    vocab = {token: idx for idx, token in enumerate(sorted(all_tokens.keys()))}
    doc_term_sets = [set(tokenize(item["text"])) for item in docs]

    idf = torch.tensor(
        [
            math.log((1 + len(docs)) / (1 + sum(1 for terms in doc_term_sets if token in terms))) + 1.0
            for token in vocab
        ],
        dtype=torch.float32,
    )

    embeddings = []
    for item in docs:
        counts = Counter(tokenize(item["text"]))
        vector = torch.zeros(len(vocab), dtype=torch.float32)
        for token, count in counts.items():
            if token in vocab:
                vector[vocab[token]] = count * idf[vocab[token]]

        norm = vector.norm()
        if norm > 0:
            vector = vector / norm
        embeddings.append(vector)

    return torch.stack(embeddings), vocab, idf


def main() -> None:
    print(f"{PRINT_PREFIX}Starting local RAG build...", flush=True)

    knowledge_dir = Path("./knowledge")
    if not knowledge_dir.exists():
        print(f"{PRINT_PREFIX}Error: {knowledge_dir} does not exist.", flush=True)
        return

    docs = []
    for file_path in sorted(knowledge_dir.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")
        chunks = [content[i:i + 500] for i in range(0, len(content), 450)]
        for chunk in chunks:
            docs.append({"text": chunk, "source": file_path.name})

    print(f"{PRINT_PREFIX}Found {len(docs)} chunks.", flush=True)

    embeddings, vocab, idf = build_tfidf_embeddings(docs)

    torch.save({
        "docs": docs,
        "embeddings": embeddings,
        "vocab": vocab,
        "idf": idf,
    }, "knowledge_base.pt")

    print(f"{PRINT_PREFIX}Saved knowledge base to knowledge_base.pt", flush=True)
    print(f"{PRINT_PREFIX}RAG system built successfully.", flush=True)


if __name__ == "__main__":
    main()