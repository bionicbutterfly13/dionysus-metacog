"""Attractor-aware state records for metacognitive control."""

from collections.abc import Mapping
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class AttractorState:
    """Host-neutral description of an attractor basin observation."""

    basin_id: str
    stability: float
    novelty: float = 0.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.basin_id:
            raise ValueError("basin_id must not be empty")
        if self.stability < 0.0:
            raise ValueError("stability must be non-negative")
        if self.novelty < 0.0:
            raise ValueError("novelty must be non-negative")


__all__ = ["AttractorState"]
