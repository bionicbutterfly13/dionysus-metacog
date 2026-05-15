"""Optional Autonoesis adapter helpers.

Autonoesis owns self-model and computational-phenomenology ontology. This
adapter only translates Autonoesis-shaped objects into host-neutral payload
context and signals; it does not import Autonoesis at module import time.
"""

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from dionysus_metacog.core import JsonValue, MetaCogPayload, MetaCogSignal

_ADAPTER_SOURCE = "dionysus_metacog.adapters.autonoesis"


@runtime_checkable
class PhenomenalLike(Protocol):
    salience: float
    valence: float
    arousal: float
    perspective: str
    transparency: object


@runtime_checkable
class AgencyLike(Protocol):
    confidence: float
    intention_strength: float
    outcome_match: float
    external_override: float


@runtime_checkable
class OwnershipLike(Protocol):
    confidence: float
    continuity: float
    source_alignment: float
    alienation: float


@runtime_checkable
class BoundaryLike(Protocol):
    self_world_separation: float
    tool_incorporation: float
    social_permeability: float


@runtime_checkable
class PerspectiveLike(Protocol):
    vantage: str
    temporal_continuity: float
    embodied_anchor: str | None


@runtime_checkable
class MetaStateLike(Protocol):
    agency_precision: float
    ownership_precision: float
    introspective_access: float
    mode: object


@runtime_checkable
class SelfModelLike(Protocol):
    subject_id: str
    phenomenal: PhenomenalLike
    agency: AgencyLike
    ownership: OwnershipLike
    boundary: BoundaryLike
    perspective: PerspectiveLike
    meta: MetaStateLike
    revision: int


@runtime_checkable
class MetaAwarenessLike(Protocol):
    opacity_level: float
    cycle_state: object
    prior_type: str | None


@runtime_checkable
class MetacognitiveFeelingLike(Protocol):
    feeling_type: object
    intensity: float
    valence: float
    precision_correlate: float
    opacity_impact: float


def self_model_to_context(self_model: SelfModelLike) -> dict[str, JsonValue]:
    """Convert an Autonoesis-style SelfModel into JSON-safe payload context."""

    return {
        "subject_id": self_model.subject_id,
        "revision": self_model.revision,
        "phenomenal": {
            "salience": float(self_model.phenomenal.salience),
            "valence": float(self_model.phenomenal.valence),
            "arousal": float(self_model.phenomenal.arousal),
            "perspective": self_model.phenomenal.perspective,
            "transparency": _enum_value(self_model.phenomenal.transparency),
        },
        "agency": {
            "confidence": float(self_model.agency.confidence),
            "intention_strength": float(self_model.agency.intention_strength),
            "outcome_match": float(self_model.agency.outcome_match),
            "external_override": float(self_model.agency.external_override),
        },
        "ownership": {
            "confidence": float(self_model.ownership.confidence),
            "continuity": float(self_model.ownership.continuity),
            "source_alignment": float(self_model.ownership.source_alignment),
            "alienation": float(self_model.ownership.alienation),
        },
        "boundary": {
            "self_world_separation": float(
                self_model.boundary.self_world_separation
            ),
            "tool_incorporation": float(self_model.boundary.tool_incorporation),
            "social_permeability": float(self_model.boundary.social_permeability),
        },
        "perspective": {
            "vantage": self_model.perspective.vantage,
            "temporal_continuity": float(
                self_model.perspective.temporal_continuity
            ),
            "embodied_anchor": self_model.perspective.embodied_anchor,
        },
        "meta": {
            "agency_precision": float(self_model.meta.agency_precision),
            "ownership_precision": float(self_model.meta.ownership_precision),
            "introspective_access": float(self_model.meta.introspective_access),
            "mode": _enum_value(self_model.meta.mode),
        },
    }


def meta_awareness_to_signal(meta_awareness: MetaAwarenessLike) -> MetaCogSignal:
    """Convert an Autonoesis-style meta-awareness state into a signal."""

    opacity = _clamp_unit(meta_awareness.opacity_level)
    metadata = {
        "cycle_state": _enum_value(meta_awareness.cycle_state),
        "opacity_level": _format_number(opacity),
    }
    if meta_awareness.prior_type is not None:
        metadata["prior_type"] = meta_awareness.prior_type
    return MetaCogSignal(
        name="autonoesis.meta_awareness",
        value=opacity,
        source=_ADAPTER_SOURCE,
        confidence=round(1.0 - opacity, 6),
        metadata=metadata,
    )


def metacognitive_feeling_to_signal(
    feeling: MetacognitiveFeelingLike,
) -> MetaCogSignal:
    """Convert an Autonoesis-style metacognitive feeling into a signal."""

    return MetaCogSignal(
        name="autonoesis.metacognitive_feeling",
        value=_clamp_unit(feeling.intensity),
        source=_ADAPTER_SOURCE,
        confidence=_clamp_unit(feeling.precision_correlate),
        metadata={
            "feeling_type": _enum_value(feeling.feeling_type),
            "valence": _format_number(feeling.valence),
            "precision_correlate": _format_number(feeling.precision_correlate),
            "opacity_impact": _format_number(feeling.opacity_impact),
        },
    )


def enrich_payload_with_self_model(
    payload: MetaCogPayload,
    *,
    self_model: SelfModelLike,
    meta_awareness: MetaAwarenessLike | None = None,
    feelings: Sequence[MetacognitiveFeelingLike] = (),
) -> MetaCogPayload:
    """Return a copy of a payload enriched with Autonoesis context."""

    context = dict(payload.context)
    context["autonoesis_self_model"] = self_model_to_context(self_model)
    if meta_awareness is not None:
        opacity = _clamp_unit(meta_awareness.opacity_level)
        context["autonoesis_meta_awareness"] = {
            "opacity_level": opacity,
            "cycle_state": _enum_value(meta_awareness.cycle_state),
            "prior_type": meta_awareness.prior_type,
        }
    if feelings:
        context["autonoesis_feelings"] = tuple(
            {
                "feeling_type": _enum_value(feeling.feeling_type),
                "intensity": _clamp_unit(feeling.intensity),
                "valence": float(feeling.valence),
                "precision_correlate": _clamp_unit(feeling.precision_correlate),
                "opacity_impact": _clamp_unit(feeling.opacity_impact),
            }
            for feeling in feelings
        )
    return MetaCogPayload.from_signal(
        payload.signal,
        payload_type=payload.payload_type,
        schema_version=payload.schema_version,
        provenance=payload.provenance,
        boundary=payload.boundary,
        context=context,
    )


def _enum_value(value: object) -> str:
    return str(getattr(value, "value", value))


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, float(value)))


def _format_number(value: float) -> str:
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


__all__ = [
    "AgencyLike",
    "BoundaryLike",
    "MetaAwarenessLike",
    "MetaStateLike",
    "MetacognitiveFeelingLike",
    "OwnershipLike",
    "PerspectiveLike",
    "PhenomenalLike",
    "SelfModelLike",
    "enrich_payload_with_self_model",
    "meta_awareness_to_signal",
    "metacognitive_feeling_to_signal",
    "self_model_to_context",
]
