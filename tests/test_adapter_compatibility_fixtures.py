import sys

from fixtures.adapter_contracts import (
    CompatibleEfeResult,
    CompatibleMetaAwareness,
    CompatibleMetacognitiveFeeling,
    CompatibleSelfModel,
    CompatibleThoughtSeed,
    compatible_linoss_filter_result,
    compatible_linoss_metrics,
)

from dionysus_metacog.adapters.autonoesis import (
    MetaAwarenessLike,
    MetacognitiveFeelingLike,
    SelfModelLike,
    enrich_payload_with_self_model,
)
from dionysus_metacog.adapters.elume import (
    EFEResultLike,
    ThoughtSeedLike,
    thoughtseed_winner_to_assessment,
)
from dionysus_metacog.adapters.linoss import (
    linoss_filter_to_pomdp_record,
    linoss_metrics_to_attractor_state,
)
from dionysus_metacog.adapters.sakshi import (
    meta_payload_to_write_guard_payload,
    signal_to_np_state_snapshot,
)
from dionysus_metacog.core import (
    InProcessMetaCogDispatcher,
    MetaCogPayload,
)


class RecordingPayloadHandler:
    def __init__(self) -> None:
        self.received: list[MetaCogPayload] = []

    def handle(self, payload: MetaCogPayload) -> None:
        self.received.append(payload)


def test_fixture_shapes_satisfy_adapter_protocols() -> None:
    assert isinstance(CompatibleThoughtSeed(), ThoughtSeedLike)
    assert isinstance(CompatibleEfeResult(), EFEResultLike)
    assert isinstance(CompatibleSelfModel(), SelfModelLike)
    assert isinstance(CompatibleMetaAwareness(), MetaAwarenessLike)
    assert isinstance(CompatibleMetacognitiveFeeling(), MetacognitiveFeelingLike)


def test_fixtures_convert_across_all_optional_adapters() -> None:
    thoughtseed = CompatibleThoughtSeed()
    assessment = thoughtseed_winner_to_assessment(
        thoughtseed,
        CompatibleEfeResult(),
        source_ids=("compatibility-fixture",),
    )
    payload = assessment.to_payload()
    payload.signal.metadata["thoughtseed_id"] = thoughtseed.id

    enriched = enrich_payload_with_self_model(
        payload,
        self_model=CompatibleSelfModel(),
        meta_awareness=CompatibleMetaAwareness(),
        feelings=(CompatibleMetacognitiveFeeling(),),
    )
    guard_payload = meta_payload_to_write_guard_payload(enriched)
    snapshot = signal_to_np_state_snapshot(enriched.signal)

    assert enriched.context["basin_id"] == "source-risk"
    assert enriched.context["autonoesis_self_model"]["subject_id"] == "agent-runtime"
    assert guard_payload["requires_guard"] is True
    assert guard_payload["control_action"]["target"] == "source-risk"
    assert snapshot["dominant_thoughtseed_id"] == "seed-source-risk"


def test_linoss_fixtures_remain_compatible_with_attractor_and_model_inputs() -> None:
    state = linoss_metrics_to_attractor_state(
        compatible_linoss_metrics(),
        basin_id="trajectory-basin",
    )
    model = linoss_filter_to_pomdp_record(
        compatible_linoss_filter_result(),
        hidden_state="trajectory-basin",
        observation="filtered-latent-state",
        policy="stabilize",
    )

    assessment = thoughtseed_winner_to_assessment(
        CompatibleThoughtSeed(dominant_basin=state.basin_id),
        model,
        source_ids=("linoss-filtered-compatibility-fixture",),
    )

    assert state.metadata["adapter"] == "linoss-dynamics"
    assert model.metadata["adapter"] == "linoss-dynamics"
    assert assessment.state.basin_id == "trajectory-basin"
    assert assessment.model.metadata["state_mean"] == "0.6,0.8"


def test_fixture_payload_can_dispatch_to_host_handler() -> None:
    assessment = thoughtseed_winner_to_assessment(
        CompatibleThoughtSeed(),
        CompatibleEfeResult(),
        source_ids=("dispatch-compatibility-fixture",),
    )
    payload = assessment.to_payload()
    handler = RecordingPayloadHandler()

    result = InProcessMetaCogDispatcher(handlers=(handler,)).dispatch(payload)

    assert result.success is True
    assert result.delivered == 1
    assert handler.received == [payload]


def test_compatibility_fixtures_keep_adjacent_packages_optional() -> None:
    assert "autonoesis" not in sys.modules
    assert "elume" not in sys.modules
    assert "linoss_dynamics" not in sys.modules
    assert "sakshi" not in sys.modules
