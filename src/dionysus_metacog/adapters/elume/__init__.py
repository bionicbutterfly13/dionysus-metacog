"""Optional Elume adapter helpers.

The adapter is structural: it accepts Elume-shaped objects or compatible fakes
without importing Elume at module import time.
"""

from typing import Protocol, runtime_checkable

from dionysus_metacog.attractors import AttractorAssessment, AttractorState
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord


@runtime_checkable
class ThoughtSeedLike(Protocol):
    """Structural subset required from an Elume-style ThoughtSeed."""

    id: object
    content: str
    activation_level: float
    layer: object
    blanket_tag: object
    dominant_basin: str | None
    source_id: str | None


@runtime_checkable
class EFEResultLike(Protocol):
    """Structural subset required from an Elume-style EFE result."""

    hidden_state: str
    observation: str
    policy: str
    expected_free_energy: float
    precision: float


def thoughtseed_to_attractor_state(
    seed: ThoughtSeedLike,
    *,
    default_basin_id: str = "unassigned-thoughtseed-basin",
    novelty: float = 0.0,
) -> AttractorState:
    """Convert an Elume-style ThoughtSeed into a host-neutral attractor state."""

    seed_id = _stringify(seed.id)
    basin_id = seed.dominant_basin or default_basin_id
    return AttractorState(
        basin_id=basin_id,
        stability=_clamp_unit(seed.activation_level),
        novelty=_clamp_min(novelty),
        metadata={
            "adapter": "elume",
            "thoughtseed_id": seed_id,
            "content": seed.content,
            "layer": _enum_value(seed.layer),
            "blanket_tag": _enum_value(seed.blanket_tag),
            "source_id": seed.source_id or "",
        },
    )


def efe_result_to_pomdp_record(result: EFEResultLike) -> PomdpStateRecord:
    """Convert an Elume-style EFE result into a POMDP-style state record."""

    return PomdpStateRecord(
        hidden_state=result.hidden_state,
        observation=result.observation,
        policy=result.policy,
        expected_free_energy=result.expected_free_energy,
        precision=result.precision,
        metadata={"adapter": "elume"},
    )


def thoughtseed_to_markov_blanket(seed: ThoughtSeedLike) -> MarkovBlanketRecord:
    """Create a compact Markov blanket record from an Elume-style ThoughtSeed."""

    seed_id = _stringify(seed.id)
    return MarkovBlanketRecord(
        internal_states=(seed.dominant_basin or "unassigned-thoughtseed-basin",),
        external_states=(seed.source_id or "unknown-source",),
        sensory_states=(seed_id,),
        active_states=(_enum_value(seed.layer),),
        metadata={
            "adapter": "elume",
            "blanket_tag": _enum_value(seed.blanket_tag),
        },
    )


def thoughtseed_winner_to_assessment(
    seed: ThoughtSeedLike,
    result: EFEResultLike,
    *,
    source_ids: tuple[str, ...],
    novelty: float = 0.0,
) -> AttractorAssessment:
    """Convert a winning Elume ThoughtSeed and EFE result to an assessment."""

    return AttractorAssessment.from_state(
        state=thoughtseed_to_attractor_state(seed, novelty=novelty),
        model=efe_result_to_pomdp_record(result),
        blanket=thoughtseed_to_markov_blanket(seed),
        source_ids=source_ids,
        novelty=novelty,
    )


def _enum_value(value: object) -> str:
    raw_value = getattr(value, "value", value)
    return str(raw_value)


def _stringify(value: object) -> str:
    return str(value)


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, float(value)))


def _clamp_min(value: float) -> float:
    return max(0.0, float(value))


__all__ = [
    "EFEResultLike",
    "ThoughtSeedLike",
    "efe_result_to_pomdp_record",
    "thoughtseed_to_attractor_state",
    "thoughtseed_to_markov_blanket",
    "thoughtseed_winner_to_assessment",
]
