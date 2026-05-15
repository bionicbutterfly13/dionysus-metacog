# Cross-Package Boundary Map

This map records the current source-of-truth boundary for Dionysus
Metacognition against the adjacent packages Dr. Mani asked us to keep clean:
Autonoesis, Elume, Sakshi, and linoss-dynamics.

Scan scope for this pass:

- `/Volumes/Asylum/dev/elume`
- `/Volumes/Asylum/dev/autonoesis`
- `/Volumes/Asylum/dev/sakshi`
- `/Volumes/Asylum/dev/linoss-dynamics`

No `Sync` or `sync` directories were accessed.

## Decision Summary

`dionysus-metacognition` should remain the host-neutral metacognitive control
and adapter kit. It should not absorb the ontology or runtime responsibilities
of the adjacent packages.

| Package | Boundary decision | Reason |
| --- | --- | --- |
| Autonoesis | Self-model and computational-phenomenology owner | Owns self-modeling, meta-awareness, metacognitive feelings, transparency/opacity, agency, and ownership |
| Elume | Optional deterministic cognition adapter | Owns immutable ThoughtSeed records, EFE-style thought competition, priors, curiosity scoring, and replayable envelope operations |
| Sakshi | Optional witness and gate adapter | Owns expectation checking, write guards, plan soundness, intervention validation, and monitor-assess-control witness flow |
| linoss-dynamics | Optional numerical substrate adapter | Owns oscillator trajectories, stability diagnostics, damped stepping, Kalman filtering, smoothing, and fitted latent dynamics |

The practical rule: core records stay here; specialized execution stays in the
package that already owns it; adapters translate between them.

## Core Package Boundary

Dionysus Metacognition owns:

- `MetaCogPayload` and portable control signals.
- `SourceReference` and `ProvenanceLedger` for attribution.
- `PomdpStateRecord` for active-inference-facing state summaries.
- `MarkovBlanketRecord` for boundary summaries.
- `AttractorState`, `AttractorBasin`, `AttractorTransition`, and
  `AttractorAssessment`.
- Adapter protocols that accept host objects without importing host runtimes.

Dionysus Metacognition should not own:

- self-model ontology or phenomenological subjectivity,
- deterministic thought competition kernels,
- witness/verification gates,
- oscillator solvers,
- host event buses, graph databases, or FastAPI routers.

## Autonoesis

Recommendation: keep as ontology/kernel for self-model, phenomenology,
meta-awareness, agency, ownership, and lightweight self-model provenance.

Evidence:

- `/Volumes/Asylum/dev/autonoesis/README.md` declares the package as a self-model
  and autonoetic cognition toolkit.
- `/Volumes/Asylum/dev/autonoesis/docs/prd.md` frames the product around
  phenomenological self-modeling.
- `/Volumes/Asylum/dev/autonoesis/src/autonoesis/inference/meta_awareness.py`
  owns meta-awareness inference.
- `/Volumes/Asylum/dev/autonoesis/src/autonoesis/feelings/metacognitive_feelings.py`
  owns metacognitive feeling records.
- `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models/smt_constraints.py` and
  `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models/consciousness_constraints.py`
  own self-model/transparency/opacity constraints.
- No direct `ThoughtSeed`, `POMDP`, or `Markov blanket` symbol was found in this
  pass.

Adapter posture:

- Treat Autonoesis outputs as optional upstream phenomenology/self-model inputs
  to `MetaCogPayload.context`.
- Keep D3-specific event bus, OODA, Heartbeat, Observatory, and basin-router
  wiring outside Autonoesis core.
- Do not move true meta-awareness ontology into `dionysus-metacognition`.

Cleanup flags:

- `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models.py` duplicates the active
  package directory `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models/`; this
  is a stale-shadow risk for Autonoesis cleanup.
- Package metadata says MIT, version `0.3.0`, Python `>=3.11`, and dependencies
  `numpy`, `pydantic`, and `scipy`.

## Elume

Recommendation: optional adapter target, not a core dependency.

Evidence:

- `/Volumes/Asylum/dev/elume/src/elume/models/thought.py` defines immutable
  `ThoughtSeed` and related thought-layer, blanket, activation, basin, source,
  reinforcement, and spawn semantics.
- `/Volumes/Asylum/dev/elume/src/elume/cognition/competition.py` implements
  deterministic thought competition and returns EFE-style results.
- `/Volumes/Asylum/dev/elume/src/elume/models/cognitive.py` defines
  `EFEResult` and `EFEResponse`.
- `/Volumes/Asylum/dev/elume/src/elume/cognition/priors.py` applies allow,
  block, boost, and suppress priors before competition.
- `/Volumes/Asylum/dev/elume/src/elume/cognition/curiosity.py` scores ThoughtSeed
  information gain and can convert curiosity into prior boosts.
