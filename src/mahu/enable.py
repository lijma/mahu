"""Enable Mahu skill files into agent-specific local directories."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from mahu.manifest import resolve_skill_root


SUPPORTED_AGENTS = ("codex", "workbuddy", "copilot", "opencode")
MARKER_START = "<!-- mahu:skill -->"
MARKER_END = "<!-- /mahu:skill -->"


@dataclass(frozen=True)
class EnableResult:
    agent: str
    target: Path
    files: tuple[Path, ...]

    def to_dict(self) -> dict:
        return {
            "agent": self.agent,
            "target": str(self.target),
            "files": [str(path) for path in self.files],
        }


def enable_agent(repo_root: Path, target: Path, agent: str) -> EnableResult:
    """Enable Mahu into a target project for an agent."""
    normalized = agent.lower()
    if normalized not in SUPPORTED_AGENTS:
        raise ValueError(f"Unsupported agent: {agent}")
    source = resolve_skill_root(repo_root)
    destination_root = _agent_skill_dir(target.resolve(), normalized)
    created = _copy_skill_bundle(source, destination_root)
    if normalized == "copilot":
        created += (_write_copilot_instruction(target.resolve()),)
    if normalized == "opencode":
        created += (_write_agents_md(target.resolve()),)
    return EnableResult(normalized, target.resolve(), tuple(created))


def _agent_skill_dir(target: Path, agent: str) -> Path:
    if agent == "codex":
        return target / ".codex" / "skills" / "mahu"
    if agent == "workbuddy":
        return target / ".workbuddy" / "skills" / "mahu"
    if agent == "copilot":
        return target / ".github" / "skills" / "mahu"
    if agent == "opencode":
        return target / ".opencode" / "skills" / "mahu"
    raise ValueError(f"Unsupported agent: {agent}")  # pragma: no cover - guarded by enable_agent


def _copy_skill_bundle(source: Path, destination: Path) -> tuple[Path, ...]:
    destination.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for filename in ("SKILL.md",):
        target = destination / filename
        shutil.copyfile(source / filename, target)
        created.append(target)
    for directory in ("skills", "adapters", "assets"):
        source_dir = source / directory
        target_dir = destination / directory
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        created.extend(path for path in sorted(target_dir.rglob("*")) if path.is_file())
    return tuple(created)


def _write_copilot_instruction(target: Path) -> Path:
    path = target / ".github" / "instructions" / "mahu.instructions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "description: 'Use Mahu for context, prototype, presentation, review, and test work.'\n"
        "applyTo: '**'\n"
        "---\n\n"
        "When the user invokes `/mahu`, read `.github/skills/mahu/SKILL.md` and follow its SOP.\n",
        encoding="utf-8",
    )
    return path


def _write_agents_md(target: Path) -> Path:
    path = target / "AGENTS.md"
    section = (
        f"{MARKER_START}\n"
        "## Mahu\n\n"
        "Use Mahu for `/mahu` requests. Read `.opencode/skills/mahu/SKILL.md`, "
        "choose the right subskill, and load only the needed `skills/*.md` reference.\n"
        f"{MARKER_END}\n"
    )
    if path.exists():
        content = path.read_text(encoding="utf-8")
        if MARKER_START in content:
            before = content[: content.index(MARKER_START)]
            if MARKER_END in content:
                after = content[content.index(MARKER_END) + len(MARKER_END) :]
            else:
                after = ""
            content = before + section + after
        else:
            content = content.rstrip() + "\n\n" + section
    else:
        content = section
    path.write_text(content, encoding="utf-8")
    return path
