# Design: IDE Coding Copilots

**Project:** `ide-coding-copilots`  
**Parent system design:** `02-streaming-token-delivery.md`

## 1. What this POC demonstrates

Low-latency inline completion with cancel and buffer-version binding.

## 2. Architecture (POC)

```text
POST /complete → fast MockLLM → suggestion + generation_id
POST /cancel/{id} → mark cancelled
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Fast small-model path | Inline complete must feel instant. | `tokens_per_sec=80` small mock. |
| Cancel registry | Editors cancel constantly; must be cheap. | `cancelled` set. |
| buffer_version binding | Prevents applying stale text to the wrong buffer. | Echoed in response. |

## 4. Key endpoints

`GET /health`, `POST /complete`, `POST /cancel/{generation_id}`

## 5. Tradeoffs / POC limits

Cancel after completion is a no-op race demo — real systems abort the generator task.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

