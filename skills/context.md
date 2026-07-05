# Mahu Context Subskill

Use for durable memory, topics, decisions, requirements, project background,
and context cleanup.

Owner: `fcontext`.

## Prerequisites

Required CLI: `fcontext`

Check before execution:

```bash
fcontext --help
# or
mahu doctor --subskill context
```

Install if missing:

```bash
pip install fcontext
```

If `fcontext` is missing and you do not have permission to install packages,
stop and ask the user. Do not simulate topic persistence by writing arbitrary
files unless the user explicitly requests a planning-only fallback.

## SOP

1. Decide whether the user is asking to save, retrieve, summarize, or clarify context.
2. For durable knowledge, save it as a topic.
3. For requirements, separate facts, assumptions, open questions, and decisions.
4. Keep topic names short and searchable.
5. Confirm the saved path or summarized context.

## Handoff

- If the saved context is for a deck, continue with `skills/presentation.md`.
- If the saved context is for a prototype, continue with `skills/prototype.md`.
- If the saved context is feedback from reviewers, continue with `skills/review.md`.
