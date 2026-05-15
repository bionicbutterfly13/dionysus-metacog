import json

import pytest

from dionysus_metacog.attractors import AttractorAssessment, AttractorBasin
from dionysus_metacog.core import MetaCogPayload, MetaCogSignal
from dionysus_metacog.models import MarkovBlanketRecord, PomdpStateRecord
from dionysus_metacog.provenance import ProvenanceLedger, SourceReference


def test_metacog_payload_is_json_safe() -> None:
    signal = MetaCogSignal(
        name="attractor_control",
        value=0.42,
        source="test",
        confidence=0.8,
        metadata={"policy": "hold", "basin_id": "focused_attention"},
    )
    payload = MetaCogPayload.from_signal(
        signal,
        payload_type="metacog.control",
        schema_version="1.0",
    )

    as_dict = payload.as_dict()

    assert as_dict["payload_type"] == "metacog.control"
    assert as_dict["schema_version"] == "1.0"
    assert as_dict["signal"]["name"] == "attractor_control"
    assert as_dict["signal"]["metadata"]["policy"] == "hold"
    json.dumps(as_dict)


def test_metacog_payload_rejects_empty_payload_type() -> None:
    signal = MetaCogSignal(name="attractor_control", value=0.42, source="test")

    with pytest.raises(ValueError, match="payload_type must not be empty"):
        MetaCogPayload.from_signal(signal, payload_type="")


def test_assessment_payload_includes_provenance_and_boundary() -> None:
    source = SourceReference(
        source_id="paper-1",
        title="Paper One",
        locator="Section 1",
        url="https://example.test/paper-1",
    )
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
    ledger = ProvenanceLedger.from_sources((source,))

    payload = AttractorAssessment.from_basin(
        basin=basin,
        model=model,
        blanket=blanket,
    ).to_payload(ledger=ledger)
    as_dict = payload.as_dict()

    assert as_dict["payload_type"] == "metacog.attractor_assessment"
    assert as_dict["signal"]["metadata"]["policy"] == "hold"
    assert as_dict["provenance"]["source_ids"] == ("paper-1",)
    assert as_dict["provenance"]["sources"][0]["title"] == "Paper One"
    assert as_dict["boundary"]["internal_states"] == ("belief_precision",)
    json.dumps(as_dict)
