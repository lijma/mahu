"""Repository manifest validation for Mahu."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mahu.router import list_subskills


REQUIRED_ADAPTERS = ("codex", "workbuddy", "copilot", "opencode")


@dataclass(frozen=True)
class ManifestReport:
    root: Path
    valid: bool
    errors: tuple[str, ...]
    files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "root": str(self.root),
            "valid": self.valid,
            "errors": list(self.errors),
            "files": list(self.files),
        }


def validate_manifest(root: Path) -> ManifestReport:
    """Validate that a Mahu repo has the expected skill-router files."""
    resolved = root.resolve()
    required_files = _required_files()
    errors: list[str] = []
    for relative in required_files:
        path = resolved / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
            continue
        if not path.read_text(encoding="utf-8").strip():
            errors.append(f"Required file is empty: {relative}")
    skill_path = resolved / "SKILL.md"
    if skill_path.is_file():
        _validate_skill_frontmatter(skill_path, errors)
    return ManifestReport(resolved, not errors, tuple(errors), tuple(required_files))


def _required_files() -> list[str]:
    files = ["SKILL.md", "README.md", "pyproject.toml"]
    files.extend(subskill.reference for subskill in list_subskills())
    files.extend(f"adapters/{adapter}.md" for adapter in REQUIRED_ADAPTERS)
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