- `/Volumes/Asylum/dev/elume/src/elume/envelope/ops/thought_competition.py`
  exposes replayable thought competition as an envelope operation.

Adapter posture:

- Use Elume when a host wants deterministic ThoughtSeed competition, EFE-style
  ranking, prior-gated cognition, or replayable competition traces.
- Do not make Elume a required dependency for `dionysus-metacognition`.
- A future optional adapter can convert Elume `ThoughtSeed`/`EFEResult` outputs
  into `AttractorAssessment` and `MetaCogPayload`.

Metadata:

- Package `elume`, version `0.4.0`.
- License MIT.
- Depends on `numpy` and `linoss-dynamics`.

## Sakshi

Recommendation: witness layer boundary and optional policy/gating adapter.

Evidence:

- `/Volumes/Asylum/dev/sakshi/README.md` and
  `/Volumes/Asylum/dev/sakshi/docs/architecture.md` describe Sakshi as an
  observer/witness package that checks expectations and emits signals while the
  host owns planning, memory, world models, and side effects.
- `/Volumes/Asylum/dev/sakshi/sakshi/protocols.py` defines witness and guard
  seams such as basin hooks and write guards.
- `/Volumes/Asylum/dev/sakshi/sakshi/meta/controller.py` runs a
  monitor-interpret-evaluate-intend-plan-control loop over traces.
- `/Volumes/Asylum/dev/sakshi/sakshi/models/cycle.py` includes
  `dominant_thoughtseed_id` and precision-delta style active-inference adapter
  signals.
- `/Volumes/Asylum/dev/sakshi/sakshi/goals/graph.py`,
  `/Volumes/Asylum/dev/sakshi/sakshi/goals/monitor.py`, and related goal modules
  support audit/lifecycle surfaces, not host agenda ownership.

Adapter posture:

- Use Sakshi to witness `MetaCogPayload` emissions, gate write/control actions,
  validate interventions, and record ThoughtSeed/basin snapshots.
- Do not move Dionysus host policy, agenda ownership, or metacognitive ontology
  into Sakshi core.

Cleanup flags:

- Package metadata says `pysakshi` version `0.12.0`, Apache-2.0, Python
  `>=3.11`.
- README status still says `0.11.0 pre-1.0`; that is documentation drift in
  Sakshi, not a Dionysus Metacognition issue.

## linoss-dynamics

Recommendation: numerical substrate and optional dynamics adapter.

Evidence:

- `/Volumes/Asylum/dev/linoss-dynamics/src/linoss_dynamics/solver.py` implements
  oscillator stepping, full trajectory scans, energy, energy deltas, and
  convergence windows.
- `/Volumes/Asylum/dev/linoss-dynamics/src/linoss_dynamics/stability.py`
  implements stability constraints and maps eigenvalues to frequency/damping.
- `/Volumes/Asylum/dev/linoss-dynamics/src/linoss_dynamics/filters.py`
  implements Kalman filtering and RTS smoothing.
- `/Volumes/Asylum/dev/linoss-dynamics/src/linoss_dynamics/fit.py` fits
  oscillator state-space model parameters.
- `/Volumes/Asylum/dev/linoss-dynamics/src/linoss_dynamics/continuous.py`
  handles exact damped oscillator stepping over irregular time intervals.
- `/Volumes/Asylum/dev/linoss-dynamics/README.md` and
  `/Volumes/Asylum/dev/linoss-dynamics/docs/architecture.md` explicitly keep
  active-inference runtimes, metacognitive policy, event buses, graph databases,
  and host adapters outside the core.

Adapter posture:

- Use linoss-dynamics to supply trajectory, damping, stability, energy, and
  latent-state signals that can inform basin movement.
- Do not treat it as an attractor-basin runtime, POMDP package, or
  metacognitive controller.

Metadata:

- Package `linoss-dynamics`, version `0.2.0`.
- License MIT.
- Core dependency is `numpy`; `scipy` is optional under probabilistic extras.
- Provenance states it is an original NumPy implementation inspired by
  LinOSS/D-LinOSS with no upstream code copied.

## Adapter Priority

1. Elume adapter: highest value for ThoughtSeed and EFE competition.
2. Sakshi adapter: highest value for validation, gates, and witness traces.
3. linoss-dynamics adapter: valuable when basin movement needs real trajectory
   or stability math.
4. Autonoesis adapter: use carefully for self-model/meta-awareness context, not
   for generic metacognitive control.

## Cleanup Source-Of-Truth

Current package rule:

- hard dependencies: none of the adjacent packages,
- optional future adapters: Elume, Sakshi, linoss-dynamics, Autonoesis,
- semantic ownership stays with the package that already owns the concept.

This avoids turning `dionysus-metacognition` into a grab-bag. It remains the
portable control and provenance layer that can speak to the rest of the stack.
