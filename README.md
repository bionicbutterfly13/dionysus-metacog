# Dionysus MetaCog

Dionysus MetaCog is an active-inference metacognitive controller kit for agent
runtimes.

It provides a public Python package, `dionysus-metacog`, with import root
`dionysus_metacog`. The package is designed to expose metacognitive control
primitives, model provenance, attractor-aware state tracking, and adapter seams
for systems such as Hermes Agent, Autonoesis, Elume, Sakshi, and
linoss-dynamics.

## Install

```bash
pip install dionysus-metacog
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
  core/          # controller signals, traces, promotion labels
  models/        # active-inference, POMDP, Markov blanket records
  attractors/    # attractor-state interfaces
  adapters/      # optional integration seams
  provenance/    # source attribution and model lineage
```

## Status

This is the initial public package skeleton. The API is intentionally small and
typed so that the package name can be claimed cleanly before deeper model
extraction lands.
