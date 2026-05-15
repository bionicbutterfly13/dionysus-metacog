"""Attractor-aware state records for metacognitive control."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

from dionysus_metacog.core import MetaCogSignal
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord
from dionysus_metacog.provenance import SourceReference


class AttractorControlPolicy(StrEnum):
    """Control stance selected from attractor and generative-model evidence."""

    HOLD = "hold"
    STABILIZE = "stabilize"
    EXPLORE = "explore"


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


class AttractorSource(SourceReference):
    """Source record backing an attractor construct."""


@dataclass(frozen=True, slots=True)
class AttractorBasin:
    """Source-backed description of an attractor basin candidate."""

    basin_id: str
    attractor_label: str
    depth: float
    width: float
    stability: float
    sources: tuple[AttractorSource, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.basin_id:
            raise ValueError("basin_id must not be empty")
        if not self.attractor_label:
            raise ValueError("attractor_label must not be empty")
        if self.depth < 0.0:
            raise ValueError("depth must be non-negative")
        if self.width < 0.0:
            raise ValueError("width must be non-negative")
        if self.stability < 0.0:
            raise ValueError("stability must be non-negative")
        if not self.sources:
            raise ValueError("sources must not be empty")
        object.__setattr__(self, "sources", tuple(self.sources))

    @property
    def source_ids(self) -> tuple[str, ...]:
        """Return stable source identifiers for this basin."""

        return tuple(source.source_id for source in self.sources)

    def as_state(self) -> AttractorState:
        """Project the richer basin record into a host-neutral state."""

        state_metadata = {
            "attractor_label": self.attractor_label,
            "depth": str(self.depth),
            "width": str(self.width),
            "source_ids": ",".join(self.source_ids),
        }
        state_metadata.update(self.metadata)
        return AttractorState(
            basin_id=self.basin_id,
            stability=self.stability,
            metadata=state_metadata,
        )


@dataclass(frozen=True, slots=True)
class AttractorAssessment:
    """Active-inference-facing assessment of an attractor observation."""

    state: AttractorState
    model: PomdpStateRecord
    policy: AttractorControlPolicy
    free_energy_proxy: float
    source_ids: tuple[str, ...] = ()
    blanket: MarkovBlanketRecord | None = None

    def __post_init__(self) -> None:
        if self.free_energy_proxy < 0.0:
            raise ValueError("free_energy_proxy must be non-negative")
        if not self.source_ids:
            raise ValueError("source_ids must not be empty")
        object.__setattr__(self, "source_ids", tuple(self.source_ids))

    @classmethod
    def from_basin(
        cls,
        *,
        basin: AttractorBasin,
        model: PomdpStateRecord,
        blanket: MarkovBlanketRecord | None = None,
    ) -> "AttractorAssessment":
        """Assess a source-backed basin against a POMDP-style model record."""

        return cls.from_state(
            state=basin.as_state(),
            model=model,
            source_ids=basin.source_ids,
            novelty=basin.as_state().novelty,
            blanket=blanket,
        )

    @classmethod
    def from_state(
        cls,
        *,
        state: AttractorState,
        model: PomdpStateRecord,
        source_ids: tuple[str, ...],
        novelty: float | None = None,
        blanket: MarkovBlanketRecord | None = None,
    ) -> "AttractorAssessment":
        """Assess a host-neutral attractor state without requiring basin geometry."""

        observed_novelty = state.novelty if novelty is None else novelty
        free_energy_proxy = _free_energy_proxy(state=state, model=model)
        policy = _select_policy(
            stability=state.stability,
            novelty=observed_novelty,
            free_energy_proxy=free_energy_proxy,
        )
        return cls(
            state=state,
            model=model,
            policy=policy,
            free_energy_proxy=free_energy_proxy,
            source_ids=source_ids,
            blanket=blanket,
        )

    def to_signal(self) -> MetaCogSignal:
        """Convert the assessment into a portable metacognitive control signal."""

        metadata = {
            "basin_id": self.state.basin_id,
            "hidden_state": self.model.hidden_state,
            "observation": self.model.observation,
            "policy": self.policy.value,
            "source_ids": ",".join(self.source_ids),
        }
        if self.blanket is not None:
            metadata.update(
                {
                    "internal_states": ",".join(self.blanket.internal_states),
                    "external_states": ",".join(self.blanket.external_states),
                    "sensory_states": ",".join(self.blanket.sensory_states),
                    "active_states": ",".join(self.blanket.active_states),
                }
            )
        return MetaCogSignal(
            name="attractor_control",
            value=self.free_energy_proxy,
            source="dionysus_metacog.attractors",
            confidence=_confidence_from_precision(self.model.precision),
            metadata=metadata,
        )


def _free_energy_proxy(*, state: AttractorState, model: PomdpStateRecord) -> float:
    if model.expected_free_energy is not None:
        return max(0.0, model.expected_free_energy)
    return max(0.0, 1.0 - state.stability + state.novelty)


def _select_policy(
    *,
    stability: float,
    novelty: float,
    free_energy_proxy: float,
) -> AttractorControlPolicy:
    if novelty >= 0.7:
        return AttractorControlPolicy.EXPLORE
    if stability <= 0.4 or free_energy_proxy >= 0.7:
        return AttractorControlPolicy.STABILIZE
    return AttractorControlPolicy.HOLD


def _confidence_from_precision(precision: float | None) -> float:
    if precision is None:
        return 1.0
    return min(1.0, max(0.0, precision))


def default_attractor_sources() -> dict[str, AttractorSource]:
    """Return the initial source ledger for attractor-basin primitives."""

    sources = (
        AttractorSource(
            source_id="friston-2014-cognitive-dynamics",
            title="Cognitive Dynamics: From Attractors to Active Inference",
            locator="Proceedings of the IEEE 102(4), 2014",
            url="https://doi.org/10.1109/JPROC.2014.2306251",
        ),
        AttractorSource(
            source_id="context-engineering-attractor-dynamics",
            title="Attractor Dynamics",
            locator="00_COURSE/08_field_theory_integration/01_attractor_dynamics.md",
            url="https://github.com/davidkimai/Context-Engineering",
        ),
        AttractorSource(
            source_id="context-engineering-attractor-co-emerge",
            title="Attractor Co-Emergence Protocol Shell",
            locator="60_protocols/shells/attractor.co.emerge.shell.md",
            url="https://github.com/davidkimai/Context-Engineering",
        ),
        AttractorSource(
            source_id="spisak-friston-fep-attractor-network",
            title=(
                "Self-orthogonalizing attractor neural networks emerging "
                "from the free energy principle"
            ),
            locator="PNI Lab FEP attractor network article",
            url="https://pni-lab.github.io/fep-attractor-network/",
        ),
    )
    return {source.source_id: source for source in sources}


__all__ = [
    "AttractorAssessment",
    "AttractorBasin",
    "AttractorControlPolicy",
    "AttractorSource",
    "AttractorState",
    "default_attractor_sources",
]
