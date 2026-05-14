"""Core metacognitive control records."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from time import time


class PromotionLabel(StrEnum):
    """Sharing and promotion state for captured metacognitive material."""

    PRIVATE = "private"
    NEEDS_REDACTION = "needs_redaction"
    SHAREABLE = "shareable"
    UPSTREAM_CANDIDATE = "upstream_candidate"


@dataclass(frozen=True, slots=True)
class MetaCogSignal:
    """A typed metacognitive observation or control signal."""

    name: str
    value: float
    source: str
    confidence: float = 1.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if not self.source:
            raise ValueError("source must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MetaCogTrace:
    """Append-only trace item suitable for local-first metacognitive ledgers."""

    signal: MetaCogSignal
    label: PromotionLabel = PromotionLabel.PRIVATE
    created_at: float = field(default_factory=time)
    note: str = ""

    @property
    def shareable(self) -> bool:
        return self.label in {
            PromotionLabel.SHAREABLE,
            PromotionLabel.UPSTREAM_CANDIDATE,
        }


__all__ = ["MetaCogSignal", "MetaCogTrace", "PromotionLabel"]
