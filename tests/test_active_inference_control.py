from dionysus_metacog.attractors import (
    AttractorAssessment,
    AttractorBasin,
    AttractorControlPolicy,
    AttractorState,
    default_attractor_sources,
)
from dionysus_metacog.models import PomdpStateRecord


def test_low_precision_amplifies_free_energy_proxy_and_escalates() -> None:
    basin = AttractorBasin(
        basin_id="unstable_attention",
        attractor_label="unstable attention",
        depth=0.3,
        width=0.9,
        stability=0.45,
        sources=(default_attractor_sources()["friston-2014-cognitive-dynamics"],),
    )
    model = PomdpStateRecord(
        hidden_state="uncertain",
        observation="ambiguous_goal",
        policy="reduce_uncertainty",
        expected_free_energy=0.7,
        precision=0.2,
    )

    assessment = AttractorAssessment.from_basin(basin=basin, model=model)
    signal = assessment.to_signal()

    assert assessment.free_energy_proxy == 1.26
    assert assessment.policy == AttractorControlPolicy.ESCALATE
    assert signal.value == 1.26
    assert signal.metadata["expected_free_energy"] == "0.7"
    assert signal.metadata["precision"] == "0.2"
    assert signal.metadata["free_energy_proxy"] == "1.26"


def test_high_precision_high_novelty_requests_attenuation() -> None:
    state = AttractorState(
        basin_id="salient_novelty",
        stability=0.75,
        novelty=0.9,
    )
    model = PomdpStateRecord(
        hidden_state="salient",
        observation="precise_novel_pattern",
        policy="attenuate_salience",
        expected_free_energy=0.3,
        precision=0.9,
    )

    assessment = AttractorAssessment.from_state(
        state=state,
        model=model,
        source_ids=("spisak-friston-fep-attractor-network",),
    )

    assert assessment.free_energy_proxy == 0.33
    assert assessment.policy == AttractorControlPolicy.ATTENUATE


def test_mid_precision_state_proxy_is_precision_weighted() -> None:
    state = AttractorState(
        basin_id="uncertain_basin",
        stability=0.6,
        novelty=0.2,
    )
    model = PomdpStateRecord(
        hidden_state="uncertain",
        observation="partial_signal",
        policy="sample",
        precision=0.5,
    )

    assessment = AttractorAssessment.from_state(
        state=state,
        model=model,
        source_ids=("friston-2014-cognitive-dynamics",),
    )

    assert assessment.free_energy_proxy == 0.9
    assert assessment.policy == AttractorControlPolicy.STABILIZE
