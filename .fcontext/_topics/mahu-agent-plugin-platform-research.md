# Mahu Agent Plugin Platform Research

Date: 2026-07-06

## Summary

Mahu should not be modeled as one universal plugin format. The stable core should be a portable agent skill, with thin platform adapters for Codex, GitHub Copilot, OpenCode, and WorkBuddy.

## Platform Findings

### Codex

- Codex skills use `SKILL.md` with YAML frontmatter.
- Codex plugins are installable bundles with `.codex-plugin/plugin.json`.
- A plugin can include skills, hooks, scripts, assets, MCP config, and apps.
- For Mahu, Codex should consume the canonical skill from a subdirectory, not the repository root.

Recommended shape:

```text
packages/codex-plugin/
  .codex-plugin/plugin.json
  skills/mahu/SKILL.md
  skills/mahu/skills/*.md
  skills/mahu/adapters/*.md
  skills/mahu/assets/mahu.png
```

### GitHub Copilot

- Copilot supports agent skills as folders with `SKILL.md`.
- Project skills can live in `.github/skills`, `.claude/skills`, or `.agents/skills`.
- Personal skills can live in `~/.copilot/skills` or `~/.agents/skills`.
- Copilot plugins are installable packages with a root `plugin.json`, and can include `agents/`, `skills/`, hooks, MCP, and LSP config.

Recommended shape:

```text
packages/copilot-plugin/
  plugin.json
  skills/mahu/SKILL.md
  skills/mahu/skills/*.md
```

### OpenCode

- OpenCode primarily uses `opencode.json` for project configuration.
- Instructions can be configured as path/glob lists.
- Agents can be represented as Markdown files and invoked as specialized assistants.
- OpenCode plugins can be loaded from plugin locations or configured packages.

Recommended shape:

```text
packages/opencode/
  opencode.json
  agents/mahu.md
  instructions/mahu.md
```

### WorkBuddy

- No reliable public developer documentation was found for WorkBuddy plugin or skill packaging.
- Mahu should keep a WorkBuddy adapter thin and avoid claiming official support until real installation/configuration rules are known.

Recommended temporary shape:

```text
packages/workbuddy/
  skills/mahu/SKILL.md
  adapters/workbuddy.md
```

## Current Mahu Gaps

1. The canonical skill currently lives at the repository root. This breaks GitHub-based skill installation because root sparse checkout can omit nested `skills/` and `adapters/`.
2. `router.py` and `mahu route` conflict with the product principle that AI should choose the subskill using judgment.
3. `SKILL.md` and `README.md` have drifted in tone and slogan.
4. `manifest.py` mixes package validation and skill validation.
5. `mahu enable` should copy from the canonical skill directory, not from the package root.

## Target Direction

Use one canonical skill source:

```text
skills/mahu/
  SKILL.md
  skills/
  adapters/
  assets/mahu.png
```

Keep CLI deterministic:

- `mahu validate`
- `mahu doctor`
- `mahu enable <agent>`

Remove CLI intent routing:

- no `mahu route`
- no keyword-based `router.py`
- use `registry.py` only as SSOT for subskill metadata and dependency checks

