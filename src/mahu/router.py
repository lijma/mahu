"""Deterministic routing rules for Mahu."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Subskill:
    name: str
    owner: str
    reference: str
    keywords: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class RouteResult:
    request: str
    primary: str
    sequence: tuple[str, ...]
    references: tuple[str, ...]
    confidence: str
    reason: str

    def to_dict(self) -> dict:
        return {
            "request": self.request,
            "primary": self.primary,
            "sequence": list(self.sequence),
            "references": list(self.references),
            "confidence": self.confidence,
            "reason": self.reason,
        }


SUBSKILLS: tuple[Subskill, ...] = (
    Subskill(
        name="context",
        owner="fcontext",
        reference="skills/context.md",
        keywords=("context", "memory", "topic", "requirement", "decision", "knowledge", "remember", "save"),
        description="durable context, topics, requirements, and decisions",
    ),
    Subskill(
        name="prototype",
        owner="fdesign",
        reference="skills/prototype.md",
        keywords=("prototype", "ui", "website", "app", "design", "component", "token", "journey", "sitemap"),
        description="prototype, UI, journey, tokens, components, and design-system work",
    ),
    Subskill(
        name="presentation",
        owner="fppt",
        reference="skills/presentation.md",
        keywords=("ppt", "slide", "slides", "deck", "presentation", "talk", "keynote", "share"),
        description="presentations, decks, slides, and talks",
    ),
    Subskill(
        name="review",
        owner="floop-client",
        reference="skills/review.md",
        keywords=("review", "feedback", "comment", "comments", "upload", "publish", "resolve", "shareurl"),
        description="review project/version upload, comments, and resolve loop",
    ),
    Subskill(
        name="test",
        owner="testboat",
        reference="skills/test.md",
        keywords=("test", "qa", "regression", "acceptance", "smoke", "verify", "coverage", "check"),
        description="tests, QA, regression checks, and acceptance evidence",
    ),
)

_SUBSKILL_BY_NAME = {subskill.name: subskill for subskill in SUBSKILLS}
_TOKEN_PATTERN = re.compile(r"[a-z0-9#+.-]+")
_WORKFLOW_ORDER = {
    "context": 0,
    "prototype": 10,
    "presentation": 10,
    "test": 20,
    "review": 30,
}


def list_subskills() -> tuple[Subskill, ...]:
    """Return supported subskills in route priority order."""
    return SUBSKILLS


def get_subskill(name: str) -> Subskill:
    """Return a subskill by name."""
    try:
        return _SUBSKILL_BY_NAME[name]
    except KeyError as exc:
        raise ValueError(f"Unknown Mahu subskill: {name}") from exc


def route_request(request: str) -> RouteResult:
    """Classify a user request into a Mahu subskill sequence."""
    cleaned = request.strip()
    if not cleaned:
        raise ValueError("Request cannot be empty.")
    normalized = cleaned.lower()
    tokens = set(_TOKEN_PATTERN.findall(normalized))
    scores = _score(tokens, normalized)
    matched = [name for name, score in scores.items() if score > 0]

    if not matched:
        fallback = get_subskill("context")
        return RouteResult(
            request=cleaned,
            primary=fallback.name,
            sequence=(fallback.name,),
            references=(fallback.reference,),
            confidence="low",
            reason="No domain keywords matched; start by clarifying and capturing context.",
        )

    sequence = tuple(sorted(matched, key=lambda name: _workflow_priority(name)))
    primary = sequence[0]
    confidence = "high" if len(sequence) > 1 or scores[primary] >= 2 else "medium"
    references = tuple(get_subskill(name).reference for name in sequence)
    reason = _reason(sequence, scores)
    return RouteResult(cleaned, primary, sequence, references, confidence, reason)


def _score(tokens: set[str], normalized: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    for subskill in SUBSKILLS:
        score = 0
        for keyword in subskill.keywords:
            if keyword in tokens or (len(keyword) > 3 and keyword in normalized):
                score += 1
        scores[subskill.name] = score
    return scores


def _workflow_priority(name: str) -> int:
    return _WORKFLOW_ORDER.get(name, len(_WORKFLOW_ORDER))  # pragma: no cover - only known subskills are ranked


def _reason(sequence: tuple[str, ...], scores: dict[str, int]) -> str:
    if len(sequence) == 1:
        subskill = get_subskill(sequence[0])
        return f"Matched {subskill.name} keywords; load {subskill.reference}."
    route = " -> ".join(sequence)
    detail = ", ".join(f"{name}:{scores[name]}" for name in sequence)
    return f"Multi-intent request; execute in sequence {route}. Scores: {detail}."
