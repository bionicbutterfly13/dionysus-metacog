# Adapter Compatibility Matrix

This matrix records the structural fixture contracts used to keep optional
adapters compatible without importing adjacent packages at runtime.

## Rule

`dionysus-metacognition` adapters accept host-shaped objects by structure. Test
fixtures under `tests/fixtures/adapter_contracts.py` are the compatibility
surface for this package; they are not copies of Autonoesis, Elume, Sakshi, or
linoss-dynamics classes.

## Fixture Coverage

| Adjacent package | Compatibility fixture | Required adapter fields | Adapter target | Test coverage |
| --- | --- | --- | --- | --- |
| Elume | `CompatibleThoughtSeed` | `id`, `content`, `activation_level`, `layer`, `blanket_tag`, `dominant_basin`, `source_id` | `thoughtseed_to_attractor_state`, `thoughtseed_to_markov_blanket`, `thoughtseed_winner_to_assessment` | `tests/test_adapter_compatibility_fixtures.py` |
| Elume | `CompatibleEfeResult` | `hidden_state`, `observation`, `policy`, `expected_free_energy`, `precision` | `efe_result_to_pomdp_record`, `thoughtseed_winner_to_assessment` | `tests/test_adapter_compatibility_fixtures.py` |
| linoss-dynamics | `compatible_linoss_metrics()` | `energy_before`, `energy_after`, `delta_energy`, `mode`, `damping_mode` | `linoss_metrics_to_attractor_state` | `tests/test_adapter_compatibility_fixtures.py` |
| linoss-dynamics | `compatible_linoss_filter_result()` | `m_f`, `P_f`, `loglik` | `linoss_filter_to_pomdp_record` | `tests/test_adapter_compatibility_fixtures.py` |
| Autonoesis | `CompatibleSelfModel` | `subject_id`, `phenomenal`, `agency`, `ownership`, `boundary`, `perspective`, `meta`, `revision` | `enrich_payload_with_self_model` | `tests/test_adapter_compatibility_fixtures.py` |
| Autonoesis | `CompatibleMetaAwareness` | `opacity_level`, `cycle_state`, `prior_type` | `enrich_payload_with_self_model`, `meta_awareness_to_signal` | `tests/test_adapter_compatibility_fixtures.py` |
| Autonoesis | `CompatibleMetacognitiveFeeling` | `feeling_type`, `intensity`, `valence`, `precision_correlate`, `opacity_impact` | `enrich_payload_with_self_model`, `metacognitive_feeling_to_signal` | `tests/test_adapter_compatibility_fixtures.py` |
| Sakshi | `MetaCogPayload` and `MetaCogSignal` from package core | `signal`, `context`, `metadata`, `policy`, `basin_id`, `free_energy_proxy` | `meta_payload_to_write_guard_payload`, `signal_to_np_state_snapshot` | `tests/test_adapter_compatibility_fixtures.py` |

## Dispatch Coverage

The compatibility fixture suite also sends a fixture-derived `MetaCogPayload`
through `InProcessMetaCogDispatcher`. That proves host handlers can consume the
same payload shape produced by the optional adapter pipeline.

## Boundary Checks

The fixture tests assert that importing and using adapter modules does not load
the sibling packages:

- `autonoesis`
- `elume`
- `linoss_dynamics`
- `sakshi`

If an adapter later adds an optional real-package integration test, keep it
separate and skip it when the adjacent package is absent. The structural fixture
suite must remain dependency-free.
