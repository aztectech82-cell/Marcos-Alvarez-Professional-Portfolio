# AI Stack MVP

Prepared: 2026-05-10

This is a free-first local AI workbench MVP. The idea is simple:

1. Use a small paid API budget only for setup, testing, or cloud-only tasks.
2. Run daily work on local Ollama models for free.
3. Keep API keys private in local env files.
4. Give users click-first workflows for chat, files, and starter automations.

## What It Does

- Local chat with Ollama models such as DeepSeek, Qwen, Mistral, and Moondream.
- Optional API key slots for OpenAI, Anthropic, Gemini, Groq, OpenRouter, DeepSeek, and xAI.
- Starter automations for notes, summaries, job packets, learning plans, audits, and business playbooks.
- Safe file workspace with generated content stored locally.

## Quick Start

```powershell
cd "C:\Users\aztec\AI-TOOL\AI-Stack-MVP"
copy .env.example .env.local
notepad .env.local
.\scripts\start-free-stack.ps1
```

## Handshake Pitch

I built a local AI workbench that starts with a small optional API budget for setup but runs day-to-day on free local models. It gives AI learners, families, veterans, and builders a practical AI stack for chat, screenshot context, file work, business planning, audits, and starter automations without needing to memorize terminal commands.
