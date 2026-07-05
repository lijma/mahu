import subprocess

import pytest

from mahu.dependencies import check_all_dependencies, check_dependency, get_dependency, list_dependencies


def test_dependency_contracts():
    dependencies = list_dependencies()
    assert [dependency.subskill for dependency in dependencies] == [
        "context",
        "prototype",
        "presentation",
        "review",
        "test",
    ]
    assert get_dependency("presentation").command == "fppt"
    assert get_dependency("review").command == "floop"
    assert get_dependency("test").install == "pip install testboat"
    with pytest.raises(ValueError, match="Unknown"):
        get_dependency("missing")


def test_check_dependency_found_with_version():
    def which(command):
        return f"/bin/{command}"

    def runner(args, **kwargs):
        assert args == ["fppt", "--version"]
        assert kwargs["timeout"] == 5
        return subprocess.CompletedProcess(args, 0, stdout="fppt 1.0\n", stderr="")

    status = check_dependency("presentation", which=which, runner=runner)
    assert status.found is True
    assert status.path == "/bin/fppt"
    assert status.version == "fppt 1.0"
    assert status.to_dict()["package"] == "fppt"


def test_check_dependency_missing_and_version_error():
    assert check_dependency("prototype", which=lambda command: None).found is False

    def runner(_args, **_kwargs):
        raise OSError("blocked")

    status = check_dependency("review", which=lambda command: "/bin/floop", runner=runner)
    assert status.found is True
    assert status.version is None


def test_check_all_dependencies():
    found = {"fcontext", "fdesign"}

    def which(command):
        return f"/bin/{command}" if command in found else None

    statuses = check_all_dependencies(which=which)
    assert [status.found for status in statuses].count(True) == 2
    assert [status.dependency.subskill for status in statuses][:2] == ["context", "prototype"]
