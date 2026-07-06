# OpenCode Adapter

Recommended enable target:

```text
.opencode/skills/mahu/
.opencode/commands/mahu.md
AGENTS.md
```

OpenCode should expose Mahu as a custom slash command. The command file
`.opencode/commands/mahu.md` registers `/mahu`, passes `$ARGUMENTS` through to
the prompt, and tells OpenCode to read `.opencode/skills/mahu/SKILL.md`.

`AGENTS.md` remains useful project guidance, but it is not enough to register a
slash command by itself.
