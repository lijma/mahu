import pytest

from mahu.router import get_subskill, list_subskills, route_request


def test_list_and_get_subskills():
    names = [subskill.name for subskill in list_subskills()]
    assert names == ["context", "prototype", "presentation", "review", "test"]
    assert get_subskill("prototype").owner == "fdesign"
    with pytest.raises(ValueError, match="Unknown"):
        get_subskill("missing")


def test_route_single_intents():
    cases = {
        "save this as a topic for later": "context",
        "build a SaaS dashboard prototype": "prototype",
        "create a PPT deck for my talk": "presentation",
        "upload this version for review and fetch comments": "review",
        "run regression tests and check coverage": "test",
    }
    for request, expected in cases.items():
        result = route_request(request)
        assert result.primary == expected
        assert result.sequence[0] == expected
        assert result.references[0] == get_subskill(expected).reference
        assert result.to_dict()["primary"] == expected


def test_route_multi_intent_sequence():
    result = route_request("build a prototype, run tests, then upload for review")
    assert result.primary == "prototype"
    assert result.sequence == ("prototype", "test", "review")
    assert result.confidence == "high"
    assert "Multi-intent" in result.reason


def test_route_fallback_and_empty_request():
    result = route_request("help me think through this")
    assert result.primary == "context"
    assert result.confidence == "low"
    assert "clarifying" in result.reason

    with pytest.raises(ValueError, match="empty"):
        route_request("   ")
