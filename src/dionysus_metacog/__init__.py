"""Dionysus MetaCog public package."""

from dionysus_metacog.attractors import (
    AttractorBasin,
    AttractorSource,
    AttractorState,
    default_attractor_sources,
)
from dionysus_metacog.core import MetaCogSignal, MetaCogTrace, PromotionLabel
from dionysus_metacog.framework import FrameworkLayer, FrameworkSpec, LayerSpec
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord

__version__ = "0.1.0"

__all__ = [
    "AttractorBasin",
    "AttractorSource",
    "AttractorState",
    "MarkovBlanketRecord",
    "MetaCogSignal",
    "MetaCogTrace",
    "PomdpStateRecord",
    "PromotionLabel",
    "FrameworkLayer",
    "FrameworkSpec",
    "LayerSpec",
    "default_attractor_sources",
    "__version__",
]
