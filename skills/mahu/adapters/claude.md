# Claude Code Adapter

Recommended install target:

```text
.claude/plugins/mahu/
.claude/skills/mahu/
.claude/commands/mahu.md
```

Claude Code has two relevant surfaces:

- Model-invoked skills live under `skills/<name>/SKILL.md`.
- User-invoked slash commands can live under `commands/<name>.md`.

Mahu installs both because `/mahu` should be selectable as a command while the
same SOP remains available as a skill.

When the user invokes `/mahu`, Claude Code should read `.claude/skills/mahu/SKILL.md`,
choose the right subskill with AI judgment, and load only the needed
`.claude/skills/mahu/skills/*.md` reference.
