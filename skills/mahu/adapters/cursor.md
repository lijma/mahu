# Cursor Adapter

Recommended install target:

```text
.cursor/skills/mahu/
.cursor/rules/mahu.mdc
```

Cursor uses project rules under `.cursor/rules/*.mdc` for agent instructions.
Mahu installs both a skill bundle and a Cursor rule:

- `.cursor/skills/mahu/` contains the Mahu `SKILL.md` bundle.
- `.cursor/rules/mahu.mdc` tells Cursor to treat `/mahu` requests as Mahu
  requests and to load `.cursor/skills/mahu/SKILL.md`.

