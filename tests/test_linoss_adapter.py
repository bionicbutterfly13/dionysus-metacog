from dionysus_metacog.adapters.linoss import (
    linoss_filter_to_pomdp_record,
    linoss_metrics_to_attractor_state,
    linoss_stability_to_attractor_state,
)
from dionysus_metacog.attractors import AttractorState
from dionysus_metacog.models import PomdpStateRecord


def test_linoss_metrics_to_attractor_state_maps_energy_delta_to_stability() -> None:
    metrics = {
        "energy_before": 1.0,
        "energy_after": 0.25,
        "delta_energy": -0.75,
        "mode": "implicit",
        "damping_mode": "explicit_g",
    }

    state = linoss_metrics_to_attractor_state(
        metrics,
        basin_id="trajectory-basin",
    )

    assert isinstance(state, AttractorState)
    assert state.basin_id == "trajectory-basin"
    assert state.stability == 0.75
    assert state.novelty == 0.0
    assert state.metadata["adapter"] == "linoss-dynamics"
    assert state.metadata["energy_before"] == "1"
    assert state.metadata["energy_after"] == "0.25"
    assert state.metadata["delta_energy"] == "-0.75"
    assert state.metadata["mode"] == "implicit"
    assert state.metadata["damping_mode"] == "explicit_g"


def test_linoss_metrics_to_attractor_state_maps_energy_gain_to_novelty() -> None:
    metrics = {
        "energy_before": 0.5,
        "energy_after": 0.9,
        "delta_energy": 0.4,
    }

    state = linoss_metrics_to_attractor_state(metrics, basin_id="moving-basin")

    assert state.stability == 0.6
    assert state.novelty == 0.4


def test_linoss_stability_to_attractor_state_records_reason() -> None:
    state = linoss_stability_to_attractor_state(
        stable=True,
        reason="implicit mode: A >= 0 and G >= 0",
        basin_id="stable-basin",
    )

    assert isinstance(state, AttractorState)
    assert state.basin_id == "stable-basin"
    assert state.stability == 1.0
    assert state.novelty == 0.0
    assert state.metadata["stability_reason"] == "implicit mode: A >= 0 and G >= 0"


def test_linoss_stability_to_attractor_state_marks_unstable_as_novel() -> None:
    state = linoss_stability_to_attractor_state(
        stable=False,
        reason="IMEX CFL condition violated",
        basin_id="unstable-basin",
    )

    assert state.stability == 0.0
    assert state.novelty == 1.0


def test_linoss_filter_to_pomdp_record_uses_loglik_as_expected_free_energy() -> None:
    filt = {
        "m_f": [[0.2, 0.4], [0.6, 0.8]],
        "P_f": [
            [[0.5, 0.0], [0.0, 0.5]],
            [[0.25, 0.0], [0.0, 0.25]],
        ],
        "loglik": -2.5,
    }

    model = linoss_filter_to_pomdp_record(
        filt,
        hidden_state="basin_latent_state",
        observation="trajectory_observation",
        policy="stabilize",
    )

    assert isinstance(model, PomdpStateRecord)
    assert model.hidden_state == "basin_latent_state"
    assert model.observation == "trajectory_observation"
    assert model.policy == "stabilize"
    assert model.expected_free_energy == 2.5
    assert model.precision == 0.8
    assert model.metadata["adapter"] == "linoss-dynamics"
    assert model.metadata["state_mean"] == "0.6,0.8"
    assert model.metadata["state_covariance_trace"] == "0.5"


def test_linoss_filter_to_pomdp_record_handles_missing_covariance() -> None:
    filt = {
        "m_f": [[0.1]],
        "loglik": 0.0,
    }

    model = linoss_filter_to_pomdp_record(
        filt,
        hidden_state="latent",
        observation="obs",
        policy="hold",
    )

    assert model.expected_free_energy == 0.0
    assert model.precision is None
    assert model.metadata["state_covariance_trace"] == ""
