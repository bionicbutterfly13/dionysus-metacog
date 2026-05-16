"""Core metacognitive control records."""

from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from inspect import isawaitable
from time import time
from typing import Protocol, runtime_checkable

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | Sequence["JsonValue"] | Mapping[str, "JsonValue"]
PayloadCallable = Callable[["MetaCogPayload"], None]
AsyncPayloadCallable = Callable[["MetaCogPayload"], Awaitable[None]]


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


@runtime_checkable
class MetaCogPayloadHandler(Protocol):
    """Structural handler for host-side metacognitive payload dispatch."""

    def handle(self, payload: MetaCogPayload) -> None:
        """Handle a single metacognitive payload."""


@runtime_checkable
class AsyncMetaCogPayloadHandler(Protocol):
    """Async structural handler for host-side metacognitive payload dispatch."""

    async def handle(self, payload: MetaCogPayload) -> None:
        """Handle a single metacognitive payload asynchronously."""


@dataclass(frozen=True, slots=True)
class DispatchFailure:
    """Failure captured from a payload handler during dispatch."""

    handler_index: int
    handler_name: str
    error_type: str
    message: str


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """Result of dispatching a payload to one or more handlers."""

    payload: MetaCogPayload
    delivered: int = 0
    failures: tuple[DispatchFailure, ...] = ()

    @property
    def success(self) -> bool:
        """Return True when every attempted handler completed."""

        return not self.failures


class InProcessMetaCogDispatcher:
    """Dependency-free in-process dispatcher for host runtimes."""

    def __init__(
        self,
        handlers: Sequence[MetaCogPayloadHandler | PayloadCallable],
        *,
        fail_fast: bool = False,
    ) -> None:
        self._handlers = tuple(handlers)
        self.fail_fast = fail_fast

    @property
    def handlers(self) -> tuple[MetaCogPayloadHandler | PayloadCallable, ...]:
        """Return dispatch handlers in delivery order."""

        return self._handlers

    def dispatch(self, payload: MetaCogPayload) -> DispatchResult:
        """Dispatch a payload to handlers in order."""

        delivered = 0
        failures: list[DispatchFailure] = []
        for index, handler in enumerate(self.handlers):
            try:
                _deliver_payload(handler=handler, payload=payload)
            except Exception as exc:  # noqa: BLE001 - dispatch records failures.
                failures.append(_failure_from_exception(index, handler, exc))
                if self.fail_fast:
                    break
            else:
                delivered += 1
        return DispatchResult(
            payload=payload,
            delivered=delivered,
            failures=tuple(failures),
        )


class AsyncInProcessMetaCogDispatcher:
    """Dependency-free async dispatcher for host runtimes."""

    def __init__(
        self,
        handlers: Sequence[
            MetaCogPayloadHandler
            | AsyncMetaCogPayloadHandler
            | PayloadCallable
            | AsyncPayloadCallable
        ],
        *,
        fail_fast: bool = False,
    ) -> None:
        self._handlers = tuple(handlers)
        self.fail_fast = fail_fast

    @property
    def handlers(
        self,
    ) -> tuple[
        MetaCogPayloadHandler
        | AsyncMetaCogPayloadHandler
        | PayloadCallable
        | AsyncPayloadCallable,
        ...,
    ]:
        """Return dispatch handlers in delivery order."""

        return self._handlers

    async def dispatch(self, payload: MetaCogPayload) -> DispatchResult:
        """Dispatch a payload to sync or async handlers in order."""

        delivered = 0
        failures: list[DispatchFailure] = []
        for index, handler in enumerate(self.handlers):
            try:
                result = _dispatch_call(handler=handler, payload=payload)
                if isawaitable(result):
                    await result
            except Exception as exc:  # noqa: BLE001 - dispatch records failures.
                failures.append(_failure_from_exception(index, handler, exc))
                if self.fail_fast:
                    break
            else:
                delivered += 1
        return DispatchResult(
            payload=payload,
            delivered=delivered,
            failures=tuple(failures),
        )


def _deliver_payload(
    *,
    handler: MetaCogPayloadHandler | PayloadCallable,
    payload: MetaCogPayload,
) -> None:
    result = _dispatch_call(handler=handler, payload=payload)
    if isawaitable(result):
        close = getattr(result, "close", None)
        if close is not None:
            close()
        raise TypeError("async handler requires AsyncInProcessMetaCogDispatcher")


def _dispatch_call(
    *,
    handler: (
        MetaCogPayloadHandler
        | AsyncMetaCogPayloadHandler
        | PayloadCallable
        | AsyncPayloadCallable
    ),
    payload: MetaCogPayload,
) -> object:
    handle = getattr(handler, "handle", None)
    if handle is not None:
        return handle(payload)
    return handler(payload)


def _failure_from_exception(
    index: int,
    handler: object,
    exc: Exception,
) -> DispatchFailure:
    return DispatchFailure(
        handler_index=index,
        handler_name=_handler_name(handler),
        error_type=type(exc).__name__,
        message=str(exc),
    )


def _handler_name(handler: object) -> str:
    if hasattr(handler, "__name__"):
        return str(handler.__name__)
    return type(handler).__name__


__all__ = [
    "AsyncInProcessMetaCogDispatcher",
    "AsyncMetaCogPayloadHandler",
    "AsyncPayloadCallable",
    "DispatchFailure",
    "DispatchResult",
    "JsonScalar",
    "JsonValue",
    "InProcessMetaCogDispatcher",
    "MetaCogPayload",
    "MetaCogPayloadHandler",
    "MetaCogSignal",
    "MetaCogTrace",
    "PayloadCallable",
    "PromotionLabel",
]
