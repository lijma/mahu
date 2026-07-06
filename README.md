# Mahu

<p align="center">
  <img src="skills/mahu/assets/mahu.png" alt="Mahu" width="320">
</p>

```text
I'm Mahu, your free AI work buddy for context, prototypes, tests, feedback, and growth.
Bring me into your daily workflow.
```

Mahu is not a single builder and not another chat persona. It is a lightweight
agent skill package that helps Codex, OpenCode, Copilot, WorkBuddy, and future
agents work through the right SOP instead of improvising every time.

Use `/mahu` when daily work needs structure: capture context, build a prototype,
create a presentation, test the result, publish it for feedback, or turn the
learning loop into growth momentum.

## What Mahu Helps With

| User intent | Mahu subskill | Owning tool |
| --- | --- | --- |
| context, memory, topics, requirements | `context` | `fcontext` |
| prototype, UI, website, app, design system | `prototype` | `fdesign` |
| deck, PPT, slides, presentation | `presentation` | `fppt` |
| review, feedback, comments, upload, resolve | `review` | `floop-client` |
| tests, QA, regression, acceptance | `test` | `testboat` |
| growth, iteration, learning loop | combine context, test, and feedback | Mahu SOP |

## Install By GitHub Link

The simplest install path is the same shape as `frontend-slides`: send your
agent the GitHub repo link and ask it to use Mahu.

The agent should:

1. Install the skill from `skills/mahu`.
2. Read `skills/mahu/SKILL.md`.
3. Classify the request with AI judgment.
4. Load only the referenced file under `skills/mahu/skills/` that matches the request.
5. Follow that subskill SOP.

For Codex-style skill installers, use:

```bash
install-skill-from-github.py --repo lijma/mahu --path skills/mahu --name mahu
```

## Local CLI

Install the CLI:

```bash
pip install mahu
```

The CLI provides deterministic checks and enablement. The skill itself lives in
`skills/mahu`.

```bash
mahu validate
mahu doctor --subskill prototype
mahu enable opencode --target .
```

Each Mahu subskill declares its own dependency. Before executing a selected
subskill, run `mahu doctor --subskill <name>` or check the required CLI
directly.

| Subskill | Required CLI | Typical install |
| --- | --- | --- |
| `context` | `fcontext` | `pip install fcontext` |
| `prototype` | `fdesign` | `pip install fdesign` |
| `presentation` | `fppt` | `pip install fppt` |
| `review` | `floop` | `pip install floop` |
| `test` | `testboat` | `pip install testboat` |

Supported enable targets:

- `codex`
- `workbuddy`
- `copilot`
- `opencode`

## Development

```bash
PYTHONPATH=src pytest --cov=mahu --cov-report=term-missing --cov-fail-under=100
```
