# Claude Code Adapter

Recommended install target:

```text
.claude/plugins/mahu/
```

Claude Code should load Mahu through the Claude plugin manifest at
`.claude/plugins/mahu/.claude-plugin/plugin.json`.

When the user invokes `/mahu`, Claude Code should read the plugin-bundled
`skills/mahu/SKILL.md` first, choose the right subskill with AI judgment, and
load only the needed `skills/mahu/skills/*.md` reference.
