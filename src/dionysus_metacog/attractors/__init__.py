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


@dataclass(frozen=True, slots=True)
class AttractorSource:
    """Source record backing an attractor construct."""

    source_id: str
    title: str
    locator: str
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id must not be empty")
        if not self.title:
            raise ValueError("title must not be empty")
        if not self.locator:
            raise ValueError("locator must not be empty")


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
    "AttractorBasin",
    "AttractorSource",
    "AttractorState",
    "default_attractor_sources",
]
