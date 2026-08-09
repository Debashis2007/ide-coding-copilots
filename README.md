# Use Case: IDE / Coding Copilots

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [02 — Streaming Token Delivery](../02-streaming-token-delivery.md)

## Users & problem

Developers get inline completions and chat-in-editor. They accept partial results, switch files, sleep the laptop, and cancel constantly—streaming must be cancellable and low-overhead.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Inline latency | Very low TTFT for short completions |
| Cancel rate | High; cheap abort |
| Partial accept | Client may keep prefix; server stops |
| Context | File/repo context; often RAG ([04](../04-rag-embedding-pipeline.md)) |

## Design (from parent)

```
IDE plugin → short-lived stream (SSE or WS)
  → Completion orchestrator (debounce, cache)
  → Fast small-model fleet for inline; larger for chat panel
  → Cancel = abort generation_id immediately
```

Reuse sequenced events; optimize for **short generations** and **extreme cancel rates**.

## Specializations

| vs chat product | IDE choice |
|-----------------|------------|
| Debounce | Keystroke coalescing before GPU spend |
| Speculative | Speculative decoding / small model first |
| State | Often ephemeral; less multi-device sync |
| Privacy | Repo secrets redaction; ZDR modes |

## Failure modes

- Cancel storms still billed wrong → meter completed tokens only; abort promptly.
- Stale completion applied to wrong buffer → bind `generation_id` to buffer version/hash.
- Laptop sleep → resume or discard; never duplicate insert.



## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd ide-coding-copilots
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/complete -H 'Content-Type: application/json' -d '{"prefix":"def add(","buffer_version":1}' | jq
