from pathlib import Path

import pytest

from mahu.enable import enable_agent


def test_enable_agent_skill_bundles(tmp_path):
    repo = Path.cwd()
    expectations = {
        "codex": tmp_path / "codex" / ".codex" / "skills" / "mahu" / "SKILL.md",
        "workbuddy": tmp_path / "workbuddy" / ".workbuddy" / "skills" / "mahu" / "SKILL.md",
        "copilot": tmp_path / "copilot" / ".github" / "skills" / "mahu" / "SKILL.md",
        "opencode": tmp_path / "opencode" / ".opencode" / "skills" / "mahu" / "SKILL.md",
    }
    for agent, skill_path in expectations.items():
        target = tmp_path / agent
        result = enable_agent(repo, target, agent)
        assert result.agent == agent
        assert skill_path.is_file()
        assert (skill_path.parent / "skills" / "review.md").is_file()
        assert (skill_path.parent / "assets" / "mahu.png").is_file()
        assert result.to_dict()["agent"] == agent


def test_enable_agent_specific_files_and_marker_replacement(tmp_path):
    repo = Path.cwd()
    copilot_target = tmp_path / "copilot"
    enable_agent(repo, copilot_target, "copilot")
    assert (copilot_target / ".github" / "instructions" / "mahu.instructions.md").is_file()
    enable_agent(repo, copilot_target, "copilot")
    assert (copilot_target / ".github" / "skills" / "mahu" / "skills" / "context.md").is_file()

    skill_root_target = tmp_path / "skill-root"
    enable_agent(repo / "skills" / "mahu", skill_root_target, "codex")
    assert (skill_root_target / ".codex" / "skills" / "mahu" / "SKILL.md").is_file()

    opencode_target = tmp_path / "opencode"
    agents_md = opencode_target / "AGENTS.md"
    agents_md.parent.mkdir(parents=True)
    agents_md.write_text("before\n\n<!-- mahu:skill -->\nold\n<!-- /mahu:skill -->\n\nafter\n", encoding="utf-8")
    enable_agent(repo, opencode_target, "opencode")
    content = agents_md.read_text(encoding="utf-8")
    assert "old" not in content
    assert "before" in content
    assert "after" in content
    assert ".opencode/skills/mahu/SKILL.md" in content

    no_end = tmp_path / "no-end"
    no_end.mkdir()
    (no_end / "AGENTS.md").write_text("x\n<!-- mahu:skill -->\nold\n", encoding="utf-8")
    enable_agent(repo, no_end, "opencode")
    assert "old" not in (no_end / "AGENTS.md").read_text(encoding="utf-8")

    append_target = tmp_path / "append"
    append_target.mkdir()
    (append_target / "AGENTS.md").write_text("existing\n", encoding="utf-8")
    enable_agent(repo, append_target, "opencode")
    assert "existing" in (append_target / "AGENTS.md").read_text(encoding="utf-8")


def test_enable_rejects_unknown_agent(tmp_path):
    with pytest.raises(ValueError, match="Unsupported"):
        enable_agent(Path.cwd(), tmp_path, "unknown")
