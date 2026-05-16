# Adapter Pipeline

This guide shows the host-neutral adapter flow for Dionysus Metacognition.
Adjacent packages keep their own ownership boundaries; this package translates
their records into portable metacognitive control payloads.

## Boundary Rule

`dionysus-metacognition` must not hard-import Autonoesis, Elume, Sakshi, or
linoss-dynamics from its core package. Adapters are structural: they accept
objects with the required fields and return package-native records.

## Pipeline

1. Elume or an Elume-shaped host produces a winning ThoughtSeed and an
   EFE-style result.
2. The Elume adapter converts those into `AttractorAssessment`.
3. The assessment emits `MetaCogPayload`.
4. linoss-dynamics output may supply trajectory-derived `AttractorState` or
   filtering-derived `PomdpStateRecord`.
5. Autonoesis output may enrich payload context with self-model,
   meta-awareness, and metacognitive-feeling state.
6. Sakshi may consume the payload as a witness event, write-guard payload,
   control action, or dominant ThoughtSeed snapshot.
7. A host may route the payload through the dispatch protocol. Broker choices
   such as RabbitMQ, Redis Streams, NATS, Kafka, or HTTP webhooks belong behind
   host-owned handlers, not in this package.

## Example

```python
from dionysus_metacog.adapters.autonoesis import enrich_payload_with_self_model
from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.sakshi import meta_payload_to_write_guard_payload

assessment = thoughtseed_winner_to_assessment(
    seed,
    efe_result,
    source_ids=("elume-thought-competition",),
)
payload = assessment.to_payload()
payload = enrich_payload_with_self_model(payload, self_model=self_model)
guard_payload = meta_payload_to_write_guard_payload(payload)
```

Runnable versions live under `examples/`:

- `examples/host_runtime_pipeline.py`
- `examples/elume_to_sakshi.py`
- `examples/linoss_state_input.py`

## What Each Adapter Owns

| Adapter | Input | Output | Boundary |
| --- | --- | --- | --- |
| Elume | ThoughtSeed-like and EFE-result-like objects | `AttractorAssessment` | deterministic cognition substrate |
| linoss-dynamics | trajectory, stability, and filter dictionaries | `AttractorState`, `PomdpStateRecord` | numerical substrate |
| Autonoesis | SelfModel, meta-awareness, feelings | payload context, `MetaCogSignal` | self-model ontology owner |
| Sakshi | `MetaCogPayload` or `MetaCogSignal` | witness/control dictionaries | verification and gating layer |

## Release Guard

Before publishing a release after adapter changes, run:

```bash
uv run pytest
uv run ruff check .
rm -rf dist build && uv build
uvx --from twine twine check dist/*
```
