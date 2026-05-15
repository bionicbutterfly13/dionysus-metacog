# ThoughtSeed To Attractor Map

This note records the local audit behind the package's future ThoughtSeed
adapter seam. The scan included `/Volumes/Asylum/repos` and
`/Volumes/Asylum/dev`; `Sync` and `sync` directories were excluded.

## Core Distinction

A ThoughtSeed is not an attractor.

A ThoughtSeed is a seed of activation: a content-bearing candidate, trace, or
agent-like unit that can enter competition, link documents, carry provenance,
or activate a cognitive path. An attractor or basin is the organizing state
structure that pulls seeds into a stable pattern, records basin strength, and
selects the control response.

In this package, ThoughtSeeds should therefore arrive through adapters. The
core package should continue to model the basin, lifecycle transition, POMDP
record, Markov blanket record, provenance ledger, and emitted metacognitive
payload.

## Evidence By Source

### Vipassana Prototype

The prototype is tied to the paper "Thoughtseeds Framework: A Hierarchical and
Agentic Framework for Investigating Thought Dynamics in Meditative States" by
Prakash Chandra Kavi, Gorka Zamora-Lopez, Daniel Ari Friedman, and Gustavo
Patow. GitHub repository metadata reported no detected software license, the
local checkout did not contain a LICENSE file, and raw LICENSE URLs returned
404 during this audit. The paper is CC BY 4.0, but the code repository has no
explicit software license, so this package treats it as cited design lineage
only. Do not copy or adapt code from that prototype without a separate
licensing and attribution pass.

`/Volumes/Asylum/repos/thoughtseeds_vipassana/thoughtseed_network.py` models
ThoughtSeeds as individual agents with activation dynamics. The network updates
each seed's activation, tracks dominant seeds in a global workspace, and exposes
state-level features such as distraction and meditation quality.

`/Volumes/Asylum/repos/thoughtseeds_vipassana/learning_thoughtseeds_revised.py`
uses state-specific attractors to adjust the weights of seed activations. That
is the earliest clean pattern: seeds move; attractors organize the movement.

### Dionysus2.0 Prior Versions

`/Volumes/Asylum/repos/Dionysus2.0/backend/src/models/clause/thoughtseed_models.py`
defines a document-linking `ThoughtSeed` with a concept, source document,
basin context, similarity threshold, linked documents, and timestamp. Here the
seed is a cross-document linking object, and the basin context is carried as
input state.

`/Volumes/Asylum/repos/Dionysus2.0/backend/src/services/thoughtseed/generator.py`
creates those seeds from concepts, attaches basin context, finds similar
documents, stores nodes in Neo4j, and caches seed records in Redis. This is a
retrieval/linking implementation, not a metacognitive controller.

`/Volumes/Asylum/repos/Dionysus2.0/backend/src/models/attractor_basin.py`
defines the richer attractor side: basin type, state, stability, depth, width,
activation threshold, current activation, neural-field influence, consciousness
contribution, ThoughtSeed associations, layer influences, memory trace, energy,
dissipation, convergence, and coherence. This is the organizing landscape.

`/Volumes/Asylum/repos/Dionysus2.0/extensions/context_engineering/attractor_basin_dynamics.py`
is the strongest prior-version bridge. It integrates a new ThoughtSeed into a
basin landscape and classifies the influence as reinforcement, competition,
synthesis, or emergence. Those map naturally to this package's lifecycle terms:

| Dionysus2.0 influence | Meaning | Current lifecycle fit |
| --- | --- | --- |
| `REINFORCEMENT` | Seed strengthens an existing basin | `held` or stronger `stabilize` assessment |
| `COMPETITION` | Seed creates pressure against an existing basin | `escaped` or `destabilized` |
| `SYNTHESIS` | Seed merges with a basin and broadens it | `merged` |
| `EMERGENCE` | Seed creates a new basin | `entered` |

`/Volumes/Asylum/repos/Dionysus2.0/specs/028-thoughtseed-bulk-processing/spec.md`
also preserves an older propagation model: seeds have semantic encodings,
target basins, propagation hops, status, related seeds, and emergent patterns;
Neo4j stores `(:ThoughtSeed)-[:ATTRACTED_TO]->(:AttractorBasin)` edges. This is
direct evidence that the intended relationship is attraction into basins, not
identity with basins.

The Dionysus2.0 extraction note says a separate
`/Volumes/Asylum/dev/thoughtseeds` package once held `thoughtseed-active-inference`
components, including `AttractorBasinManager`, `BasinInfluenceType`, and
`NeuronalPacket`. That path is not present on this machine, so it is historical
evidence only unless the package is restored.

### Current Dionysus3

`/Volumes/Asylum/dev/dionysus3/api/models/thought.py` defines the current
`ThoughtSeed` as a Pydantic cognitive processing unit with:

