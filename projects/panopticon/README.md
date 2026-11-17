# Panopticon — Phased Executive-Intelligence Pipeline

Panopticon turns email, document, repository, task-board, public-contract, publishing, and social-service signals into one executive brief. Its current architecture isolates sources into bounded phases so a slow or rejected integration cannot destroy the entire report.

## Architecture

1. Email and job intelligence.
2. Project-document inventory.
3. GitHub and local operating intelligence.
4. Trello, SAM.gov, Ghost, and social services.
5. Final assembly, local persistence, and optional delivery.

Each phase has its own wall-clock budget and returns `completed`, `timeout`, or `error`. Final assembly continues with explicit coverage markers and safe empty values when a source fails. A durable manifest records timing and outcome by phase.

## Live Validation

An authorized full run on September 13, 2026 completed in approximately 152 seconds:

- Eight enabled email accounts completed; 207 messages were inspected across 241 folders.
- 31,997 documents were indexed across 2,374 directories.
- Local intelligence summarized five commits in 24 hours, 93 in seven days, 43 strategy documents, and 132 knowledge-base files.
- Trello returned 44 active tasks.
- The canonical brief and run manifest were created successfully.

## Reliability Lesson

“The phase returned” is deliberately different from “every credential worked.” During the same validation, several external services returned authorization failures. Panopticon recorded those failures and still completed the useful portions of the brief. That distinction prevents a green process status from hiding degraded integrations.

## Safety and Privacy

- Source payloads containing full email bodies are removed after successful assembly.
- The compact run and finalization manifests remain for diagnosis.
- Credentials are environment-managed and are not included here.
- Portfolio metrics are aggregate counts; no message bodies, recipients, or private task content are published.

## Tools

Python, subprocess isolation, JSON manifests, IMAP/API adapters, Markdown reporting, Windows Task Scheduler, and automated tests.
