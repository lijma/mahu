"""Shared Mahu subskill metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Subskill:
    name: str
    owner: str
    reference: str
    description: str


SUBSKILLS: tuple[Subskill, ...] = (
    Subskill("context", "fcontext", "skills/context.md", "durable context, topics, requirements, and decisions"),
    Subskill("prototype", "fdesign", "skills/prototype.md", "prototype, UI, journeys, components, and design-system work"),
    Subskill("presentation", "fppt", "skills/presentation.md", "presentations, decks, slides, and talks"),
    Subskill("review", "floop-client", "skills/review.md", "review project/version upload, comments, and resolve loop"),
    Subskill("test", "testboat", "skills/test.md", "tests, QA, regression checks, and acceptance evidence"),
)

_SUBSKILL_BY_NAME = {subskill.name: subskill for subskill in SUBSKILLS}


def list_subskills() -> tuple[Subskill, ...]:
    """Return supported subskills in stable display order."""
    return SUBSKILLS


def get_subskill(name: str) -> Subskill:
    """Return a subskill by name."""
    try:
        return _SUBSKILL_BY_NAME[name]
    except KeyError as exc:
        raise ValueError(f"Unknown Mahu subskill: {name}") from exc
