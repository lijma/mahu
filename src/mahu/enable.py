"""Install Mahu into agent-specific local directories."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from mahu.manifest import resolve_skill_root


SUPPORTED_AGENTS = ("codex", "claude", "workbuddy", "copilot", "opencode", "trae")
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
    """Install Mahu into a target project for an agent."""
    normalized = agent.lower()
    if normalized not in SUPPORTED_AGENTS:
        raise ValueError(f"Unsupported agent: {agent}")
    if normalized == "claude":
        created = _install_claude_plugin(repo_root.resolve(), target.resolve())
    else:
        source = resolve_skill_root(repo_root)
        destination_root = _agent_skill_dir(target.resolve(), normalized)
        created = _copy_skill_bundle(source, destination_root)
    if normalized == "copilot":
        created += (_write_copilot_instruction(target.resolve()),)
    if normalized == "opencode":
        created += (_write_agents_md(target.resolve()),)
        created += (_write_opencode_command(target.resolve()),)
    if normalized == "trae":
        created += (_write_trae_rule(target.resolve()),)
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
    if agent == "trae":
        return target / ".trae" / "skills" / "mahu"
    raise ValueError(f"Unsupported agent: {agent}")  # pragma: no cover - guarded by enable_agent


def _install_claude_plugin(repo_root: Path, target: Path) -> tuple[Path, ...]:
    plugin_root = target / ".claude" / "plugins" / "mahu"
    plugin_root.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    manifest_source = repo_root / ".claude-plugin" / "plugin.json"
    if not manifest_source.is_file():
        raise ValueError("Claude plugin install requires a Mahu package root with .claude-plugin/plugin.json.")
    manifest_target = plugin_root / ".claude-plugin" / "plugin.json"
    manifest_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(manifest_source, manifest_target)
    created.append(manifest_target)

    source = resolve_skill_root(repo_root)
    created.extend(_copy_skill_bundle(source, plugin_root / "skills" / "mahu"))
    return tuple(created)


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


def _write_opencode_command(target: Path) -> Path:
    path = target / ".opencode" / "commands" / "mahu.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "description: Route a request through Mahu's daily work SOP\n"
        "---\n\n"
        "The user invoked `/mahu` with this request:\n\n"
        "$ARGUMENTS\n\n"
        "Read `.opencode/skills/mahu/SKILL.md`, classify the request with AI judgment, "
        "load only the needed Mahu subskill, run the required validation checks, and then "
        "complete the user's request.\n",
        encoding="utf-8",
    )
    return path


def _write_trae_rule(target: Path) -> Path:
    path = target / ".trae" / "rules" / "mahu" / "rule.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "name: mahu\n"
        "description: Route /mahu requests through Mahu's daily work SOP.\n"
        "alwaysApply: false\n"
        "---\n\n"
        "# Mahu\n\n"
        "Use this rule when the user invokes `/mahu` or asks to use Mahu.\n\n"
        "Read `.trae/skills/mahu/SKILL.md`, classify the request with AI judgment, "
        "load only the needed Mahu subskill, run the required validation checks, and then "
        "complete the user's request.\n",
        encoding="utf-8",
    )
    return path
