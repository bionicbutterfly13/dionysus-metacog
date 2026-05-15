import pytest

from dionysus_metacog.attractors import (
    AttractorBasin,
    AttractorSource,
    default_attractor_sources,
)
from dionysus_metacog.provenance import SourceReference


def test_default_attractor_sources_include_formal_and_protocol_lineage() -> None:
    sources = default_attractor_sources()

    assert isinstance(sources["friston-2014-cognitive-dynamics"], SourceReference)
    assert sources["friston-2014-cognitive-dynamics"].title == (
        "Cognitive Dynamics: From Attractors to Active Inference"
    )
    assert sources["friston-2014-cognitive-dynamics"].url == (
        "https://doi.org/10.1109/JPROC.2014.2306251"
    )
    assert sources["context-engineering-attractor-dynamics"].locator == (
        "00_COURSE/08_field_theory_integration/01_attractor_dynamics.md"
    )
    assert sources["spisak-friston-fep-attractor-network"].url == (
        "https://pni-lab.github.io/fep-attractor-network/"
    )


def test_attractor_source_uses_provenance_reference_contract() -> None:
    source = AttractorSource(
        source_id="test-source",
        title="Test Source",
        locator="test locator",
    )

    assert isinstance(source, SourceReference)


def test_attractor_basin_requires_source_backing() -> None:
    source = default_attractor_sources()["friston-2014-cognitive-dynamics"]
    basin = AttractorBasin(
        basin_id="focused_attention",
        attractor_label="focused attention",
        depth=0.8,
        width=0.6,
        stability=0.9,
        sources=(source,),
    )

    assert basin.source_ids == ("friston-2014-cognitive-dynamics",)
    assert basin.as_state().basin_id == "focused_attention"
    assert basin.as_state().stability == 0.9


def test_attractor_basin_rejects_empty_sources() -> None:
    with pytest.raises(ValueError, match="sources must not be empty"):
        AttractorBasin(
            basin_id="unbacked",
            attractor_label="unbacked idea",
            depth=0.5,
            width=0.5,
            stability=0.5,
        )


def test_attractor_basin_rejects_negative_geometry() -> None:
    source = AttractorSource(
        source_id="test-source",
        title="Test Source",
        locator="test locator",
    )

    with pytest.raises(ValueError, match="depth must be non-negative"):
        AttractorBasin(
            basin_id="bad_depth",
            attractor_label="bad depth",
            depth=-0.1,
            width=0.5,
            stability=0.5,
            sources=(source,),
        )

    with pytest.raises(ValueError, match="width must be non-negative"):
        AttractorBasin(
            basin_id="bad_width",
            attractor_label="bad width",
            depth=0.5,
            width=-0.1,
            stability=0.5,
            sources=(source,),
        )
