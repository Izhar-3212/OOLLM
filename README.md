# 🤖 Mini Me — A Local Fine-Tuned Agile Assistant

**Mini Me** is a specialized Agile Project Management assistant built by fine-tuning
[TinyLlama](https://github.com/jzhang38/TinyLlama) (1.1B parameters) and pairing it with a
Retrieval-Augmented Generation (RAG) system over a curated Agile knowledge base.

Everything runs **100% locally** — on CPU, no GPU, no cloud APIs, no per-token costs.
The model was trained, quantized, served, and evaluated entirely on a single Windows laptop.

> *"I am Mini Me, trained by Izhar."*

---

## Table of Contents
1. [What It Does](#what-it-does)
2. [Key Features](#key-features)
3. [Architecture & How It Works](#architecture--how-it-works)
4. [Quick Start](#quick-start)
5. [Project Structure — File by File (Pipeline Order)](#project-structure--file-by-file-pipeline-order)
6. [Configuration Reference](#configuration-reference)
7. [Results](#results)
8. [Notes & Gotchas](#notes--gotchas)
9. [Roadmap](#roadmap)

---

## What It Does

Ask Mini Me anything about Agile — Scrum, Kanban, estimation, user stories,
retrospectives, engineering practices, or scaling frameworks — and it answers using:

1. **A fine-tuned brain** — TinyLlama trained on ~480 curated Agile Q&A pairs, so the
   model *internally* understands Agile concepts and terminology.
2. **Retrieval grounding (RAG)** — before answering, it searches a knowledge base of 9
   curated Agile documents and feeds the most relevant passages into the prompt.
3. **Source attribution** — every answer lists which documents it drew from, with
   relevance scores.
4. **A relevance gate** — if your question isn't about Agile (or retrieval finds nothing
   relevant), it politely redirects instead of hallucinating.

Example:

```
You: What are WIP limits and why are they important?
🤖 Mini Me: WIP limits constrain the maximum number of work-in-progress items allowed
in each workflow stage. They reduce multitasking, expose bottlenecks, improve flow...

Retrieved from:
  - kanban.md (chunk 2)  [relevance 10.21]
  - agile_metrics.md (chunk 4)  [relevance 7.72]
```

---

## Key Features

| Feature | Description |
|---|---|
| **Local & private** | Runs on CPU, fully offline. No API keys, no data leaves your machine. |
| **Fine-tuned, not just prompted** | LoRA fine-tuning specializes a general 1.1B model into an Agile expert. |
| **RAG-grounded** | BM25 / TF-IDF retrieval over a curated knowledge base keeps answers factual. |
| **Two inference engines** | Fast quantized path (Ollama) **or** a self-contained transformers fallback. |
| **Query expansion** | Synonyms/abbreviations (WIP↔work in progress, DoD↔definition of done) improve retrieval. |
| **Source attribution** | Answers cite the documents they used, with relevance scores. |
| **Relevance gate** | Refuses to hallucinate on off-topic or unsupported queries. |
| **Rigorous evaluation** | A 35-question suite with a semantic grader (stemming + synonyms), not brittle keyword matching. |
| **Centralized config** | All training/inference/eval parameters live in `config.yaml`. |

---

## Architecture & How It Works

The project is a full ML pipeline, from raw data to a served, evaluated model:

```
                          ┌─────────────────────────────────────────────┐
   DATA                   │  10_generate_agile_training_data.py          │
                          │     → data/training/agile_pm_qa.json         │
                          │  15_prepare_data_v2.py  (dedupe, split,       │
                          │     add RAG-grounded examples)               │
                          │     → data/training/agile_v2_dataset          │
                          └───────────────────────┬─────────────────────┘
                                                  ▼
   TRAIN                  ┌─────────────────────────────────────────────┐
                          │  03_train_lora.py   (LoRA fine-tune, CPU)    │
                          │     → models/fine-tuned/  (adapter)          │
                          │  04_merge_model.py  (merge adapter into base)│
                          │     → models/merged/  (standalone fp16)      │
                          └───────────────────────┬─────────────────────┘
                                                  ▼
   QUANTIZE               ┌─────────────────────────────────────────────┐
                          │  Modelfile + `ollama create --quantize q8_0` │
                          │     → Ollama model "mini-me-q8" (Q8_0 GGUF)  │
                          └───────────────────────┬─────────────────────┘
                                                  ▼
   BUILD RAG INDEX        ┌─────────────────────────────────────────────┐
   (from knowledge/*.md)  │  11_build_rag_bm25.py → knowledge_base.json  │
                          │  11_build_rag.py      → knowledge_base.pt    │
                          └───────────────────────┬─────────────────────┘
                                                  ▼
   CHAT                   ┌─────────────────────────────────────────────┐
                          │  12_rag_inference_ollama.py  (FAST, primary) │
                          │  12_rag_inference.py         (slow fallback) │
                          │     retrieve → gate → generate → attribute   │
                          └─────────────────────────────────────────────┘

   EVALUATE (any time)    13_run_evals_ollama.py / 13_run_evals.py
                          → 14_score_evals_v3.py  (semantic scoring)
                          check_retrieval.py  (retrieval-only diagnostic)
```

**A single chat turn** (`chat_with_mini_me`) does four things:
1. **Retrieve** — expand the query with synonyms, score knowledge-base chunks with BM25
   (or TF-IDF), take the top-k.
2. **Gate** — if the best chunk's relevance is below a threshold, return a friendly
   fallback instead of answering from junk context.
3. **Generate** — build a prompt (system message with the retrieved context + the user
   question) in TinyLlama's chat format and generate the answer.
4. **Attribute** — append a "Retrieved from" footer listing the source documents.

---

## Quick Start

> **Prerequisites:** Python venv at `./venv` with deps installed
> (`transformers`, `datasets`, `peft`, `torch`, `rank_bm25`, `requests`, `pyyaml`, `scikit-learn`).
> For the fast path, [Ollama](https://ollama.com) installed and running.
> Run all commands from the project root. On Windows, set `PYTHONUTF8=1` to avoid console
> encoding errors from emoji output.

### Talk to Mini Me

**Fast (recommended)** — quantized model via Ollama (~11s/answer):
```powershell
$env:PYTHONUTF8 = "1"
.\venv\Scripts\python.exe scripts\12_rag_inference_ollama.py
```

**Fallback** — no Ollama needed, pure transformers (slower, ~40s/answer):
```powershell
$env:PYTHONUTF8 = "1"
.\venv\Scripts\python.exe scripts\12_rag_inference.py
```

### Evaluate the model
```powershell
$env:PYTHONUTF8 = "1"
.\venv\Scripts\python.exe scripts\13_run_evals_ollama.py   # ~13 min, runs 35 questions
.\venv\Scripts\python.exe scripts\14_score_evals_v3.py     # scores the latest results
```

### Rebuild everything from scratch
```powershell
# 1. Data
.\venv\Scripts\python.exe scripts\10_generate_agile_training_data.py
.\venv\Scripts\python.exe scripts\15_prepare_data_v2.py
# 2. Train + merge (long; ~hours on CPU)
.\venv\Scripts\python.exe scripts\03_train_lora.py
.\venv\Scripts\python.exe scripts\04_merge_model.py
# 3. Quantize into Ollama
ollama create mini-me-q8 -f Modelfile --quantize q8_0
# 4. Build the RAG indexes
.\venv\Scripts\python.exe scripts\11_build_rag_bm25.py
.\venv\Scripts\python.exe scripts\11_build_rag.py
# 5. Chat (see above)
```

(`run_pipeline.ps1` chains the train → merge → eval → score steps.)

---

## Project Structure — File by File (Pipeline Order)

### Configuration & shared code

| File | Role |
|---|---|
| **`config.yaml`** | Single source of truth for all parameters: model paths, LoRA/training hyperparameters, and the `inference`/`eval` generation + retrieval settings. Scripts read from here — nothing is hardcoded. |
| **`Modelfile`** | The Ollama recipe that imports the merged model, applies TinyLlama's chat template + stop tokens, sets generation defaults, and (via `ollama create --quantize`) produces the quantized `mini-me-q8`. Replaces the old, broken llama.cpp conversion script. |
| **`scripts/rag_lib.py`** | Shared library imported by every retrieval/chat/eval script. Provides: `load_config()`, `tokenize()`, **query expansion** (`SYNONYM_GROUPS`, `expand_query`), `bm25_search()`, **source attribution** (`format_sources`), and the **relevance gate** helpers (`top_score`, `FALLBACK_MESSAGE`). |
| **`run_pipeline.ps1`** | Orchestrates the end-to-end training pipeline: train → merge → eval → score. |

### Stage 1 — Data preparation

| File | Role |
|---|---|
| **`scripts/10_generate_agile_training_data.py`** | Generates ~300+ Agile Q&A pairs (identity, Agile fundamentals, Scrum, Kanban, estimation) → `data/training/agile_pm_qa.json`. This is Mini Me's curriculum. |
| **`scripts/15_prepare_data_v2.py`** | Turns the Q&A into a clean training set: **dedupes** questions, **splits by question** before expansion (no train/test leakage), and emits **two examples per question** — a closed-book one and a **RAG-grounded** one (with top-3 retrieved chunks in the prompt) so the model learns to *use* context. → `data/training/agile_v2_dataset`. |

### Stage 2 — Training

| File | Role |
|---|---|
| **`scripts/03_train_lora.py`** | LoRA fine-tunes TinyLlama on CPU. Key correctness fixes baked in: a real pad token (so the model learns to **stop** generating), **completion-only loss** (trains on the answer, not the prompt), chat-template prompts matching inference, dynamic padding, and a wider LoRA (`r=16`, 7 target modules). → adapter in `models/fine-tuned/`. |
| **`scripts/04_merge_model.py`** | Merges the LoRA adapter back into the base model to produce a standalone fp16 model → `models/merged/` (what inference and quantization consume). |

### Stage 3 — Quantization (speed)

Run `ollama create mini-me-q8 -f Modelfile --quantize q8_0`. Ollama imports
`models/merged/`, quantizes it to **Q8_0 GGUF**, and serves it as `mini-me-q8` —
~4× faster than fp32 transformers on CPU with effectively no quality loss.
(Q4 was tested and rejected: too aggressive for a 1.1B model.)

### Stage 4 — Build the RAG index (from `knowledge/*.md`)

| File | Role |
|---|---|
| **`scripts/11_build_rag_bm25.py`** | Chunks the knowledge base by paragraph, tokenizes, builds a **BM25** index → `knowledge_base.json`. Used by the Ollama chat and the evals. |
| **`scripts/11_build_rag.py`** | Builds a **TF-IDF** vector index → `knowledge_base.pt`. Used by the transformers (no-Ollama) chat path. |

### Stage 5 — Inference / Chat

| File | Role |
|---|---|
| **`scripts/12_rag_inference_ollama.py`** | **Primary, fast chat.** BM25 retrieval + query expansion → relevance gate → generation via Ollama (`mini-me-q8`) → source attribution. Requires the Ollama server. |
| **`scripts/12_rag_inference.py`** | **Self-contained fallback chat.** TF-IDF retrieval → relevance gate → generation via `transformers` (the fp16 merged model) → source attribution. No Ollama, but slower. |

### Stage 6 — Evaluation

| File | Role |
|---|---|
| **`scripts/13_run_evals_ollama.py`** | Runs the eval suite through an Ollama model (defaults to `mini-me-q8`). Fast (~13 min). Output format matches the transformers eval so the same scorer works. |
| **`scripts/13_run_evals.py`** | Same eval via `transformers` (slow, ~1.5h). Includes an `EXPAND_QUERY` env toggle for A/B testing query expansion. |
| **`scripts/14_score_evals_v3.py`** | **Semantic grader.** Scores answers using Porter stemming + an Agile synonym map + flexible phrase matching (so correct paraphrases aren't punished). Reports semantic vs. exact-match scores and a per-category breakdown. |
| **`scripts/check_retrieval.py`** | Retrieval-only diagnostic: checks whether each question's expected keywords appear in the top-k retrieved context — measures the *retrieval ceiling* without involving the LLM. Invaluable for separating retrieval failures from generation failures. |
| **`evals/eval_questions.json`** | The 35-question benchmark (Scrum, Kanban, metrics, user stories, engineering, scaling, plus abbreviation-phrased questions) with expected keywords and difficulty. |

### Stage 7 — Feedback loop (experimental)

| File | Role |
|---|---|
| **`scripts/feedback_manager.py`** | Stores user feedback (good / bad / corrected) → `data/feedback/feedback.json`. |
| **`scripts/08_quantized_inference.py`** | A chat loop that collects feedback after each answer and uses recent "good" examples for in-context learning. |
| **`scripts/09_retrain_with_feedback.py`** | Converts accumulated feedback into a training set for a future retraining pass. |

### Knowledge base & generated artifacts

| Path | Role |
|---|---|
| **`knowledge/*.md`** | The 9 curated Agile documents: `agile_manifesto`, `scrum_guide`, `kanban`, `estimation`, `user_stories`, `agile_metrics`, `retrospectives`, `engineering_practices`, `scaling_agile`. The source of truth for RAG. |
| `knowledge_base.json` / `.pt` | Generated BM25 / TF-IDF indexes (rebuild with the `11_*` scripts; git-ignored). |
| `models/base` · `fine-tuned` · `merged` | Base model, LoRA adapter, merged model (git-ignored; large). |
| `data/training/` | Generated datasets (git-ignored). |
| `evals/eval_results_*.json` · `score_report_*.json` | Generated eval outputs (git-ignored). |
| **`Dev Test/`** | Retired/superseded scripts kept for reference (original starter scripts, the broken GGUF converter, the v2 scorer, scratch tests). Not part of the active pipeline. |

---

## Configuration Reference

All tunable parameters live in **`config.yaml`**:

- **`training`** — LoRA rank/alpha/modules, learning rate, epochs, sequence length, the dataset path.
- **`inference`** — chat generation (`temperature`, `top_p`, `top_k`, `max_new_tokens`,
  `repetition_penalty`), retrieval (`retrieval_top_k`), relevance thresholds for each
  retriever, and the Ollama model name (`mini-me-q8`).
- **`eval`** — deterministic greedy decoding (`do_sample: false`) and retrieval settings
  for reproducible scoring (intentionally distinct from chat).

Change a setting once here and every script picks it up.

---

## Results

Measured on the 35-question suite with the semantic grader, the model improved through
a series of measured, A/B-tested fixes:

| Milestone | Score |
|---|---|
| Baseline (prompt format mismatched training) | ~23% |
| Prompt format aligned to training | ~45% |
| Knowledge base expanded & strengthened | ~79% |
| v2 retrain (EOS fix, completion-only loss, RAG-grounded data) | **~90%** |

**Speed (CPU):** fp32 transformers ≈ 3.5 tok/s → **Q8_0 via Ollama ≈ 14 tok/s** (~4× faster),
with quality matching the fp16 model. Quantizing to Q4 was measured and rejected (~5-point
quality drop on a model this small).

> Note: the score is a *semantic keyword* proxy, used as a regression guard — not a claim of
> "90% perfect answers." It exists to catch regressions and compare changes objectively.

---

## Notes & Gotchas

- **Run from the project root.** Scripts reference paths like `./models/merged` and
  `knowledge_base.json` relative to the working directory.
- **Use the project venv** (`./venv/Scripts/python.exe`). The system Python likely lacks
  `rank_bm25` and other deps.
- **Set `PYTHONUTF8=1`** on Windows, or emoji in console output can crash under the default
  cp1252 encoding.
- **Ollama must be running** for the fast chat/eval (`ollama serve`, or the desktop app).
  The transformers paths need no Ollama.
- **Eval vs. chat decoding differ by design:** evals use greedy decoding (reproducible);
  chat uses sampling (natural). Both are visible/tunable in `config.yaml`.

---

## Roadmap

- **RAG on/off ablation** — measure how much retrieval actually helps the fine-tuned model.
- **Feedback-driven retraining** — batch corrected answers + original data, retrain, gate on the eval.
- **Demand-driven KB growth** — log relevance-gate misses and expand the knowledge base where users actually ask.

---

*Built as a hands-on experiment in local LLM fine-tuning, RAG, quantization, and rigorous
evaluation — proving you don't need a massive model or a cloud budget to build something useful.*
