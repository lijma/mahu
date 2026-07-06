"""Repository manifest validation for Mahu."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mahu.registry import list_subskills


REQUIRED_ADAPTERS = ("codex", "claude", "workbuddy", "copilot", "opencode", "trae")
CANONICAL_SKILL_PATH = Path("skills") / "mahu"


@dataclass(frozen=True)
class ManifestReport:
    root: Path
    kind: str
    valid: bool
    errors: tuple[str, ...]
    files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "root": str(self.root),
            "kind": self.kind,
            "valid": self.valid,
            "errors": list(self.errors),
            "files": list(self.files),
        }


def validate_manifest(root: Path) -> ManifestReport:
    """Validate that a Mahu package repo or skill directory is complete."""
    resolved = root.resolve()
    kind = _detect_kind(resolved)
    required_files = _required_files(kind)
    errors: list[str] = []
    for relative in required_files:
        path = resolved / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"Required file is empty: {relative}")
    skill_path = _skill_root(resolved, kind) / "SKILL.md"
    if skill_path.is_file():
        _validate_skill_frontmatter(skill_path, errors)
    return ManifestReport(resolved, kind, not errors, tuple(errors), tuple(required_files))


def resolve_skill_root(root: Path) -> Path:
    """Return the canonical Mahu skill directory for a package or skill root."""
    resolved = root.resolve()
    kind = _detect_kind(resolved)
    return _skill_root(resolved, kind)


def _detect_kind(root: Path) -> str:
    if (root / "SKILL.md").is_file():
        return "skill"
    return "package"


def _skill_root(root: Path, kind: str) -> Path:
    return root if kind == "skill" else root / CANONICAL_SKILL_PATH


def _required_files(kind: str) -> list[str]:
    prefix = "" if kind == "skill" else f"{CANONICAL_SKILL_PATH}/"
    files = [f"{prefix}SKILL.md"]
    files.extend(f"{prefix}{subskill.reference}" for subskill in list_subskills())
    files.extend(f"{prefix}adapters/{adapter}.md" for adapter in REQUIRED_ADAPTERS)
    files.append(f"{prefix}assets/mahu.png")
    if kind == "package":
        files = ["README.md", "pyproject.toml", ".claude-plugin/plugin.json"] + files
    return files


def _validate_skill_frontmatter(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter.")
        return
    try:
        _, frontmatter, _body = text.split("---", 2)
    except ValueError:
        errors.append("SKILL.md frontmatter is not closed.")
        return
    if "name: mahu" not in frontmatter:
        errors.append("SKILL.md frontmatter must include name: mahu.")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include description.")
