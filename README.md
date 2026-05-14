# Dionysus MetaCog

Dionysus MetaCog is an active-inference metacognitive controller kit for agent
runtimes.

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

Dionysus MetaCog is not a generic `utils` package and is not the ontology owner
for phenomenological self-modeling. It is the applied metacognitive controller
layer: the place where active-inference control signals, POMDP-style model
records, Markov blanket boundaries, attractor-aware runtime observations, and
adapter seams can be assembled without polluting host projects.

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

```python
from dionysus_metacog.attractors import AttractorBasin, default_attractor_sources

sources = default_attractor_sources()
basin = AttractorBasin(
    basin_id="focused_attention",
    attractor_label="focused attention",
    depth=0.8,
    width=0.6,
    stability=0.9,
    sources=(sources["friston-2014-cognitive-dynamics"],),
)
```

## Status

This is the initial public package skeleton. The API is intentionally small and
typed so that the package name can be claimed cleanly before deeper model
extraction lands.
