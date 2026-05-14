"""Layer contract for the Dionysus MetaCog framework."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum


class FrameworkLayer(StrEnum):
    """Canonical layers in the Dionysus MetaCog framework."""

    PROVENANCE = "provenance"
    GENERATIVE_MODEL = "generative_model"
    BOUNDARY = "boundary"
    DYNAMICS = "dynamics"
    CONTROL = "control"
    ADAPTERS = "adapters"


@dataclass(frozen=True, slots=True)
class LayerSpec:
    """A framework layer with its ownership and dependency contract."""

    name: FrameworkLayer
    purpose: str
    owns: tuple[str, ...] = ()
    depends_on: tuple[FrameworkLayer, ...] = ()
    adapters: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _coerce_layer(self.name))
        object.__setattr__(self, "depends_on", _coerce_layers(self.depends_on))
        object.__setattr__(self, "owns", tuple(self.owns))
        object.__setattr__(self, "adapters", tuple(self.adapters))

        if not self.purpose:
            raise ValueError("purpose must not be empty")
        if not self.owns:
            raise ValueError("owns must not be empty")


@dataclass(frozen=True, slots=True)
class FrameworkSpec:
    """Ordered framework specification for metacognitive runtime assembly."""

    layers: tuple[LayerSpec, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "layers", tuple(self.layers))
        _validate_layers(self.layers)

    @classmethod
    def default(cls) -> "FrameworkSpec":
        """Return the canonical Dionysus MetaCog layer stack."""

        return cls(
            layers=(
                LayerSpec(
                    name=FrameworkLayer.PROVENANCE,
                    purpose="source attribution and model lineage",
                    owns=("SourceReference",),
                ),
                LayerSpec(
                    name=FrameworkLayer.GENERATIVE_MODEL,
                    purpose="active-inference and POMDP model records",
                    owns=("PomdpStateRecord",),
                    depends_on=(FrameworkLayer.PROVENANCE,),
                ),
                LayerSpec(
                    name=FrameworkLayer.BOUNDARY,
                    purpose="Markov blanket boundary records",
                    owns=("MarkovBlanketRecord",),
                    depends_on=(FrameworkLayer.GENERATIVE_MODEL,),
                ),
                LayerSpec(
                    name=FrameworkLayer.DYNAMICS,
                    purpose="attractor basin and dynamical-state observations",
                    owns=("AttractorState",),
                    depends_on=(FrameworkLayer.BOUNDARY,),
                ),
                LayerSpec(
                    name=FrameworkLayer.CONTROL,
                    purpose="metacognitive control signals and traces",
                    owns=("MetaCogSignal", "MetaCogTrace", "PromotionLabel"),
                    depends_on=(FrameworkLayer.DYNAMICS,),
                ),
                LayerSpec(
                    name=FrameworkLayer.ADAPTERS,
                    purpose="optional host runtime integration seams",
                    owns=("Hermes Agent adapter",),
                    depends_on=(FrameworkLayer.CONTROL,),
                    adapters=("hermes", "autonoesis", "elume", "sakshi"),
                ),
            )
        )

    @property
    def dependency_graph(self) -> Mapping[FrameworkLayer, tuple[FrameworkLayer, ...]]:
        return {layer.name: layer.depends_on for layer in self.layers}

    def layer(self, name: FrameworkLayer | str) -> LayerSpec:
        layer_name = _coerce_layer(name)
        for layer in self.layers:
            if layer.name == layer_name:
                return layer
        raise KeyError(f"unknown framework layer: {layer_name}")


def _coerce_layer(name: FrameworkLayer | str) -> FrameworkLayer:
    if isinstance(name, FrameworkLayer):
        return name
    return FrameworkLayer(name)


def _coerce_layers(names: Iterable[FrameworkLayer | str]) -> tuple[FrameworkLayer, ...]:
    return tuple(_coerce_layer(name) for name in names)


def _validate_layers(layers: tuple[LayerSpec, ...]) -> None:
    seen: dict[FrameworkLayer, int] = {}
    for index, layer in enumerate(layers):
        if layer.name in seen:
            raise ValueError(f"duplicate framework layer: {layer.name}")
        seen[layer.name] = index

    for index, layer in enumerate(layers):
        for dependency in layer.depends_on:
            dependency_index = seen.get(dependency)
            if dependency_index is None:
                raise ValueError(
                    f"framework layer {layer.name} depends on missing layer "
                    f"{dependency}"
                )
            if dependency_index > index:
                raise ValueError(
                    f"framework layer {layer.name} depends on later layer "
                    f"{dependency}"
                )


__all__ = ["FrameworkLayer", "FrameworkSpec", "LayerSpec"]
