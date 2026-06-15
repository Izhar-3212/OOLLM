"""
Shared retrieval helpers for the RAG scripts.

The headline feature is QUERY EXPANSION: before a search query is scored, we
inject Agile synonyms and abbreviations so a user query phrased differently
from the knowledge base still matches the right chunk. Example: a user types
"explain WIP" but the KB says "work in progress" -- expansion adds those words
to the query so BM25 (or TF-IDF) ranks the correct chunk highly.

This is query-time only. The index is NOT modified, so nothing needs to be
rebuilt. Expansion is low-risk: synonyms that appear in no chunk contribute
almost nothing to the ranking.

To extend: add a row to SYNONYM_GROUPS. Each row is a set of surface forms that
mean the same Agile concept; if any one appears in the query, all of them are
added to the search. Keep groups genuinely equivalent -- loose synonyms pull in
irrelevant chunks.
"""
import os
import re

import yaml

TOKEN_RE = re.compile(r"\w+")


def load_config():
    """Load config.yaml from the project root (parent of scripts/), CWD-independent."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

# Each inner list = surface forms of one Agile concept (abbreviations + synonyms).
SYNONYM_GROUPS = [
    ["wip", "work in progress"],
    ["po", "product owner"],
    ["sm", "scrum master"],
    ["dod", "definition of done"],
    ["dor", "definition of ready"],
    ["ci", "continuous integration"],
    ["cd", "continuous delivery", "continuous deployment"],
    ["tdd", "test driven development", "test-driven development"],
    ["bdd", "behavior driven development", "behaviour driven development"],
    ["mvp", "minimum viable product"],
    ["safe", "scaled agile framework"],
    ["art", "agile release train"],
    ["pi planning", "program increment planning"],
    ["cfd", "cumulative flow diagram"],
    ["sle", "service level expectation"],
    ["standup", "stand-up", "daily scrum", "daily standup"],
    ["grooming", "backlog refinement", "refinement"],
    ["retro", "retrospective"],
    ["estimate", "estimation", "sizing", "size"],
    ["user story", "story"],
    ["story points", "story point", "points"],
    ["ceremony", "ceremonies", "scrum event", "scrum events"],
    ["velocity", "team velocity"],
    ["mob programming", "ensemble programming"],
    ["pair programming", "pairing"],
    ["burndown", "burn-down", "burn down"],
    ["burnup", "burn-up", "burn up"],
]


def tokenize(text):
    """Match the tokenizer used to build the BM25 corpus."""
    return TOKEN_RE.findall(text.lower())


def expand_query_text(query):
    """Return the query string with matched-concept synonyms appended."""
    q = query.lower()
    additions = []
    for group in SYNONYM_GROUPS:
        if any(re.search(r"\b" + re.escape(term) + r"\b", q) for term in group):
            additions.extend(group)
    return f"{query} {' '.join(additions)}" if additions else query


def expand_query(query):
    """Tokenized, synonym-expanded query for BM25 scoring."""
    return tokenize(expand_query_text(query))


def bm25_search(query, bm25, docs, top_k=5):
    """Return the top_k (doc dict, score) pairs for a query, with expansion."""
    scores = bm25.get_scores(expand_query(query))
    top = sorted(range(len(scores)), key=lambda i: scores[i])[-top_k:]
    return [(docs[i], float(scores[i])) for i in reversed(top)]


FALLBACK_MESSAGE = (
    "I'm Mini Me, your Agile Project Management assistant. I couldn't find "
    "anything relevant in my Agile knowledge base for that. Try asking me about "
    "Scrum, Kanban, sprints, estimation, retrospectives, user stories, or other "
    "Agile topics!"
)


def top_score(results):
    """Best retrieval score from (doc, score) pairs; 0.0 if there are none.

    Used by the relevance gate: if the top score is below a retriever-specific
    threshold, the query found nothing useful and the chat should return
    FALLBACK_MESSAGE instead of forcing the model to answer from junk context.
    """
    return results[0][1] if results else 0.0


def format_sources(results):
    """Build a de-duped 'Retrieved from' footer from (chunk, score) pairs.

    Tolerates chunks without a chunk_id (the TF-IDF knowledge base omits it).
    These are retrieved chunks, not verified citations -- the model may or may
    not have used each one.
    """
    seen, lines = set(), []
    for chunk, score in results:
        key = (chunk["source"], chunk.get("chunk_id"))
        if key in seen:
            continue
        seen.add(key)
        cid = chunk.get("chunk_id")
        loc = f" (chunk {cid})" if cid is not None else ""
        lines.append(f"  - {chunk['source']}{loc}  [relevance {score:.2f}]")
    return "Retrieved from:\n" + "\n".join(lines)
