# Dionysus Metacognition

Dionysus Metacognition is an active-inference metacognitive controller kit for
agent runtimes.

It provides a public Python package, `dionysus-metacognition`, with import root
`dionysus_metacog`. The package is designed to expose metacognitive control
primitives, model provenance, attractor-aware state tracking, and adapter seams
for systems such as Hermes Agent, Autonoesis, Elume, Sakshi, and
linoss-dynamics.

## Install

```bash
pip install dionysus-metacognition
```

## Import

```python
import dionysus_metacog
from dionysus_metacog.core import MetaCogSignal, PromotionLabel
```

For local code that wants a shorter alias:

```python
import dionysus_metacog as metacog
```

## Scope

Dionysus Metacognition is not a generic `utils` package and is not the ontology
owner for phenomenological self-modeling. It is the applied metacognitive
controller layer: the place where active-inference control signals, POMDP-style
model records, Markov blanket boundaries, attractor-aware runtime observations,
and adapter seams can be assembled without polluting host projects.

Autonoesis should remain the self-model and computational-phenomenology kernel.
Elume should remain the deterministic replay and competition substrate.
Sakshi should remain the witness and verification layer. linoss-dynamics should
remain the oscillator dynamics toolkit. Hermes Agent should remain a first-class
runtime adapter target, not a hard dependency.

## Package Layout

```text
dionysus_metacog/
  framework/     # canonical layer stack and dependency contract
  core/          # controller signals, traces, promotion labels
  models/        # active-inference, POMDP, Markov blanket records
  attractors/    # attractor-state interfaces
  adapters/      # optional integration seams
  provenance/    # source attribution and model lineage
```

## Framework Layers

The initial framework stack is intentionally explicit:

1. `provenance` owns source attribution and model lineage.
2. `generative_model` owns active-inference and POMDP model records.
3. `boundary` owns Markov blanket boundary records.
4. `dynamics` owns attractor-basin and dynamical-state observations.
5. `control` owns metacognitive control signals and traces.
6. `adapters` owns optional host-runtime integration seams.

The default layer contract is available in code:

```python
from dionysus_metacog.framework import FrameworkSpec

framework = FrameworkSpec.default()
print(framework.dependency_graph)
```

## Provenance Ledger

`ProvenanceLedger` is the source registry for framework records. It stores
`SourceReference` objects by `source_id`, accepts exact duplicate references,
and rejects conflicting duplicates so source lineage fails loudly instead of
silently drifting.

```python
from dionysus_metacog.attractors import default_attractor_sources
from dionysus_metacog.provenance import ProvenanceLedger

ledger = ProvenanceLedger.from_sources(default_attractor_sources().values())
metadata = ledger.metadata_for(("friston-2014-cognitive-dynamics",))
```

The emitted metadata is string-only so adapters can pass it through systems
such as Hermes Agent without taking a hard dependency on this package's Python
objects.

## Attractor Sources

Attractor-basin records must carry source backing. The initial source ledger
connects the package to:

- Friston, Sengupta, and Auletta's "Cognitive Dynamics: From Attractors to
  Active Inference" (`https://doi.org/10.1109/JPROC.2014.2306251`).
- Context-Engineering's attractor dynamics and attractor co-emergence protocol
  shell lineage.
- Spisak and Friston's PNI Lab article, "Self-orthogonalizing attractor neural
  networks emerging from the free energy principle"
  (`https://pni-lab.github.io/fep-attractor-network/`).

Attractor source records use the shared `SourceReference` provenance contract,
so source attribution stays consistent across attractor, model, and future
adapter layers.

```python
from dionysus_metacog.attractors import AttractorBasin, default_attractor_sources
from dionysus_metacog.models import PomdpStateRecord

sources = default_attractor_sources()
basin = AttractorBasin(
    basin_id="focused_attention",
    attractor_label="focused attention",
    depth=0.8,
    width=0.6,
    stability=0.9,
    sources=(sources["friston-2014-cognitive-dynamics"],),
)
model = PomdpStateRecord(
    hidden_state="focused",
    observation="task_stable",
    policy="continue",
    expected_free_energy=0.1,
    precision=0.9,
)
```

Use `AttractorAssessment` when an attractor observation should become a
portable metacognitive control signal:

```python
from dionysus_metacog.attractors import AttractorAssessment

assessment = AttractorAssessment.from_basin(basin=basin, model=model)
control_signal = assessment.to_signal()
```

When available, a `MarkovBlanketRecord` can be passed into
`AttractorAssessment.from_basin(...)` so the emitted control signal carries the
internal, external, sensory, and active-state boundary context alongside the
POMDP observation.

## Attractor Lifecycle

`AttractorObservation` and `AttractorTransition` describe how source-backed
basin states change over time. The transition classifier is deterministic and
intentionally small: it labels observations as `entered`, `held`,
`destabilized`, `escaped`, or `merged` while preserving source IDs across the
lifecycle.

```python
from dionysus_metacog.attractors import (
    AttractorObservation,
    AttractorTransition,
)

prior = AttractorObservation(state=basin.as_state(), source_ids=basin.source_ids)
current = AttractorObservation(
    state=basin.as_state(),
    source_ids=basin.source_ids,
)
transition = AttractorTransition.from_observations(
    prior=prior,
    current=current,
)
```

## Status

This is the initial public package skeleton. The API is intentionally small and
typed so that the package name can be claimed cleanly before deeper model
extraction lands.
