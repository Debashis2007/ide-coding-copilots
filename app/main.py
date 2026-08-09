# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""IDE Coding Copilots — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "IDE Coding Copilots"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


import uuid
cancelled: set[str] = set()

class CompleteIn(BaseModel):
    prefix: str
    buffer_version: int = 1

@app.post("/complete")
async def complete(body: CompleteIn):
    gid = f"c_{uuid.uuid4().hex[:8]}"
    suggestion = await MockLLM(model="mock-small", tokens_per_sec=80).complete(
        f"Complete code: {body.prefix}", max_tokens=12
    )
    if gid in cancelled:
        return {"cancelled": True}
    return {"generation_id": gid, "buffer_version": body.buffer_version, "suggestion": suggestion}

@app.post("/cancel/{generation_id}")
def cancel(generation_id: str):
    cancelled.add(generation_id)
    return {"cancelled": generation_id}
