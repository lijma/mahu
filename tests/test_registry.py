import pytest

from mahu.registry import get_subskill, list_subskills


def test_subskill_registry():
    subskills = list_subskills()
    assert [subskill.name for subskill in subskills] == [
        "context",
        "prototype",
        "presentation",
        "review",
        "test",
    ]
    assert get_subskill("presentation").owner == "fppt"
    assert get_subskill("review").reference == "skills/review.md"
    with pytest.raises(ValueError, match="Unknown"):
        get_subskill("missing")
