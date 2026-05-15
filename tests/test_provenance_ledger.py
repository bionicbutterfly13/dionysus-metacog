import pytest

from dionysus_metacog.attractors import AttractorAssessment, AttractorBasin
from dionysus_metacog.models import PomdpStateRecord
from dionysus_metacog.provenance import (
    ProvenanceLedger,
    SourceConflictError,
    SourceReference,
)


def test_provenance_ledger_resolves_sources_by_id() -> None:
    source = SourceReference(
        source_id="paper-1",
        title="Paper One",
        locator="Section 1",
        url="https://example.test/paper-1",
    )

    ledger = ProvenanceLedger.from_sources((source,))

    assert ledger.get("paper-1") == source
    assert ledger.resolve(("paper-1",)) == (source,)


def test_provenance_ledger_rejects_conflicting_duplicate_ids() -> None:
    first = SourceReference(
        source_id="same-id",
        title="First Title",
        locator="Section 1",
    )
    conflicting = SourceReference(
        source_id="same-id",
        title="Different Title",
        locator="Section 1",
    )

    with pytest.raises(SourceConflictError, match="same-id"):
        ProvenanceLedger.from_sources((first, conflicting))


def test_provenance_ledger_allows_exact_duplicate_references() -> None:
    source = SourceReference(
        source_id="same-id",
        title="Same Title",
        locator="Section 1",
    )

    ledger = ProvenanceLedger.from_sources((source, source))

    assert ledger.source_ids == ("same-id",)


def test_provenance_ledger_emits_adapter_friendly_metadata() -> None:
    first = SourceReference(
        source_id="paper-1",
        title="Paper One",
        locator="Section 1",
        url="https://example.test/paper-1",
    )
    second = SourceReference(
        source_id="paper-2",
        title="Paper Two",
        locator="Figure 2",
    )
    ledger = ProvenanceLedger.from_sources((first, second))

    assert ledger.metadata_for(("paper-1", "paper-2")) == {
        "source_ids": "paper-1,paper-2",
        "source_titles": "Paper One|Paper Two",
        "source_locators": "paper-1=Section 1|paper-2=Figure 2",
        "source_urls": "paper-1=https://example.test/paper-1",
    }


def test_attractor_assessment_signal_can_include_ledger_metadata() -> None:
    source = SourceReference(
        source_id="paper-1",
        title="Paper One",
        locator="Section 1",
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
    ledger = ProvenanceLedger.from_sources((source,))

    signal = AttractorAssessment.from_basin(basin=basin, model=model).to_signal(
        ledger=ledger
    )

    assert signal.metadata["source_ids"] == "paper-1"
    assert signal.metadata["source_titles"] == "Paper One"
    assert signal.metadata["source_locators"] == "paper-1=Section 1"
