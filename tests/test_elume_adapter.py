from dataclasses import dataclass

from dionysus_metacog.adapters.elume import (
    ThoughtSeedLike,
    efe_result_to_pomdp_record,
    thoughtseed_to_attractor_state,
    thoughtseed_to_markov_blanket,
    thoughtseed_winner_to_assessment,
)
from dionysus_metacog.attractors import (
    AttractorControlPolicy,
    AttractorState,
)
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord


@dataclass
class FakeElumeThoughtSeed:
    id: str
    content: str
    activation_level: float
    layer: str
    blanket_tag: str
    dominant_basin: str | None
    source_id: str | None


@dataclass
class FakeElumeEfeResult:
    hidden_state: str
    observation: str
    policy: str
    expected_free_energy: float
    precision: float


def test_thoughtseed_protocol_accepts_elume_shaped_seed() -> None:
    seed = FakeElumeThoughtSeed(
        id="seed-1",
        content="Protect source attribution",
        activation_level=0.86,
        layer="metacognitive",
        blanket_tag="internal",
        dominant_basin="provenance-basin",
        source_id="paper:thoughtseeds",
    )

    assert isinstance(seed, ThoughtSeedLike)


def test_thoughtseed_to_attractor_state_uses_basin_and_salience() -> None:
    seed = FakeElumeThoughtSeed(
        id="seed-1",
        content="Protect source attribution",
        activation_level=0.86,
        layer="metacognitive",
        blanket_tag="internal",
        dominant_basin="provenance-basin",
        source_id="paper:thoughtseeds",
    )

    state = thoughtseed_to_attractor_state(seed)

    assert isinstance(state, AttractorState)
    assert state.basin_id == "provenance-basin"
    assert state.stability == 0.86
    assert state.metadata["thoughtseed_id"] == "seed-1"
    assert state.metadata["content"] == "Protect source attribution"
    assert state.metadata["layer"] == "metacognitive"
    assert state.metadata["blanket_tag"] == "internal"
    assert state.metadata["source_id"] == "paper:thoughtseeds"


def test_thoughtseed_to_attractor_state_falls_back_to_unassigned_basin() -> None:
    seed = FakeElumeThoughtSeed(
        id="seed-2",
        content="Explore competing idea",
        activation_level=1.4,
        layer="conceptual",
        blanket_tag="sensory",
        dominant_basin=None,
        source_id=None,
    )

    state = thoughtseed_to_attractor_state(seed)

    assert state.basin_id == "unassigned-thoughtseed-basin"
    assert state.stability == 1.0
    assert state.metadata["source_id"] == ""


def test_efe_result_to_pomdp_record_maps_expected_free_energy() -> None:
    result = FakeElumeEfeResult(
        hidden_state="source_risk",
        observation="unlicensed_code_reference",
        policy="attenuate",
        expected_free_energy=0.42,
        precision=0.8,
    )

    model = efe_result_to_pomdp_record(result)

    assert isinstance(model, PomdpStateRecord)
    assert model.hidden_state == "source_risk"
    assert model.observation == "unlicensed_code_reference"
    assert model.policy == "attenuate"
    assert model.expected_free_energy == 0.42
    assert model.precision == 0.8
    assert model.metadata["adapter"] == "elume"


def test_thoughtseed_to_markov_blanket_groups_by_blanket_tag() -> None:
    seed = FakeElumeThoughtSeed(
        id="seed-3",
        content="Attend to the user correction",
        activation_level=0.7,
        layer="perceptual",
        blanket_tag="sensory",
        dominant_basin="attention-basin",
        source_id="conversation",
    )

    blanket = thoughtseed_to_markov_blanket(seed)

    assert isinstance(blanket, MarkovBlanketRecord)
    assert blanket.sensory_states == ("seed-3",)
    assert blanket.internal_states == ("attention-basin",)
    assert blanket.external_states == ("conversation",)
    assert blanket.active_states == ("perceptual",)
    assert blanket.metadata["blanket_tag"] == "sensory"


def test_thoughtseed_winner_to_assessment_builds_control_payload_input() -> None:
    seed = FakeElumeThoughtSeed(
        id="seed-4",
        content="High novelty hypothesis",
        activation_level=0.3,
        layer="abstract",
        blanket_tag="internal",
        dominant_basin="hypothesis-basin",
        source_id="elume:round-1",
    )
    result = FakeElumeEfeResult(
        hidden_state="hypothesis",
        observation="novel_but_unstable",
        policy="explore",
        expected_free_energy=0.6,
        precision=0.7,
    )

    assessment = thoughtseed_winner_to_assessment(
        seed,
        result,
        source_ids=("elume-thought-competition",),
    )

    assert assessment.state.basin_id == "hypothesis-basin"
    assert assessment.model.hidden_state == "hypothesis"
    assert assessment.source_ids == ("elume-thought-competition",)
    assert assessment.policy == AttractorControlPolicy.STABILIZE
    payload = assessment.to_payload()
    assert payload.payload_type == "metacog.attractor_assessment"