- `layer`
- `blanket_tag`
- `content`
- `activation_level`
- `competition_status`
- parent/child thought links
- `dominant_basin`
- `mineness`
- perception, epistemic value, and opacity observability fields
- `source_id`

It can reinforce winners and losers, spawn children, persist to Neo4j, and
convert itself into a SOHM state. This confirms that the current seed is a
competitive, recursive candidate with boundary and provenance metadata.

`/Volumes/Asylum/dev/dionysus3/api/services/thoughtseed_competition_service.py`
runs seed competition through an external provider, cognition boundary, local
fallback, SOHM ignition detection, or BounceGrad. Winning seeds then trigger
basin activation through the integration service. This keeps competition
separate from basin organization.

`/Volumes/Asylum/dev/dionysus3/api/services/thoughtseed_integration.py`
is already a boundary facade. It delegates generation, winner-based basin
activation, and prediction competition to external providers or the cognition
boundary. This is the correct integration posture for this package too: adapter
first, no hard D3 dependency.

`/Volumes/Asylum/dev/dionysus3/api/services/narrative_intake_service.py`
creates narrative-born ThoughtSeeds from text segments, classifies their layer,
computes activation, assigns a dominant basin, persists them to Neo4j, and
routes the raw narrative through the memory basin router. This is a concrete
runtime path where a ThoughtSeed becomes a basin-facing control input.

### MetaToTAI Boundary

`/Volumes/Asylum/repos/metatotai/docs/extraction-plan.md` treats
`elume.models.thought.ThoughtSeed` as an optional promotion adapter target.
The core Meta-ToT package emits neutral promoted-path records; adapters may
turn those into ThoughtSeed candidates. That supports the same design choice
here: keep the core package neutral, and add a small adapter/protocol layer
for host-specific ThoughtSeed shapes.

### Elume Boundary

`/Volumes/Asylum/dev/elume/src/elume/models/thought.py` now confirms that Elume
has its own immutable `ThoughtSeed` model, including thought layers, Markov
blanket tags, activation, basin/source metadata, reinforcement, and child-spawn
semantics. Elume also owns deterministic thought competition, EFE-style result
records, prior-gated cognition, curiosity scoring, and replayable envelope
operations.

That makes Elume the strongest optional adapter target for actual ThoughtSeed
execution. It does not change this package's core rule: `dionysus-metacognition`
should translate Elume outputs into `AttractorAssessment` and `MetaCogPayload`,
not import Elume as a required runtime dependency.

## Mapping Into Dionysus Metacognition

| ThoughtSeed field or behavior | Package target |
| --- | --- |
| seed ID | provenance/context metadata, not `source_id` by itself |
| `source_id` | `SourceReference.source_id` when it names the source; otherwise context metadata |
| `content` or `concept` | `AttractorState.metadata["content"]` or adapter context |
| `activation_level` | salience input; may influence novelty, stability, or expected free energy |
| `layer` | boundary/model metadata; can help choose hidden state or blanket partition |
| `blanket_tag` | `MarkovBlanketRecord` adapter input |
| `dominant_basin` | `AttractorState.basin_id` or `AttractorBasin.basin_id` |
| `competition_status` | lifecycle/control context |
| winner selection | trigger for `AttractorAssessment` |
| EFE, VFE, precision | `PomdpStateRecord.expected_free_energy` and `precision` |
| basin influence type | `AttractorTransitionLabel` plus selected control policy |

## Recommended Adapter Shape

Do not add a first-class `ThoughtSeed` model to the core package yet. That
would force this package to choose between several host meanings: meditation
agent, document-linking node, recursive D3 thought object, or Elume adapter
target.

Instead, add a lightweight protocol and converter later:

```python
class ThoughtSeedLike(Protocol):
    id: object
    content: str
    activation_level: float
    source_id: str | None
    dominant_basin: str | None
```

Then expose adapter functions that accept protocol-shaped objects or plain
dicts and return existing core records:

- `thoughtseed_to_attractor_state(...)`
- `thoughtseed_to_pomdp_record(...)`
- `thoughtseed_to_markov_blanket(...)`
- `thoughtseed_winner_to_assessment(...)`

That keeps `dionysus-metacognition` Hermes-compatible and D3-compatible without
making either runtime a dependency.

## Practical Lifecycle

1. A host creates or receives a ThoughtSeed.
2. The seed enters competition or salience scoring.
3. A winner or high-salience seed points toward a dominant basin.
4. The adapter converts that seed plus runtime evidence into:
   - `AttractorState`
   - `PomdpStateRecord`
   - optional `MarkovBlanketRecord`
   - provenance/context metadata
5. `AttractorAssessment` selects the control policy:
   `hold`, `explore`, `attenuate`, `stabilize`, or `escalate`.
6. `MetaCogPayload` carries the result back to the host runtime.

The clean conceptual rule is: ThoughtSeeds activate, compete, and point;
attractors organize, stabilize, and govern.
