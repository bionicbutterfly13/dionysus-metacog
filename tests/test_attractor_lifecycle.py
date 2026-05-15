import pytest

from dionysus_metacog.attractors import (
    AttractorObservation,
    AttractorState,
    AttractorTransition,
    AttractorTransitionLabel,
)


def test_first_observation_enters_basin() -> None:
    current = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.8),
        source_ids=("paper-1",),
    )

    transition = AttractorTransition.from_observations(prior=None, current=current)

    assert transition.label == AttractorTransitionLabel.ENTERED
    assert transition.prior is None
    assert transition.current == current
    assert transition.source_ids == ("paper-1",)
    assert transition.drift == 0.0


def test_stable_same_basin_is_held() -> None:
    prior = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.82),
        source_ids=("paper-1",),
    )
    current = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.8),
        source_ids=("paper-1",),
    )

    transition = AttractorTransition.from_observations(prior=prior, current=current)

    assert transition.label == AttractorTransitionLabel.HELD
    assert transition.stability_delta == pytest.approx(-0.02)
    assert transition.novelty_delta == 0.0
    assert transition.drift == pytest.approx(0.02)


def test_same_basin_stability_drop_destabilizes() -> None:
    prior = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.9),
        source_ids=("paper-1",),
    )
    current = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.35),
        source_ids=("paper-1",),
    )

    transition = AttractorTransition.from_observations(prior=prior, current=current)

    assert transition.label == AttractorTransitionLabel.DESTABILIZED
    assert transition.stability_delta == pytest.approx(-0.55)
    assert transition.drift == pytest.approx(0.55)


def test_new_basin_without_shared_sources_is_escaped() -> None:
    prior = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.8),
        source_ids=("paper-1",),
    )
    current = AttractorObservation(
        state=AttractorState(basin_id="fragmented_attention", stability=0.5),
        source_ids=("paper-2",),
    )

    transition = AttractorTransition.from_observations(prior=prior, current=current)

    assert transition.label == AttractorTransitionLabel.ESCAPED
    assert transition.source_ids == ("paper-1", "paper-2")


def test_new_basin_with_shared_sources_is_merged() -> None:
    prior = AttractorObservation(
        state=AttractorState(basin_id="focused_attention", stability=0.7),
        source_ids=("paper-1",),
    )
    current = AttractorObservation(
        state=AttractorState(basin_id="focused_flow", stability=0.72),
        source_ids=("paper-1", "paper-2"),
    )

    transition = AttractorTransition.from_observations(prior=prior, current=current)

    assert transition.label == AttractorTransitionLabel.MERGED
    assert transition.source_ids == ("paper-1", "paper-2")


def test_observation_requires_source_ids() -> None:
    with pytest.raises(ValueError, match="source_ids must not be empty"):
        AttractorObservation(
            state=AttractorState(basin_id="unbacked", stability=0.5),
            source_ids=(),
        )
