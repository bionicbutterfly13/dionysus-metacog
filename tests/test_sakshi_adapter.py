from dionysus_metacog.adapters.sakshi import (
    CONTROL_ACTION_TYPE_BY_POLICY,
    meta_payload_to_control_action,
    meta_payload_to_write_guard_payload,
    signal_to_np_state_snapshot,
    signal_to_witness_event,
)
from dionysus_metacog.attractors import AttractorAssessment, AttractorBasin
from dionysus_metacog.models import PomdpStateRecord
from dionysus_metacog.provenance import SourceReference


def _payload(policy: str = "stabilize"):
    source = SourceReference(
        source_id="test-source",
        title="Test Source",
        locator="fixture",
    )
    basin = AttractorBasin(
        basin_id="source-risk",
        attractor_label="source risk",
        depth=0.7,
        width=0.4,
        stability=0.3,
        sources=(source,),
    )
    model = PomdpStateRecord(
        hidden_state="license-risk",
        observation="unlicensed-code-reference",
        policy=policy,
        expected_free_energy=0.76,
        precision=0.62,
    )
    payload = AttractorAssessment.from_basin(basin=basin, model=model).to_payload()
    payload.signal.metadata["policy"] = policy
    return payload


def test_meta_payload_to_control_action_maps_policy_to_sakshi_type() -> None:
    payload = _payload(policy="stabilize")

    action = meta_payload_to_control_action(payload)

    assert action["action_type"] == "ADJUST_PRECISION"
    assert action["target"] == "source-risk"
    assert action["magnitude"] == 1.0488
    assert action["precision_delta"] == 0.38
    assert "license-risk" in action["rationale"]


def test_control_action_policy_mapping_is_explicit() -> None:
    assert CONTROL_ACTION_TYPE_BY_POLICY == {
        "hold": "STRENGTHEN_MODULE",
        "stabilize": "ADJUST_PRECISION",
        "explore": "STRENGTHEN_MODULE",
        "attenuate": "SUPPRESS_MODULE",
        "escalate": "REPLACE_MODULE",
    }


def test_signal_to_witness_event_preserves_context() -> None:
    payload = _payload(policy="escalate")
    signal = payload.signal

    event = signal_to_witness_event(signal, event_type="dionysus.metacog.signal")

    assert event["event_type"] == "dionysus.metacog.signal"
    assert event["source_origin"] == "dionysus-metacognition"
    assert event["payload"]["signal_name"] == "attractor_control"
    assert event["payload"]["policy"] == "escalate"
    assert event["payload"]["basin_id"] == "source-risk"
    assert event["payload"]["requires_guard"] is True


def test_meta_payload_to_write_guard_payload_wraps_control_action() -> None:
    payload = _payload(policy="attenuate")

    guard_payload = meta_payload_to_write_guard_payload(payload)

    assert guard_payload["source_origin"] == "dionysus-metacognition"
    assert guard_payload["payload_type"] == "metacog.attractor_assessment"
    assert guard_payload["control_action"]["action_type"] == "SUPPRESS_MODULE"
    assert guard_payload["requires_guard"] is True


def test_signal_to_np_state_snapshot_uses_dominant_thoughtseed_metadata() -> None:
    payload = _payload()
    signal = payload.signal
    signal.metadata["thoughtseed_id"] = "seed-123"
    signal.metadata["prior_type"] = "L"

    snapshot = signal_to_np_state_snapshot(signal)

    assert snapshot == {
        "dominant_thoughtseed_id": "seed-123",
        "np_state": "Dominant",
        "prior_type": "L",
    }


def test_signal_to_np_state_snapshot_uses_basin_fallback() -> None:
    payload = _payload()

    snapshot = signal_to_np_state_snapshot(payload.signal)

    assert snapshot["dominant_thoughtseed_id"] == "source-risk"
    assert snapshot["np_state"] == "Dominant"
    assert snapshot["prior_type"] == "λ"
