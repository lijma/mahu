---
name: mahu
description: Coordinate daily AI work through the /mahu entrypoint for context management, prototypes, presentations, tests, feedback loops, and growth work. Use when the user invokes /mahu or asks for help coordinating fcontext, fdesign, fppt, floop-client, or testboat workflows.
---

# Mahu

Mahu is a free AI work buddy:

> I'm Mahu, your free AI work buddy for context, prototypes, tests, feedback, and growth.
> Bring me into your daily workflow.

Mahu does not replace domain skills. Mahu helps the agent pick the right
SOP, check the local toolchain, and keep the loop honest.

## Core Rule

Use AI judgment to choose the subskill needed for the current request. Do not
preload every reference, and do not rely on deterministic keyword routing when
the user's intent needs reasoning.

## Install And Enable

If Mahu is not installed in the current environment, install it before running
Mahu CLI checks:

```bash
pip install mahu
```

If the user provided the GitHub repository instead of a package, install the CLI
from that repository:

```bash
pip install git+https://github.com/lijma/mahu.git
```

For Codex-style skill installers, install the skill from the repository
subdirectory:

```bash
install-skill-from-github.py --repo lijma/mahu --path skills/mahu --name mahu
```

After Mahu is available, enable it for the active agent workspace when the
user wants persistent `/mahu` usage:

```bash
mahu enable claude --target .
mahu enable codex --target .
mahu enable opencode --target .
mahu enable copilot --target .
mahu enable cursor --target .
mahu enable trae --target .
mahu enable workbuddy --target .
```

Claude Code uses `.claude/commands/mahu.md` for `/mahu` plus `.claude/skills/mahu/`
for skill loading. Codex, Cursor, OpenCode, Copilot, Trae, and WorkBuddy use
agent-specific skill/instruction bundles.

Pick only the matching agent. If the active agent is unknown, continue from this
`SKILL.md` without enabling an agent-specific directory.

After installation or enablement, run these checks before starting a subskill SOP:

```bash
mahu validate
mahu doctor
```

Use `mahu doctor --subskill <name>` when only one subskill is needed.

## Subskills

| Intent | Load | Owner |
| --- | --- | --- |
| context, topic, memory, requirement, decision | `skills/context.md` | fcontext |
| prototype, UI, website, app, design system | `skills/prototype.md` | fdesign |
| deck, slides, PPT, presentation, talk | `skills/presentation.md` | fppt |
| review, feedback, comments, upload, resolve | `skills/review.md` | floop-client |
| test, QA, regression, acceptance | `skills/test.md` | testboat |

If a request has multiple intents, plan a sequence. Example:

```text
"Build a prototype and upload it for review"
1. Load `skills/prototype.md` and finish fdesign validation.
2. Then load `skills/review.md` and publish the checked artifact.
```

## SOP

1. Restate the user's goal in one sentence.
2. If Mahu CLI is available or can be installed, run `mahu validate`.
3. Classify the request using AI judgment and the subskill table.
4. Load the matching `skills/*.md` file.
5. Run `mahu doctor --subskill <name>` for the selected subskill, or check the
   required CLI directly if Mahu CLI is unavailable.
6. Follow that subskill's validation loop.
7. Stop for user decisions when the subskill says to stop.
8. Store durable decisions in fcontext topics when they should survive sessions.

## Guardrails

- Do not one-shot complex work.
- Do not treat Mahu CLI routing as a substitute for AI reasoning.
- Do not use floop-client as an artifact builder.
- Do not use fppt for prototypes.
- Do not use fdesign for decks.
- Do not skip validation/check steps owned by the selected subskill.
- If unsure, ask one concise clarifying question or load `skills/context.md`
  to capture ambiguity first.
