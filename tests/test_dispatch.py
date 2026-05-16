import asyncio
from dataclasses import dataclass

from dionysus_metacog.core import (
    AsyncInProcessMetaCogDispatcher,
    DispatchFailure,
    InProcessMetaCogDispatcher,
    MetaCogPayload,
    MetaCogPayloadHandler,
    MetaCogSignal,
)


def _payload() -> MetaCogPayload:
    return MetaCogPayload.from_signal(
        MetaCogSignal(
            name="attractor_control",
            value=0.7,
            source="test",
            metadata={"policy": "stabilize", "basin_id": "source-risk"},
        ),
        payload_type="metacog.attractor_assessment",
    )


@dataclass
class RecordingHandler:
    name: str
    calls: list[str]

    def handle(self, payload: MetaCogPayload) -> None:
        self.calls.append(f"{self.name}:{payload.payload_type}")


@dataclass
class FailingHandler:
    message: str = "dispatch failed"

    def handle(self, payload: MetaCogPayload) -> None:
        raise RuntimeError(self.message)


class AsyncRecordingHandler:
    def __init__(self, calls: list[str], name: str) -> None:
        self.calls = calls
        self.name = name

    async def handle(self, payload: MetaCogPayload) -> None:
        self.calls.append(f"{self.name}:{payload.signal.name}")


def test_payload_handler_protocol_accepts_structural_handler() -> None:
    handler = RecordingHandler(name="audit", calls=[])

    assert isinstance(handler, MetaCogPayloadHandler)


def test_in_process_dispatcher_fans_out_in_order() -> None:
    calls: list[str] = []
    dispatcher = InProcessMetaCogDispatcher(
        handlers=(
            RecordingHandler(name="first", calls=calls),
            RecordingHandler(name="second", calls=calls),
        )
    )

    result = dispatcher.dispatch(_payload())

    assert result.delivered == 2
    assert result.failures == ()
    assert result.success is True
    assert calls == [
        "first:metacog.attractor_assessment",
        "second:metacog.attractor_assessment",
    ]


def test_in_process_dispatcher_accepts_callable_handlers() -> None:
    calls: list[str] = []

    def handler(payload: MetaCogPayload) -> None:
        calls.append(payload.signal.metadata["policy"])

    result = InProcessMetaCogDispatcher(handlers=(handler,)).dispatch(_payload())

    assert result.delivered == 1
    assert calls == ["stabilize"]


def test_dispatcher_captures_failures_and_continues() -> None:
    calls: list[str] = []
    dispatcher = InProcessMetaCogDispatcher(
        handlers=(
            FailingHandler("bad handler"),
            RecordingHandler(name="after", calls=calls),
        )
    )

    result = dispatcher.dispatch(_payload())

    assert result.delivered == 1
    assert result.success is False
    assert result.failures == (
        DispatchFailure(
            handler_index=0,
            handler_name="FailingHandler",
            error_type="RuntimeError",
            message="bad handler",
        ),
    )
    assert calls == ["after:metacog.attractor_assessment"]


def test_dispatcher_can_fail_fast() -> None:
    calls: list[str] = []
    dispatcher = InProcessMetaCogDispatcher(
        handlers=(
            FailingHandler("stop"),
            RecordingHandler(name="after", calls=calls),
        ),
        fail_fast=True,
    )

    result = dispatcher.dispatch(_payload())

    assert result.delivered == 0
    assert result.failures[0].message == "stop"
    assert calls == []


def test_sync_dispatcher_rejects_async_handlers() -> None:
    dispatcher = InProcessMetaCogDispatcher(
        handlers=(AsyncRecordingHandler([], "async"),)
    )

    result = dispatcher.dispatch(_payload())

    assert result.delivered == 0
    assert result.failures == (
        DispatchFailure(
            handler_index=0,
            handler_name="AsyncRecordingHandler",
            error_type="TypeError",
            message="async handler requires AsyncInProcessMetaCogDispatcher",
        ),
    )


def test_async_dispatcher_supports_async_handlers() -> None:
    calls: list[str] = []
    dispatcher = AsyncInProcessMetaCogDispatcher(
        handlers=(
            AsyncRecordingHandler(calls=calls, name="first"),
            AsyncRecordingHandler(calls=calls, name="second"),
        )
    )

    result = asyncio.run(dispatcher.dispatch(_payload()))

    assert result.delivered == 2
    assert result.success is True
    assert calls == [
        "first:attractor_control",
        "second:attractor_control",
    ]
