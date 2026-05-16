import sys

from fixtures.adapter_contracts import (
    CompatibleEfeResult,
    CompatibleSelfModel,
    CompatibleThoughtSeed,
    compatible_linoss_filter_result,
)

from dionysus_metacog.adapters.autonoesis import enrich_payload_with_self_model
from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.linoss import linoss_filter_to_pomdp_record
from dionysus_metacog.adapters.sakshi import meta_payload_to_write_guard_payload


def test_optional_adapters_do_not_import_adjacent_packages() -> None:
    assert "autonoesis" not in sys.modules
    assert "elume" not in sys.modules
    assert "linoss_dynamics" not in sys.modules
    assert "sakshi" not in sys.modules


def test_full_adapter_pipeline_composes_without_hard_dependencies() -> None:
    assessment = thoughtseed_winner_to_assessment(
        CompatibleThoughtSeed(),
        CompatibleEfeResult(),
        source_ids=("elume-thought-competition",),
    )
    payload = assessment.to_payload()
    enriched = enrich_payload_with_self_model(
        payload,
        self_model=CompatibleSelfModel(subject_id="agent"),
    )
    guard_payload = meta_payload_to_write_guard_payload(enriched)

    assert enriched.context["autonoesis_self_model"]["subject_id"] == "agent"
    assert guard_payload["requires_guard"] is True
    assert guard_payload["control_action"]["action_type"] == "REPLACE_MODULE"
    assert guard_payload["payload"]["context"]["basin_id"] == "source-risk"


def test_linoss_filter_output_can_supply_model_for_elume_like_assessment() -> None:
    model = linoss_filter_to_pomdp_record(
        compatible_linoss_filter_result(),
        hidden_state="source-risk",
        observation="trajectory-observation",
        policy="stabilize",
    )

    assessment = thoughtseed_winner_to_assessment(
        CompatibleThoughtSeed(),
        model,
        source_ids=("linoss-filtered-elume-competition",),
    )

    assert assessment.model.metadata["adapter"] == "linoss-dynamics"
    assert assessment.free_energy_proxy == 3.0
    assert assessment.to_payload().signal.metadata["policy"] == "escalate"
