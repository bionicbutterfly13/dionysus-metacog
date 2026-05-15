"""Optional Sakshi adapter helpers.

The adapter emits Sakshi-compatible dictionaries without importing Sakshi at
module import time.
"""

from dionysus_metacog.core import MetaCogPayload, MetaCogSignal

CONTROL_ACTION_TYPE_BY_POLICY = {
    "hold": "STRENGTHEN_MODULE",
    "stabilize": "ADJUST_PRECISION",
    "explore": "STRENGTHEN_MODULE",
    "attenuate": "SUPPRESS_MODULE",
    "escalate": "REPLACE_MODULE",
}

DEFAULT_SOURCE_ORIGIN = "dionysus-metacognition"


def meta_payload_to_control_action(payload: MetaCogPayload) -> dict[str, object]:
    """Convert a MetaCogPayload into a Sakshi-style ControlAction payload."""

    signal = payload.signal
    policy = _policy(signal)
    free_energy = _float_metadata(signal, "free_energy_proxy", default=signal.value)
    precision = _float_metadata(signal, "precision", default=1.0)
    return {
        "action_type": CONTROL_ACTION_TYPE_BY_POLICY.get(
            policy,
            "ADJUST_PRECISION",
        ),
        "target": _target(signal),
        "magnitude": free_energy,
        "rationale": _rationale(signal),
        "precision_delta": _precision_delta(policy=policy, precision=precision),
    }


def signal_to_witness_event(
    signal: MetaCogSignal,
    *,
    event_type: str = "dionysus.metacog.control",
    source_origin: str = DEFAULT_SOURCE_ORIGIN,
) -> dict[str, object]:
    """Convert a signal into a Sakshi EventBus-compatible event wrapper."""

    policy = _policy(signal)
    return {
        "event_type": event_type,
        "source_origin": source_origin,
        "payload": {
            "signal_name": signal.name,
            "signal_source": signal.source,
            "value": signal.value,
            "confidence": signal.confidence,
            "policy": policy,
            "basin_id": _target(signal),
            "requires_guard": _requires_guard(policy),
            "metadata": dict(signal.metadata),
        },
    }


def meta_payload_to_write_guard_payload(
    payload: MetaCogPayload,
    *,
    source_origin: str = DEFAULT_SOURCE_ORIGIN,
) -> dict[str, object]:
    """Wrap a payload for a Sakshi WriteGuard check."""

    policy = _policy(payload.signal)
    return {
        "source_origin": source_origin,
        "payload_type": payload.payload_type,
        "requires_guard": _requires_guard(policy),
        "control_action": meta_payload_to_control_action(payload),
        "payload": payload.as_dict(),
    }


def signal_to_np_state_snapshot(signal: MetaCogSignal) -> dict[str, str]:
    """Convert signal metadata into a Sakshi NPStateSnapshot-compatible dict."""

    thoughtseed_id = signal.metadata.get("thoughtseed_id") or _target(signal)
    return {
        "dominant_thoughtseed_id": str(thoughtseed_id),
        "np_state": str(signal.metadata.get("np_state") or "Dominant"),
        "prior_type": str(signal.metadata.get("prior_type") or "λ"),
    }


def _policy(signal: MetaCogSignal) -> str:
    return str(signal.metadata.get("policy") or "")


def _target(signal: MetaCogSignal) -> str:
    return str(signal.metadata.get("basin_id") or signal.name)


def _rationale(signal: MetaCogSignal) -> str:
    hidden_state = signal.metadata.get("hidden_state", "unknown")
    observation = signal.metadata.get("observation", "unknown")
    policy = _policy(signal)
    free_energy = signal.metadata.get("free_energy_proxy", str(signal.value))
    return (
        f"{policy} requested for hidden_state={hidden_state}, "
        f"observation={observation}, free_energy_proxy={free_energy}"
    )


def _float_metadata(
    signal: MetaCogSignal,
    key: str,
    *,
    default: float,
) -> float:
    try:
        return float(signal.metadata.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _precision_delta(*, policy: str, precision: float) -> float | None:
    if policy != "stabilize":
        return None
    return round(1.0 - min(1.0, max(0.0, precision)), 6)


def _requires_guard(policy: str) -> bool:
    return policy in {"attenuate", "escalate", "stabilize"}


__all__ = [
    "CONTROL_ACTION_TYPE_BY_POLICY",
    "DEFAULT_SOURCE_ORIGIN",
    "meta_payload_to_control_action",
    "meta_payload_to_write_guard_payload",
    "signal_to_np_state_snapshot",
    "signal_to_witness_event",
]
