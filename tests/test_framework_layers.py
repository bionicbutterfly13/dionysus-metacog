import pytest

from dionysus_metacog.framework import FrameworkLayer, FrameworkSpec, LayerSpec


def test_default_framework_exposes_ordered_layers() -> None:
    framework = FrameworkSpec.default()

    assert [layer.name for layer in framework.layers] == [
        FrameworkLayer.PROVENANCE,
        FrameworkLayer.GENERATIVE_MODEL,
        FrameworkLayer.BOUNDARY,
        FrameworkLayer.DYNAMICS,
        FrameworkLayer.CONTROL,
        FrameworkLayer.ADAPTERS,
    ]


def test_default_framework_declares_explicit_dependencies() -> None:
    framework = FrameworkSpec.default()

    assert framework.layer(FrameworkLayer.GENERATIVE_MODEL).depends_on == (
        FrameworkLayer.PROVENANCE,
    )
    assert framework.layer(FrameworkLayer.BOUNDARY).depends_on == (
        FrameworkLayer.GENERATIVE_MODEL,
    )
    assert framework.layer(FrameworkLayer.DYNAMICS).depends_on == (
        FrameworkLayer.BOUNDARY,
    )
    assert framework.layer(FrameworkLayer.CONTROL).depends_on == (
        FrameworkLayer.DYNAMICS,
    )
    assert framework.layer(FrameworkLayer.ADAPTERS).depends_on == (
        FrameworkLayer.CONTROL,
    )


def test_framework_lookup_accepts_strings_and_enums() -> None:
    framework = FrameworkSpec.default()

    assert framework.layer("control") == framework.layer(FrameworkLayer.CONTROL)
    assert "MetaCogSignal" in framework.layer("control").owns


def test_framework_rejects_duplicate_layers() -> None:
    provenance = LayerSpec(
        name=FrameworkLayer.PROVENANCE,
        purpose="source attribution",
        owns=("SourceReference",),
    )

    with pytest.raises(ValueError, match="duplicate framework layer"):
        FrameworkSpec(layers=(provenance, provenance))


def test_framework_rejects_out_of_order_dependencies() -> None:
    control = LayerSpec(
        name=FrameworkLayer.CONTROL,
        purpose="metacognitive action selection",
        owns=("MetaCogSignal",),
        depends_on=(FrameworkLayer.DYNAMICS,),
    )
    dynamics = LayerSpec(
        name=FrameworkLayer.DYNAMICS,
        purpose="attractor basin state",
        owns=("AttractorState",),
    )

    with pytest.raises(ValueError, match="depends on later layer"):
        FrameworkSpec(layers=(control, dynamics))


def test_layer_specs_require_real_purpose_and_ownership() -> None:
    with pytest.raises(ValueError, match="purpose must not be empty"):
        LayerSpec(name=FrameworkLayer.PROVENANCE, purpose="", owns=("SourceReference",))

    with pytest.raises(ValueError, match="owns must not be empty"):
        LayerSpec(name=FrameworkLayer.PROVENANCE, purpose="source attribution")
