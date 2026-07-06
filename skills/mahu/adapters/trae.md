# Trae Adapter

Recommended install target:

```text
.trae/skills/mahu/
.trae/rules/mahu/rule.md
```

Trae has local skill evidence in the form of `~/.trae/skills/<name>/SKILL.md`.
Project templates also use `.trae/rules/<name>/rule.md` for workspace rules.

Mahu installs both shapes for Trae:

- `.trae/skills/mahu/` contains the Mahu `SKILL.md` bundle.
- `.trae/rules/mahu/rule.md` tells Trae to treat `/mahu` requests as Mahu
  requests and to load `.trae/skills/mahu/SKILL.md`.

