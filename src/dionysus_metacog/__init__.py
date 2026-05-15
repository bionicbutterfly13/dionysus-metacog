"""Dionysus MetaCog public package."""

from dionysus_metacog.attractors import (
    AttractorAssessment,
    AttractorBasin,
    AttractorControlPolicy,
    AttractorObservation,
    AttractorSource,
    AttractorState,
    AttractorTransition,
    AttractorTransitionLabel,
    default_attractor_sources,
)
from dionysus_metacog.core import (
    MetaCogPayload,
    MetaCogSignal,
    MetaCogTrace,
    PromotionLabel,
)
from dionysus_metacog.framework import FrameworkLayer, FrameworkSpec, LayerSpec
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord
from dionysus_metacog.provenance import (
    ProvenanceLedger,
    SourceConflictError,
    SourceReference,
)

__version__ = "0.1.1"

__all__ = [
    "AttractorAssessment",
    "AttractorBasin",
    "AttractorControlPolicy",
    "AttractorObservation",
    "AttractorSource",
    "AttractorState",
    "AttractorTransition",
    "AttractorTransitionLabel",
    "MarkovBlanketRecord",
    "MetaCogPayload",
    "MetaCogSignal",
    "MetaCogTrace",
    "PomdpStateRecord",
    "PromotionLabel",
    "ProvenanceLedger",
    "SourceConflictError",
    "SourceReference",
    "FrameworkLayer",
    "FrameworkSpec",
    "LayerSpec",
    "default_attractor_sources",
    "__version__",
]
