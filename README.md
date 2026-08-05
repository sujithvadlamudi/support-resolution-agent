# Enterprise Support Resolution Agent

A GenAI system that resolves customer support tickets by grounding answers in real policy documents and (soon) live account/order data built to demonstrate the gap between naive LLM calls and a production-grade support automation system.

## The Problem
Enterprises have tried automating customer support for years:
- **Rule-based IVR / decision trees** :rigid, breaks on anything outside the scripted path, low deflection rates.
- **Keyword-matching FAQ bots** :no real understanding of intent, gives generic answers, doesn't stay current with policy changes.

Both approaches fail the same way: they can't reason over unstructured knowledge or combine information from multiple sources.

## What a plain LLM call gets wrong
Before adding any retrieval, I tested a raw LLM against 8 realistic support tickets with zero context. The failure mode wasn't "bad answers" — it was **confident fabrication**: the model invented refund policies, confirmed loyalty perks that may not exist, and claimed it could "check with the shipping team" when it has no such capability.

See [`naive_baseline_results.json`](./naive_baseline_results.json) for full outputs.

## Fixing it with RAG
I built a small policy knowledge base (5 documents) and added retrieval (ChromaDB) so answers are grounded in actual policy text instead of the model's memory.

**Result:** the model stopped inventing policy details, and critically started **honestly admitting** when something was outside its knowledge (e.g., real-time order status) instead of guessing.

See [`rag_results.json`](./rag_results.json) for full outputs.

### What RAG still can't fix
RAG only grounds answers in *policy text*, not *live data*. Questions like "did my order actually go through" need real order-system access — which policy documents alone can never answer. That's the next phase: an agent that can call tools to fetch real data, not just retrieve documents.

## Status
- [x] Naive baseline (evidence of the problem)
- [x] RAG grounding (policy-based fix)
- [ ] Agent orchestration + tool calling (in progress)
- [ ] Evaluation harness
- [ ] Deployment (FastAPI + Docker)
- [ ] Observability

## Stack
Python, Groq (Llama 3.3 70B), ChromaDB