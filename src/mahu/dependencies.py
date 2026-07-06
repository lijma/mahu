"""Dependency checks for Mahu subskills."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Callable

from mahu.registry import get_subskill, list_subskills


@dataclass(frozen=True)
class Dependency:
    subskill: str
    owner: str
    command: str
    package: str
    install: str
    purpose: str

    def to_dict(self) -> dict:
        return {
            "subskill": self.subskill,
            "owner": self.owner,
            "command": self.command,
            "package": self.package,
            "install": self.install,
            "purpose": self.purpose,
        }


@dataclass(frozen=True)
class DependencyStatus:
    dependency: Dependency
    found: bool
    path: str | None = None
    version: str | None = None

    def to_dict(self) -> dict:
        data = self.dependency.to_dict()
        data.update({"found": self.found, "path": self.path, "version": self.version})
        return data


DEPENDENCIES: tuple[Dependency, ...] = (
    Dependency("context", "fcontext", "fcontext", "fcontext", "pip install fcontext", "topics, requirements, decisions, and durable context"),
    Dependency("prototype", "fdesign", "fdesign", "fdesign", "pip install fdesign", "prototype and design-system workflow"),
    Dependency("presentation", "fppt", "fppt", "fppt", "pip install fppt", "presentation and HTML deck workflow"),
    Dependency("review", "floop-client", "floop", "floop", "pip install floop", "review project/version upload and comments"),
    Dependency("test", "testboat", "testboat", "testboat", "pip install testboat", "tests, QA, regression, and acceptance evidence"),
)

_DEPENDENCY_BY_SUBSKILL = {dependency.subskill: dependency for dependency in DEPENDENCIES}


def list_dependencies() -> tuple[Dependency, ...]:
    """Return dependency contracts in subskill order."""
    return DEPENDENCIES


def get_dependency(subskill: str) -> Dependency:
    """Return the dependency contract for a subskill."""
    get_subskill(subskill)
    return _DEPENDENCY_BY_SUBSKILL[subskill]


def check_dependency(
    subskill: str,
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> DependencyStatus:
    """Check whether the CLI required by a subskill is available."""
    dependency = get_dependency(subskill)
    path = which(dependency.command)
    if not path:
        return DependencyStatus(dependency, found=False)
    version = _read_version(dependency.command, runner)
    return DependencyStatus(dependency, found=True, path=path, version=version)


def check_all_dependencies(
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> tuple[DependencyStatus, ...]:
    """Check all subskill dependencies."""
    return tuple(
        check_dependency(subskill.name, which=which, runner=runner)
        for subskill in list_subskills()
    )


def _read_version(command: str, runner: Callable[..., subprocess.CompletedProcess]) -> str | None:
    try:
        result = runner(
            [command, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    output = (result.stdout or result.stderr or "").strip()
    return output.splitlines()[0] if output else None
