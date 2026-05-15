from dionysus_metacog.attractors import (
    AttractorAssessment,
    AttractorBasin,
    AttractorControlPolicy,
    default_attractor_sources,
)
from dionysus_metacog.models import PomdpStateRecord


def test_stable_low_free_energy_basin_holds_policy() -> None:
    basin = AttractorBasin(
        basin_id="focused_attention",
        attractor_label="focused attention",
        depth=0.8,
        width=0.6,
        stability=0.9,
        sources=(default_attractor_sources()["friston-2014-cognitive-dynamics"],),
    )
    pomdp = PomdpStateRecord(
        hidden_state="focused",
        observation="task_stable",
        policy="continue",
        expected_free_energy=0.1,
        precision=0.9,
    )

    assessment = AttractorAssessment.from_basin(basin=basin, model=pomdp)

    assert assessment.policy == AttractorControlPolicy.HOLD
    assert assessment.free_energy_proxy == 0.11
    assert assessment.to_signal().metadata["policy"] == "hold"


def test_unstable_high_free_energy_basin_requests_stabilization() -> None:
    basin = AttractorBasin(
        basin_id="fragmented_attention",
        attractor_label="fragmented attention",
        depth=0.2,
        width=0.9,
        stability=0.2,
        sources=(default_attractor_sources()["friston-2014-cognitive-dynamics"],),
    )
    pomdp = PomdpStateRecord(
        hidden_state="unsettled",
        observation="goal_switching",
        policy="reduce_uncertainty",
        expected_free_energy=0.9,
        precision=0.3,
    )

    assessment = AttractorAssessment.from_basin(basin=basin, model=pomdp)

    assert assessment.policy == AttractorControlPolicy.ESCALATE
    assert assessment.to_signal().name == "attractor_control"
    assert assessment.to_signal().confidence == 0.3


def test_high_novelty_basin_requests_exploration() -> None:
    basin = AttractorBasin(
        basin_id="novel_pattern",
        attractor_label="novel pattern",
        depth=0.6,
        width=0.7,
        stability=0.5,
        sources=(default_attractor_sources()["spisak-friston-fep-attractor-network"],),
    )
    state = basin.as_state()
    model = PomdpStateRecord(
        hidden_state="uncertain",
        observation="unexpected_regularities",
        policy="sample",
        expected_free_energy=0.4,
        precision=0.6,
    )

    assessment = AttractorAssessment.from_state(
        state=state,
        model=model,
        source_ids=basin.source_ids,
        novelty=0.8,
    )

    assert assessment.policy == AttractorControlPolicy.EXPLORE
    assert assessment.to_signal().metadata["source_ids"] == (
        "spisak-friston-fep-attractor-network"
    )
