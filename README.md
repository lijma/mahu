# Mahu

<p align="center">
  <img src="skills/mahu/assets/mahu.png" alt="Mahu" width="320">
</p>

```text
I'm Mahu, your free AI work buddy for context, prototypes, tests, feedback, and growth.
Bring me into your daily workflow.
```

Mahu is not a single builder and not another chat persona. It is a cross-agent
`/mahu` entrypoint that helps Codex, Claude Code, OpenCode, Copilot, Trae,
WorkBuddy, and future agents work through the right SOP instead of improvising
every time.

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

## Quick Start

Ask your agent to install Mahu:

```text
Install skill for me: https://github.com/lijma/mahu
```

Then use Mahu from the agent chat:

```text
/mahu create a product prototype for a checkout flow
/mahu build a deck about how to create an agent skill
/mahu upload this version for review and collect feedback
/mahu save this decision as project context
/mahu run a smoke test and summarize the risk
```

That is the intended flow: give the repo to your agent, let it inspect the
Mahu adapter for the current environment, then invoke Mahu with `/mahu`.

## Install

Most users should use the Quick Start above. Mahu includes adapters for Codex,
Claude Code, OpenCode, GitHub Copilot, Trae, and WorkBuddy, so the agent can
choose the correct install shape after reading this repository.

If you want to be explicit, say:

```text
Install skill for me: https://github.com/lijma/mahu
After installation, I want to use Mahu by typing /mahu.
```

The agent should inspect the repo, pick the adapter for itself, install the
right files, and verify the setup before using Mahu.

## How It Works

When `/mahu` is invoked, the agent should:

1. Load Mahu through the installed adapter.
2. Read the bundled `SKILL.md`.
3. Choose the right subskill with AI judgment.
4. Load only the needed file under `skills/`.
5. Run `mahu doctor --subskill <name>` or check the dependency directly.
6. Follow that subskill's validation loop.

Each Mahu subskill declares its own dependency:

| Subskill | Required CLI | Typical install |
| --- | --- | --- |
| `context` | `fcontext` | `pip install fcontext` |
| `prototype` | `fdesign` | `pip install fdesign` |
| `presentation` | `fppt` | `pip install fppt` |
| `review` | `floop` | `pip install floop` |
| `test` | `testboat` | `pip install testboat` |

## Advanced

The CLI is optional. It exists so agents can perform deterministic install,
validation, and dependency checks when a manual path is useful.

Install from PyPI:

```bash
pip install mahu
```

Or install from GitHub:

```bash
pip install git+https://github.com/lijma/mahu.git
```

Install Mahu into a specific agent workspace:

```bash
mahu enable claude --target .
mahu enable codex --target .
mahu enable copilot --target .
mahu enable opencode --target .
mahu enable trae --target .
mahu enable workbuddy --target .
```

What `mahu enable` writes:

| Agent | Files created |
| --- | --- |
| Claude Code | `.claude/plugins/mahu/` with `.claude-plugin/plugin.json` and bundled `skills/mahu/` |
| Codex | `.codex/skills/mahu/` |
| GitHub Copilot | `.github/skills/mahu/` and `.github/instructions/mahu.instructions.md` |
| OpenCode | `.opencode/skills/mahu/`, `.opencode/commands/mahu.md`, and a Mahu section in `AGENTS.md` |
| Trae | `.trae/skills/mahu/` and `.trae/rules/mahu/rule.md` |
| WorkBuddy | `.workbuddy/skills/mahu/` |

Validate the repository and dependencies:

```bash
mahu validate
mahu doctor --subskill prototype
```

## Development

```bash
PYTHONPATH=src pytest --cov=mahu --cov-report=term-missing --cov-fail-under=100
```
