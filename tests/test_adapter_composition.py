import sys
from dataclasses import dataclass, field

from dionysus_metacog.adapters.autonoesis import enrich_payload_with_self_model
from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.linoss import linoss_filter_to_pomdp_record
from dionysus_metacog.adapters.sakshi import meta_payload_to_write_guard_payload


@dataclass
class FakeThoughtSeed:
    id: str = "seed-1"
    content: str = "Protect source attribution"
    activation_level: float = 0.72
    layer: str = "metacognitive"
    blanket_tag: str = "internal"
    dominant_basin: str | None = "source-risk"
    source_id: str | None = "conversation"


@dataclass
class FakeEfeResult:
    hidden_state: str = "source-risk"
    observation: str = "unlicensed-code-reference"
    policy: str = "stabilize"
    expected_free_energy: float = 0.76
    precision: float = 0.62


@dataclass
class FakePhenomenalState:
    salience: float = 0.6
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
    confidence: float = 0.7
    continuity: float = 0.8
    source_alignment: float = 0.6
    alienation: float = 0.2


@dataclass
class FakeBoundary:
    self_world_separation: float = 0.9
    tool_incorporation: float = 0.2
    social_permeability: float = 0.1


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
    revision: int = 1


def test_optional_adapters_do_not_import_adjacent_packages() -> None:
    assert "autonoesis" not in sys.modules
    assert "elume" not in sys.modules
    assert "linoss_dynamics" not in sys.modules
    assert "sakshi" not in sys.modules


def test_full_adapter_pipeline_composes_without_hard_dependencies() -> None:
    assessment = thoughtseed_winner_to_assessment(
        FakeThoughtSeed(),
        FakeEfeResult(),
        source_ids=("elume-thought-competition",),
    )
    payload = assessment.to_payload()
    enriched = enrich_payload_with_self_model(payload, self_model=FakeSelfModel())
    guard_payload = meta_payload_to_write_guard_payload(enriched)

    assert enriched.context["autonoesis_self_model"]["subject_id"] == "agent"
    assert guard_payload["requires_guard"] is True
    assert guard_payload["control_action"]["action_type"] == "REPLACE_MODULE"
    assert guard_payload["payload"]["context"]["basin_id"] == "source-risk"


def test_linoss_filter_output_can_supply_model_for_elume_like_assessment() -> None:
    model = linoss_filter_to_pomdp_record(
        {
            "m_f": [[0.1, 0.3], [0.4, 0.6]],
            "P_f": [
                [[0.5, 0.0], [0.0, 0.5]],
                [[0.2, 0.0], [0.0, 0.2]],
            ],
            "loglik": -1.5,
        },
        hidden_state="source-risk",
        observation="trajectory-observation",
        policy="stabilize",
    )

    assessment = thoughtseed_winner_to_assessment(
        FakeThoughtSeed(),
        model,
        source_ids=("linoss-filtered-elume-competition",),
    )

    assert assessment.model.metadata["adapter"] == "linoss-dynamics"
    assert assessment.free_energy_proxy == 1.75
    assert assessment.to_payload().signal.metadata["policy"] == "escalate"
