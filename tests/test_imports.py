from dionysus_metacog import (
    AttractorAssessment,
    AttractorTransition,
    MetaCogPayload,
    ProvenanceLedger,
    __version__,
)
from dionysus_metacog.adapters.hermes import HERMES_AGENT_ADAPTER_NAME
from dionysus_metacog.attractors import AttractorControlPolicy, AttractorState
from dionysus_metacog.core import MetaCogSignal, MetaCogTrace, PromotionLabel
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord
from dionysus_metacog.provenance import SourceReference


def test_import_root_version() -> None:
    assert __version__ == "0.2.0"
    assert AttractorAssessment.__name__ == "AttractorAssessment"
    assert AttractorTransition.__name__ == "AttractorTransition"
    assert MetaCogPayload.__name__ == "MetaCogPayload"
    assert ProvenanceLedger.__name__ == "ProvenanceLedger"


def test_core_records() -> None:
    signal = MetaCogSignal(name="meta_awareness", value=1.0, source="test")
    trace = MetaCogTrace(signal=signal, label=PromotionLabel.SHAREABLE)

    assert trace.shareable is True


def test_model_records() -> None:
    pomdp = PomdpStateRecord(
        hidden_state="focused",
        observation="task_stable",
        policy="stay",
        precision=0.9,
    )
    blanket = MarkovBlanketRecord(
        internal_states=["belief"],
        external_states=["task"],
        sensory_states=["observation"],
        active_states=["policy"],
    )

    assert pomdp.policy == "stay"
    assert blanket.active_states == ["policy"]


def test_adapter_and_provenance_records() -> None:
    state = AttractorState(basin_id="focused", stability=0.8)
    source = SourceReference(
        source_id="sandved-smith-2021",
        title="Towards a computational phenomenology of mental action",
        locator="Figure 6",
    )

    assert HERMES_AGENT_ADAPTER_NAME == "dionysus-metacog"
    assert AttractorControlPolicy.HOLD == "hold"
    assert AttractorControlPolicy.ATTENUATE == "attenuate"
    assert state.basin_id == "focused"
    assert source.locator == "Figure 6"


def test_optional_adapter_modules_import_without_adjacent_packages() -> None:
    from dionysus_metacog.adapters import autonoesis, elume, linoss, sakshi

    assert autonoesis.SelfModelLike.__name__ == "SelfModelLike"
    assert elume.ThoughtSeedLike.__name__ == "ThoughtSeedLike"
    assert linoss.linoss_metrics_to_attractor_state.__name__ == (
        "linoss_metrics_to_attractor_state"
    )
    assert sakshi.meta_payload_to_control_action.__name__ == (
        "meta_payload_to_control_action"
    )
