# AI-TOOL — Automation and AI-Orchestration Platform

AI-TOOL is a Python-based operating platform for job intelligence, document workflows, research, and business automation. It combines deterministic rules with multiple AI providers so that model output is checked against source evidence instead of treated as ground truth.

## Verified Scale

- 160+ core Python files and 65,000+ core lines.
- Integrations for JSearch, Adzuna, Jooble, USAJOBS, Greenhouse, Lever, Workday, SmartRecruiters, Ashby, RemoteOK, Remotive, The Muse, and University of California recruiting sources.
- Five AI-provider routes: Anthropic, OpenAI-compatible endpoints, DeepSeek, Ollama, and OpenRouter.
- One live run on September 12, 2026 collected 6,212 raw listings and persisted 496 records after qualification and deduplication.

## What the System Does

1. Collects opportunities from APIs, public applicant-tracking systems, and university sources.
2. Normalizes and deduplicates records.
3. Applies deterministic qualification, compensation, freshness, and location gates.
4. Uses bounded AI analysis where judgment helps, while preserving explicit failure states.
5. Produces reviewable research and draft application materials without submitting applications automatically.

## Engineering Priorities

- Source provenance and reproducible evidence.
- Prompt-injection screening for untrusted job text.
- Fail-closed behavior when a posting, compensation range, or minimum qualification cannot be verified.
- Draft-only external actions unless the user explicitly authorizes submission or delivery.
- Human-readable logs and handoffs across multiple AI coding assistants.

## Outcome

The platform is useful not because it produces the largest possible list, but because it converts noisy listings into a smaller, auditable queue. The September 12 run retained about 8% of raw records, demonstrating that rejection and filtering are first-class outputs.

## Public Boundary

This case study contains architecture and measured throughput only. Credentials, private email content, candidate records, employer portal data, and generated application packets are excluded.

[View the AI-TOOL repository](https://github.com/aztectech82-cell/AI-TOOL)
