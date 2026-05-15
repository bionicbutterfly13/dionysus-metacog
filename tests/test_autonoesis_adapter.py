from dataclasses import dataclass, field

from dionysus_metacog.adapters.autonoesis import (
    MetaAwarenessLike,
    MetacognitiveFeelingLike,
    SelfModelLike,
    enrich_payload_with_self_model,
    meta_awareness_to_signal,
    metacognitive_feeling_to_signal,
    self_model_to_context,
)
from dionysus_metacog.core import MetaCogPayload, MetaCogSignal


@dataclass
class FakePhenomenalState:
    salience: float = 0.7
    valence: float = -0.2
    arousal: float = 0.4
    perspective: str = "first_person"
    transparency: str = "partly_opaque"


@dataclass
class FakeAgency:
    confidence: float = 0.8
    intention_strength: float = 0.9
    outcome_match: float = 0.6
    external_override: float = 0.1


@dataclass
class FakeOwnership:
    confidence: float = 0.65
    continuity: float = 0.7
    source_alignment: float = 0.5
    alienation: float = 0.2


@dataclass
class FakeBoundary:
    self_world_separation: float = 0.9
    tool_incorporation: float = 0.3
    social_permeability: float = 0.2


@dataclass
class FakePerspective:
    vantage: str = "first_person"
    temporal_continuity: float = 0.85
    embodied_anchor: str | None = "breath"


@dataclass
class FakeMetaState:
    agency_precision: float = 0.6
    ownership_precision: float = 0.55
    introspective_access: float = 0.72
    mode: str = "active"


@dataclass
class FakeSelfModel:
    subject_id: str = "agent"
    phenomenal: FakePhenomenalState = field(default_factory=FakePhenomenalState)
    agency: FakeAgency = field(default_factory=FakeAgency)
    ownership: FakeOwnership = field(default_factory=FakeOwnership)
    boundary: FakeBoundary = field(default_factory=FakeBoundary)
    perspective: FakePerspective = field(default_factory=FakePerspective)
    meta: FakeMetaState = field(default_factory=FakeMetaState)
    revision: int = 7


@dataclass
class FakeMetaAwareness:
    opacity_level: float = 0.25
    cycle_state: str = "aware_of_distraction"
    prior_type: str | None = "L"


@dataclass
class FakeFeeling:
    feeling_type: str = "feeling_of_error"
    intensity: float = 0.8
    valence: float = -0.4
    precision_correlate: float = 0.7
    opacity_impact: float = 0.3


def test_self_model_protocol_accepts_autonoesis_shaped_model() -> None:
    assert isinstance(FakeSelfModel(), SelfModelLike)


def test_meta_awareness_protocol_accepts_autonoesis_shaped_state() -> None:
    assert isinstance(FakeMetaAwareness(), MetaAwarenessLike)


def test_feeling_protocol_accepts_autonoesis_shaped_feeling() -> None:
    assert isinstance(FakeFeeling(), MetacognitiveFeelingLike)


def test_self_model_to_context_preserves_phenomenology_fields() -> None:
    context = self_model_to_context(FakeSelfModel())

    assert context["subject_id"] == "agent"
    assert context["revision"] == 7
    assert context["phenomenal"]["salience"] == 0.7
    assert context["phenomenal"]["transparency"] == "partly_opaque"
    assert context["agency"]["confidence"] == 0.8
    assert context["ownership"]["alienation"] == 0.2
    assert context["boundary"]["self_world_separation"] == 0.9
    assert context["perspective"]["embodied_anchor"] == "breath"
    assert context["meta"]["introspective_access"] == 0.72


def test_meta_awareness_to_signal_uses_opacity_as_value() -> None:
    signal = meta_awareness_to_signal(FakeMetaAwareness())

    assert isinstance(signal, MetaCogSignal)
    assert signal.name == "autonoesis.meta_awareness"
    assert signal.value == 0.25
    assert signal.confidence == 0.75
    assert signal.metadata["cycle_state"] == "aware_of_distraction"
    assert signal.metadata["prior_type"] == "L"


def test_metacognitive_feeling_to_signal_uses_intensity_and_precision() -> None:
    signal = metacognitive_feeling_to_signal(FakeFeeling())

    assert signal.name == "autonoesis.metacognitive_feeling"
    assert signal.value == 0.8
    assert signal.confidence == 0.7
    assert signal.metadata["feeling_type"] == "feeling_of_error"
    assert signal.metadata["valence"] == "-0.4"
    assert signal.metadata["opacity_impact"] == "0.3"


def test_enrich_payload_with_self_model_adds_autonoesis_context() -> None:
    payload = MetaCogPayload.from_signal(
        MetaCogSignal(
            name="attractor_control",
            value=0.4,
            source="test",
            metadata={"policy": "hold"},
        ),
        payload_type="metacog.attractor_assessment",
        context={"basin_id": "focused-basin"},
    )

    enriched = enrich_payload_with_self_model(
        payload,
        self_model=FakeSelfModel(),
        meta_awareness=FakeMetaAwareness(),
        feelings=(FakeFeeling(),),
    )

    assert enriched is not payload
    assert enriched.context["basin_id"] == "focused-basin"
    assert enriched.context["autonoesis_self_model"]["subject_id"] == "agent"
    assert enriched.context["autonoesis_meta_awareness"]["opacity_level"] == 0.25
    assert (
        enriched.context["autonoesis_feelings"][0]["feeling_type"]
        == "feeling_of_error"
    )
    assert payload.context == {"basin_id": "focused-basin"}
