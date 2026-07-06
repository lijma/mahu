import json
from pathlib import Path

from click.testing import CliRunner

from mahu.cli import main


def test_cli_help_and_route():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "agent skill package" in result.output
    assert "route" not in result.output


def test_cli_validate_success_and_failure(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["validate"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "manifest is valid" in result.output

    result = runner.invoke(main, ["validate", "--json-output"], catch_exceptions=False)
    assert json.loads(result.output)["valid"] is True

    result = runner.invoke(main, ["validate", "--root", str(tmp_path)], catch_exceptions=False)
    assert result.exit_code == 1
    assert "Missing required file" in result.output


def test_cli_doctor(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(
        "mahu.cli.check_dependency",
        lambda subskill: type(
            "Status",
            (),
            {
                "found": True,
                "version": "fppt 1.0",
                "path": "/bin/fppt",
                "dependency": type("Dependency", (), {"subskill": subskill, "command": "fppt", "install": "pip install fppt"})(),
                "to_dict": lambda self: {"subskill": subskill, "found": True},
            },
        )(),
    )
    result = runner.invoke(main, ["doctor", "--subskill", "presentation", "--json-output"], catch_exceptions=False)
    assert json.loads(result.output)["dependencies"][0]["subskill"] == "presentation"

    monkeypatch.setattr(
        "mahu.cli.check_all_dependencies",
        lambda: (
            type(
                "Status",
                (),
                {
                    "found": False,
                    "version": None,
                    "path": None,
                    "dependency": type("Dependency", (), {"subskill": "test", "command": "testboat", "install": "pip install testboat"})(),
                    "to_dict": lambda self: {"subskill": "test", "found": False},
                },
            )(),
        ),
    )
    result = runner.invoke(main, ["doctor"], catch_exceptions=False)
    assert result.exit_code == 1
    assert "pip install testboat" in result.output

    monkeypatch.setattr("mahu.cli.check_dependency", lambda subskill: (_ for _ in ()).throw(ValueError("bad subskill")))
    result = runner.invoke(main, ["doctor", "--subskill", "bad"], catch_exceptions=False)
    assert result.exit_code == 1
    assert "bad subskill" in result.output


def test_cli_enable_success_and_failure(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["enable", "codex", "--target", str(tmp_path), "--json-output"],
        catch_exceptions=False,
    )
    payload = json.loads(result.output)
    assert payload["agent"] == "codex"
    assert (tmp_path / ".codex" / "skills" / "mahu" / "SKILL.md").is_file()

    human_target = tmp_path / "human"
    result = runner.invoke(
        main,
        ["enable", "workbuddy", "--target", str(human_target)],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "Mahu enabled for workbuddy" in result.output

    broken_root = tmp_path / "broken"
    broken_root.mkdir()
    result = runner.invoke(
        main,
        ["enable", "codex", "--target", str(tmp_path), "--root", str(broken_root)],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Missing required file" in result.output
