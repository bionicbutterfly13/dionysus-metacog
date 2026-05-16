"""Reusable host-shaped fixtures for optional adapter compatibility tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CompatibleThoughtSeed:
    id: str = "seed-source-risk"
    content: str = "Protect source attribution before adapting prototype code"
    activation_level: float = 0.74
    layer: str = "metacognitive"
    blanket_tag: str = "internal"
    dominant_basin: str | None = "source-risk"
    source_id: str | None = "conversation"


@dataclass(frozen=True)
class CompatibleEfeResult:
    hidden_state: str = "source-risk"
    observation: str = "unlicensed-code-reference"
    policy: str = "stabilize"
    expected_free_energy: float = 0.76
    precision: float = 0.62


@dataclass(frozen=True)
class CompatiblePhenomenalState:
    salience: float = 0.62
    valence: float = -0.2
    arousal: float = 0.46
    perspective: str = "first_person"
    transparency: str = "partly_opaque"


@dataclass(frozen=True)
class CompatibleAgency:
    confidence: float = 0.81
    intention_strength: float = 0.9
    outcome_match: float = 0.64
    external_override: float = 0.08


@dataclass(frozen=True)
class CompatibleOwnership:
    confidence: float = 0.78
    continuity: float = 0.84
    source_alignment: float = 0.69
    alienation: float = 0.12


@dataclass(frozen=True)
class CompatibleBoundary:
    self_world_separation: float = 0.88
    tool_incorporation: float = 0.22
    social_permeability: float = 0.16


@dataclass(frozen=True)
class CompatiblePerspective:
    vantage: str = "first_person"
    temporal_continuity: float = 0.86
    embodied_anchor: str | None = "breath"


@dataclass(frozen=True)
class CompatibleMetaState:
    agency_precision: float = 0.67
    ownership_precision: float = 0.61
    introspective_access: float = 0.73
    mode: str = "active"


@dataclass(frozen=True)
class CompatibleSelfModel:
    subject_id: str = "agent-runtime"
    phenomenal: CompatiblePhenomenalState = field(
        default_factory=CompatiblePhenomenalState
    )
    agency: CompatibleAgency = field(default_factory=CompatibleAgency)
    ownership: CompatibleOwnership = field(default_factory=CompatibleOwnership)
    boundary: CompatibleBoundary = field(default_factory=CompatibleBoundary)
    perspective: CompatiblePerspective = field(default_factory=CompatiblePerspective)
    meta: CompatibleMetaState = field(default_factory=CompatibleMetaState)
    revision: int = 3


@dataclass(frozen=True)
class CompatibleMetaAwareness:
    opacity_level: float = 0.25
    cycle_state: str = "aware_of_distraction"
    prior_type: str | None = "L"


@dataclass(frozen=True)
class CompatibleMetacognitiveFeeling:
    feeling_type: str = "feeling_of_error"
    intensity: float = 0.8
    valence: float = -0.4
    precision_correlate: float = 0.7
    opacity_impact: float = 0.3


def compatible_linoss_metrics() -> dict[str, Any]:
    return {
        "energy_before": 1.0,
        "energy_after": 0.25,
        "delta_energy": -0.75,
        "mode": "implicit",
        "damping_mode": "explicit_g",
    }


def compatible_linoss_filter_result() -> dict[str, Any]:
    return {
        "m_f": [[0.2, 0.4], [0.6, 0.8]],
        "P_f": [
            [[0.5, 0.0], [0.0, 0.5]],
            [[0.25, 0.0], [0.0, 0.25]],
        ],
        "loglik": -2.5,
    }
