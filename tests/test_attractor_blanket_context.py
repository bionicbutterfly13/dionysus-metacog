from dionysus_metacog.attractors import (
    AttractorAssessment,
    AttractorBasin,
    default_attractor_sources,
)
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord


def test_assessment_signal_can_carry_markov_blanket_context() -> None:
    source = default_attractor_sources()["friston-2014-cognitive-dynamics"]
    basin = AttractorBasin(
        basin_id="focused_attention",
        attractor_label="focused attention",
        depth=0.8,
        width=0.6,
        stability=0.9,
        sources=(source,),
    )
    model = PomdpStateRecord(
        hidden_state="focused",
        observation="task_stable",
        policy="continue",
        expected_free_energy=0.1,
        precision=0.9,
    )
    blanket = MarkovBlanketRecord(
        internal_states=("belief_precision",),
        external_states=("task_demands",),
        sensory_states=("task_stable",),
        active_states=("continue",),
    )

    assessment = AttractorAssessment.from_basin(
        basin=basin,
        model=model,
        blanket=blanket,
    )
    signal = assessment.to_signal()

    assert assessment.blanket == blanket
    assert signal.metadata["internal_states"] == "belief_precision"
    assert signal.metadata["sensory_states"] == "task_stable"
    assert signal.metadata["active_states"] == "continue"
