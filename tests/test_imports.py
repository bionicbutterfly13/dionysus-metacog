from dionysus_metacog import AttractorAssessment, ProvenanceLedger, __version__
from dionysus_metacog.adapters.hermes import HERMES_AGENT_ADAPTER_NAME
from dionysus_metacog.attractors import AttractorControlPolicy, AttractorState
from dionysus_metacog.core import MetaCogSignal, MetaCogTrace, PromotionLabel
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord
from dionysus_metacog.provenance import SourceReference


def test_import_root_version() -> None:
    assert __version__ == "0.1.1"
    assert AttractorAssessment.__name__ == "AttractorAssessment"
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
    assert state.basin_id == "focused"
    assert source.locator == "Figure 6"
