"""Model records for active-inference metacognition."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PomdpStateRecord:
    """Minimal POMDP-style state record for metacognitive controllers."""

    hidden_state: str
    observation: str
    policy: str
    expected_free_energy: float | None = None
    precision: float | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.hidden_state:
            raise ValueError("hidden_state must not be empty")
        if not self.observation:
            raise ValueError("observation must not be empty")
        if not self.policy:
            raise ValueError("policy must not be empty")


@dataclass(frozen=True, slots=True)
class MarkovBlanketRecord:
    """Boundary record describing internal, external, sensory, and active states."""

    internal_states: Sequence[str]
    external_states: Sequence[str]
    sensory_states: Sequence[str]
    active_states: Sequence[str]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, values in (
            ("internal_states", self.internal_states),
            ("external_states", self.external_states),
            ("sensory_states", self.sensory_states),
            ("active_states", self.active_states),
        ):
            if not values:
                raise ValueError(f"{name} must not be empty")


__all__ = ["MarkovBlanketRecord", "PomdpStateRecord"]
