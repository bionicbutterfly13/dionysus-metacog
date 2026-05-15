"""Optional linoss-dynamics adapter helpers.

The adapter accepts plain dictionaries shaped like linoss-dynamics outputs and
converts them into Dionysus Metacognition records. It does not import
linoss-dynamics at module import time.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from dionysus_metacog.attractors import AttractorState
from dionysus_metacog.models import PomdpStateRecord

_ADAPTER_NAME = "linoss-dynamics"


def linoss_metrics_to_attractor_state(
    metrics: Mapping[str, Any],
    *,
    basin_id: str,
) -> AttractorState:
    """Convert linoss energy/convergence metrics into an attractor state."""

    delta_energy = _energy_delta(metrics)
    if delta_energy <= 0.0:
        stability = _clamp_unit(abs(delta_energy))
        novelty = 0.0
    else:
        stability = _clamp_unit(1.0 - delta_energy)
        novelty = _clamp_unit(delta_energy)

    metadata = {
        "adapter": _ADAPTER_NAME,
        "energy_before": _format_number(metrics.get("energy_before")),
        "energy_after": _format_number(metrics.get("energy_after")),
        "delta_energy": _format_number(delta_energy),
    }
    for key in ("mode", "damping_mode"):
        if key in metrics:
            metadata[key] = str(metrics[key])

    return AttractorState(
        basin_id=basin_id,
        stability=stability,
        novelty=novelty,
        metadata=metadata,
    )


def linoss_stability_to_attractor_state(
    *,
    stable: bool,
    reason: str,
    basin_id: str,
) -> AttractorState:
    """Convert a linoss stability check into an attractor state."""

    return AttractorState(
        basin_id=basin_id,
        stability=1.0 if stable else 0.0,
        novelty=0.0 if stable else 1.0,
        metadata={
            "adapter": _ADAPTER_NAME,
            "stable": str(stable),
            "stability_reason": reason,
        },
    )


def linoss_filter_to_pomdp_record(
    filter_result: Mapping[str, Any],
    *,
    hidden_state: str,
    observation: str,
    policy: str,
) -> PomdpStateRecord:
    """Convert linoss filter output into a POMDP-style state record."""

    state_mean = _last_vector(filter_result.get("m_f"))
    covariance_trace = _last_covariance_trace(filter_result.get("P_f"))
    precision = _precision_from_covariance_trace(
        covariance_trace=covariance_trace,
        dimensions=len(state_mean),
    )

    return PomdpStateRecord(
        hidden_state=hidden_state,
        observation=observation,
        policy=policy,
        expected_free_energy=abs(float(filter_result.get("loglik", 0.0) or 0.0)),
        precision=precision,
        metadata={
            "adapter": _ADAPTER_NAME,
            "state_mean": ",".join(_format_number(value) for value in state_mean),
            "state_covariance_trace": (
                "" if covariance_trace is None else _format_number(covariance_trace)
            ),
        },
    )


def _energy_delta(metrics: Mapping[str, Any]) -> float:
    if "delta_energy" in metrics:
        return float(metrics["delta_energy"])
    before = float(metrics.get("energy_before", 0.0) or 0.0)
    after = float(metrics.get("energy_after", before) or before)
    return after - before


def _last_vector(value: Any) -> tuple[float, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    if not value:
        return ()
    last = value[-1]
    if isinstance(last, Sequence) and not isinstance(last, (str, bytes)):
        return tuple(float(item) for item in last)
    return (float(last),)


def _last_covariance_trace(value: Any) -> float | None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return None
    if not value:
        return None
    last = value[-1]
    if not isinstance(last, Sequence) or isinstance(last, (str, bytes)):
        return float(last)
    trace = 0.0
    for index, row in enumerate(last):
        if isinstance(row, Sequence) and not isinstance(row, (str, bytes)):
            if index < len(row):
                trace += float(row[index])
        elif index == 0:
            trace += float(row)
    return trace


def _precision_from_covariance_trace(
    *,
    covariance_trace: float | None,
    dimensions: int,
) -> float | None:
    if covariance_trace is None or dimensions <= 0:
        return None
    mean_variance = max(0.0, covariance_trace) / dimensions
    return round(1.0 / (1.0 + mean_variance), 6)


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, float(value)))


def _format_number(value: Any) -> str:
    if value is None:
        return ""
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


__all__ = [
    "linoss_filter_to_pomdp_record",
    "linoss_metrics_to_attractor_state",
    "linoss_stability_to_attractor_state",
]
