"""Mahu CLI."""

from __future__ import annotations

import json
from pathlib import Path

import click

from mahu import __version__
from mahu.dependencies import check_all_dependencies, check_dependency
from mahu.enable import SUPPORTED_AGENTS, enable_agent
from mahu.manifest import validate_manifest


@click.group()
@click.version_option(__version__, prog_name="mahu")
def main():
    """Mahu — /mahu entrypoint for agent-assisted daily work."""


@main.command()
@click.option("--root", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".", help="Mahu repo root.")
@click.option("--json-output", is_flag=True, default=False, help="Output structured JSON.")
def validate(root: Path, json_output: bool):
    """Validate Mahu repository structure."""
    report = validate_manifest(root)
    if json_output:
        click.echo(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    elif report.valid:
        click.secho("✓ Mahu repository manifest is valid", fg="green", bold=True)
    else:
        for error in report.errors:
            click.secho(f"✗ {error}", fg="red", err=True)
    if not report.valid:
        raise SystemExit(1)


@main.command()
@click.option("--subskill", default=None, help="Check one subskill dependency.")
@click.option("--json-output", is_flag=True, default=False, help="Output structured JSON.")
def doctor(subskill: str | None, json_output: bool):
    """Check CLI dependencies required by Mahu subskills."""
    try:
        statuses = (check_dependency(subskill),) if subskill else check_all_dependencies()
    except ValueError as exc:
        click.secho(f"✗ {exc}", fg="red", err=True)
        raise SystemExit(1) from exc
    payload = {"ok": all(status.found for status in statuses), "dependencies": [status.to_dict() for status in statuses]}
    if json_output:
        click.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    for status in statuses:
        marker = "✓" if status.found else "✗"
        detail = status.version or status.path or status.dependency.install
        color = "green" if status.found else "yellow"
        click.secho(f"{marker} {status.dependency.subskill}: {status.dependency.command} - {detail}", fg=color)
    if not payload["ok"]:
        raise SystemExit(1)


@main.command()
@click.argument("agent", type=click.Choice(SUPPORTED_AGENTS))
@click.option("--target", type=click.Path(file_okay=False, path_type=Path), default=".", help="Target project directory.")
@click.option("--root", type=click.Path(exists=True, file_okay=False, path_type=Path), default=".", help="Mahu repo root.")
@click.option("--json-output", is_flag=True, default=False, help="Output structured JSON.")
def enable(agent: str, target: Path, root: Path, json_output: bool):
    """Install Mahu into a local agent workspace."""
    try:
        report = validate_manifest(root)
        if not report.valid:
            raise ValueError("; ".join(report.errors))
        result = enable_agent(root, target, agent)
    except ValueError as exc:
        click.secho(f"✗ {exc}", fg="red", err=True)
        raise SystemExit(1) from exc
    if json_output:
        click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return
    click.secho(f"✓ Mahu installed for {agent}", fg="green", bold=True)
    for path in result.files:
        click.echo(f"  {path}")


if __name__ == "__main__":
    main()  # pragma: no cover
