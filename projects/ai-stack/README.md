# Free AI Workbench and AI Verification Stack

The Free AI Workbench is a local-first browser application for using Ollama models with workspace context and practical file tools. The goal is a useful daily operator interface that can run on-device without requiring a subscription or sending routine work to a cloud model.

## Working Features

- Local browser UI and Ollama model discovery.
- Ask-one and ask-all model comparison.
- Support for DeepSeek, Qwen, Mistral, Moondream, and other locally installed models.
- Agent-mode workspace tree, search, file reading, and attachment flows.
- File create, edit, and append operations constrained to the selected workspace.
- Voice input and screenshot/vision-model workflows where the browser and model support them.
- `AUTO BRAIN` keyword routing and a `CONDUCTOR` pipeline in which one model plans and another performs.
- Eleven reusable contexts spanning business, finance, engineering, marketing, writing, analytics, research, career, creative work, reflective/astrology work, and AI-stack development.

## Separate Cross-Verification Tool

AI-Verifier is a separate active codebase that can route the same question across five provider stacks: DeepSeek, Groq, Grok, OpenRouter, and Ollama. It is used to compare answers and surface disagreements, not to manufacture certainty through majority vote.

## Current Boundaries

- The workbench is local software, not a hosted multi-user service.
- Direct file writes exist; preview-before-overwrite remains an improvement area.
- Optional cloud-provider keys are configuration slots, not evidence that every provider route is currently enabled.
- Authentication, broad remote deployment, and a polished public installer are not complete.

## Product Direction

The planned model is free-first/shareware: a small local-model tier with an optional paid unlock. That is a plan, not current revenue.

## Supporting Documents

- [Capability inventory](AI-Stack-Capability_Inventory.md)
- [MVP overview](AI-Stack-MVP_README.md)
- [Showcase draft](AI-Stack-MVP_Showcase.md)
