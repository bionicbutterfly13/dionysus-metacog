"""Core metacognitive control records."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from time import time

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | Sequence["JsonValue"] | Mapping[str, "JsonValue"]


class PromotionLabel(StrEnum):
    """Sharing and promotion state for captured metacognitive material."""

    PRIVATE = "private"
    NEEDS_REDACTION = "needs_redaction"
    SHAREABLE = "shareable"
    UPSTREAM_CANDIDATE = "upstream_candidate"


@dataclass(frozen=True, slots=True)
class MetaCogSignal:
    """A typed metacognitive observation or control signal."""

    name: str
    value: float
    source: str
    confidence: float = 1.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if not self.source:
            raise ValueError("source must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class MetaCogTrace:
    """Append-only trace item suitable for local-first metacognitive ledgers."""

    signal: MetaCogSignal
    label: PromotionLabel = PromotionLabel.PRIVATE
    created_at: float = field(default_factory=time)
    note: str = ""

    @property
    def shareable(self) -> bool:
        return self.label in {
            PromotionLabel.SHAREABLE,
            PromotionLabel.UPSTREAM_CANDIDATE,
        }


@dataclass(frozen=True, slots=True)
class MetaCogPayload:
    """JSON-safe metacognitive payload for host-runtime adapters."""

    payload_type: str
    schema_version: str
    signal: MetaCogSignal
    provenance: Mapping[str, JsonValue] = field(default_factory=dict)
    boundary: Mapping[str, JsonValue] = field(default_factory=dict)
    context: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.payload_type:
            raise ValueError("payload_type must not be empty")
        if not self.schema_version:
            raise ValueError("schema_version must not be empty")

    @classmethod
    def from_signal(
        cls,
        signal: MetaCogSignal,
        *,
        payload_type: str,
        schema_version: str = "1.0",
        provenance: Mapping[str, JsonValue] | None = None,
        boundary: Mapping[str, JsonValue] | None = None,
        context: Mapping[str, JsonValue] | None = None,
    ) -> "MetaCogPayload":
        """Build a payload from a portable metacognitive signal."""

        return cls(
            payload_type=payload_type,
            schema_version=schema_version,
            signal=signal,
            provenance={} if provenance is None else dict(provenance),
            boundary={} if boundary is None else dict(boundary),
            context={} if context is None else dict(context),
        )

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a JSON-serializable dictionary representation."""

        return {
            "payload_type": self.payload_type,
            "schema_version": self.schema_version,
            "signal": {
                "name": self.signal.name,
                "value": self.signal.value,
                "source": self.signal.source,
                "confidence": self.signal.confidence,
                "metadata": dict(self.signal.metadata),
            },
            "provenance": dict(self.provenance),
            "boundary": dict(self.boundary),
            "context": dict(self.context),
        }


__all__ = [
    "JsonScalar",
    "JsonValue",
    "MetaCogPayload",
    "MetaCogSignal",
    "MetaCogTrace",
    "PromotionLabel",
]
