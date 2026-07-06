from pathlib import Path

from mahu.manifest import resolve_skill_root, validate_manifest


def test_validate_manifest_success():
    report = validate_manifest(Path.cwd())
    assert report.valid is True
    assert report.errors == ()
    data = report.to_dict()
    assert data["valid"] is True
    assert data["kind"] == "package"
    assert ".claude-plugin/plugin.json" in data["files"]
    assert "skills/mahu/SKILL.md" in data["files"]
    assert "skills/mahu/skills/review.md" in data["files"]
    assert resolve_skill_root(Path.cwd()) == Path.cwd() / "skills" / "mahu"
    for subskill in ["context", "prototype", "presentation", "review", "test"]:
        content = (Path.cwd() / "skills" / "mahu" / "skills" / f"{subskill}.md").read_text(encoding="utf-8")
        assert "## Prerequisites" in content
        assert "mahu doctor --subskill" in content


def test_validate_skill_root_success():
    root = Path.cwd() / "skills" / "mahu"
    report = validate_manifest(root)
    assert report.valid is True
    assert report.kind == "skill"
    assert "SKILL.md" in report.files
    assert "assets/mahu.png" in report.files
    assert resolve_skill_root(root) == root


def test_validate_manifest_missing_and_empty_files(tmp_path):
    (tmp_path / "skills" / "mahu").mkdir(parents=True)
    (tmp_path / "skills" / "mahu" / "SKILL.md").write_text("---\nname: mahu\n---\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("", encoding="utf-8")
    report = validate_manifest(tmp_path)
    assert report.valid is False
    assert any("pyproject.toml" in error for error in report.errors)
    assert any("README.md" in error for error in report.errors)


def test_validate_skill_frontmatter_errors(tmp_path):
    (tmp_path / "assets").mkdir()
    for directory in ["skills", "adapters"]:
        (tmp_path / directory).mkdir()
    for relative in ["context", "prototype", "presentation", "review", "test"]:
        (tmp_path / "skills" / f"{relative}.md").write_text("ok", encoding="utf-8")
    for relative in ["codex", "claude", "workbuddy", "copilot", "opencode", "trae"]:
        (tmp_path / "adapters" / f"{relative}.md").write_text("ok", encoding="utf-8")
    (tmp_path / "assets" / "mahu.png").write_text("ok", encoding="utf-8")

    (tmp_path / "SKILL.md").write_text("no frontmatter", encoding="utf-8")
    report = validate_manifest(tmp_path)
    assert any("frontmatter" in error for error in report.errors)

    (tmp_path / "SKILL.md").write_text("---\nname: mahu\n", encoding="utf-8")
    report = validate_manifest(tmp_path)
    assert any("not closed" in error for error in report.errors)

    (tmp_path / "SKILL.md").write_text("---\ndescription: x\n---\nbody", encoding="utf-8")
    report = validate_manifest(tmp_path)
    assert any("name: mahu" in error for error in report.errors)

    (tmp_path / "SKILL.md").write_text("---\nname: mahu\n---\nbody", encoding="utf-8")
    report = validate_manifest(tmp_path)
    assert any("description" in error for error in report.errors)
