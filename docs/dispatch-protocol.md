# Dispatch Protocol

Dionysus Metacognition defines the payload contract and a small dispatch seam.
It does not own the host runtime's broker, queue, retry store, or process
supervisor.

## Core Types

| Type | Purpose |
| --- | --- |
| `MetaCogPayloadHandler` | Structural sync handler protocol with `handle(payload)` |
| `AsyncMetaCogPayloadHandler` | Structural async handler protocol with `async handle(payload)` |
| `InProcessMetaCogDispatcher` | Dependency-free ordered sync fanout |
| `AsyncInProcessMetaCogDispatcher` | Dependency-free ordered async fanout |
| `DispatchResult` | Delivery count plus captured failures |
| `DispatchFailure` | Handler index, handler name, error type, and message |

## In-Process Dispatch

```python
from dionysus_metacog import InProcessMetaCogDispatcher

dispatcher = InProcessMetaCogDispatcher(
    handlers=(audit_handler, sakshi_guard_handler),
)
result = dispatcher.dispatch(payload)

if not result.success:
    for failure in result.failures:
        print(failure.handler_name, failure.message)
```

Handlers can be objects with a `handle(payload)` method or plain callables that
accept one `MetaCogPayload`.

## Async Dispatch

```python
from dionysus_metacog import AsyncInProcessMetaCogDispatcher

dispatcher = AsyncInProcessMetaCogDispatcher(
    handlers=(async_audit_handler, async_guard_handler),
)
result = await dispatcher.dispatch(payload)
```

Async dispatch can call sync or async handlers in order. Sync dispatch rejects
async handlers so a coroutine is not accidentally dropped.

## Broker Boundary

RabbitMQ, Redis Streams, NATS, Kafka, HTTP webhooks, and host event buses should
live outside this package. A host can wrap any transport behind the protocol:

```python
import json


class RabbitPayloadHandler:
    def __init__(self, channel):
        self.channel = channel

    def handle(self, payload):
        self.channel.basic_publish(
            exchange="metacog",
            routing_key=payload.payload_type,
            body=json.dumps(payload.as_dict()).encode("utf-8"),
        )
```

This keeps `dionysus-metacognition` focused on portable payloads, attribution,
control assessment, and structural adapter seams.
