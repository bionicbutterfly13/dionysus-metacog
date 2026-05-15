# Source Inventory

This inventory is the cleanup list for Dionysus Metacognition. It distinguishes
current source-of-truth inputs from historical material, adapter targets, and
missing or stale references.

Scan scope for this pass:

- Included: `/Volumes/Asylum/repos`
- Included: `/Volumes/Asylum/dev`
- Excluded: any `Sync` or `sync` directory

## Source-Of-Truth Rules

- Current package source of truth: files under this repository's `src/`,
  `tests/`, and `docs/`.
- Host runtime source of truth: the live host repo that owns runtime behavior.
  For current Dionysus behavior, that is `/Volumes/Asylum/dev/dionysus3`.
- Prior-version evidence: older repos such as
  `/Volumes/Asylum/repos/Dionysus2.0` can inform lineage and compatibility, but
  should not override current live code without a deliberate migration decision.
- Historical research/prototype evidence: use for model lineage and examples,
  not as direct runtime dependency.
- Missing paths: record them as unresolved inventory, not as available source.

## Current Package

| Path | Role | Cleanup status |
| --- | --- | --- |
| `/Volumes/Asylum/dev/dionysus-metacog/src/dionysus_metacog/attractors/__init__.py` | Current attractor state, basin, transition, assessment, and control policy implementation | Source of truth for package attractor API |
| `/Volumes/Asylum/dev/dionysus-metacog/src/dionysus_metacog/models/__init__.py` | Current POMDP and Markov blanket records | Source of truth for package model records |
| `/Volumes/Asylum/dev/dionysus-metacog/src/dionysus_metacog/core/__init__.py` | Current portable signal and payload contract | Source of truth for package handoff payload |
| `/Volumes/Asylum/dev/dionysus-metacog/src/dionysus_metacog/provenance/__init__.py` | Current source reference and ledger contract | Source of truth for attribution and lineage |
| `/Volumes/Asylum/dev/dionysus-metacog/docs/thoughtseed-attractor-map.md` | Audit result for ThoughtSeed-to-attractor relationship | New cleanup artifact |
| `/Volumes/Asylum/dev/dionysus-metacog/docs/cross-package-boundary-map.md` | Audit result for Autonoesis, Elume, Sakshi, and linoss-dynamics ownership boundaries | Source of truth for adjacent package adapter posture |

## Current Host Evidence

| Path | What it proves | Cleanup disposition |
| --- | --- | --- |
| `/Volumes/Asylum/dev/dionysus3/api/models/thought.py` | Current D3 `ThoughtSeed` shape: layer, blanket tag, activation, competition status, dominant basin, mineness, source, observability, SOHM conversion | Adapter target, not package dependency |
| `/Volumes/Asylum/dev/dionysus3/api/services/thoughtseed_competition_service.py` | Current D3 competition route and winner handling | Adapter behavior reference |
| `/Volumes/Asylum/dev/dionysus3/api/services/thoughtseed_integration.py` | Current D3 boundary/provider facade for seed generation and basin activation | Preferred integration pattern |
| `/Volumes/Asylum/dev/dionysus3/api/services/narrative_intake_service.py` | Current narrative path from text segments to ThoughtSeeds, dominant basins, persistence, and memory routing | Adapter test fixture source |

## Prior-Version Evidence

| Path | What it proves | Cleanup disposition |
| --- | --- | --- |
| `/Volumes/Asylum/repos/Dionysus2.0/backend/src/models/clause/thoughtseed_models.py` | Older `ThoughtSeed` as document-linking object carrying basin context | Historical compatibility shape |
| `/Volumes/Asylum/repos/Dionysus2.0/backend/src/services/thoughtseed/generator.py` | Older seed generation, Redis cache, Neo4j persistence, and document linking | Historical implementation reference |
| `/Volumes/Asylum/repos/Dionysus2.0/backend/src/models/attractor_basin.py` | Older rich basin model with state, activation, field influence, layer influence, ThoughtSeed associations, energy, and coherence | Candidate field vocabulary for future adapters |
| `/Volumes/Asylum/repos/Dionysus2.0/extensions/context_engineering/attractor_basin_dynamics.py` | Older seed-to-basin integration with reinforcement, competition, synthesis, and emergence | Strong lineage for lifecycle mapping |
| `/Volumes/Asylum/repos/Dionysus2.0/specs/028-thoughtseed-bulk-processing/spec.md` | Older intended graph relation `(:ThoughtSeed)-[:ATTRACTED_TO]->(:AttractorBasin)` | Confirms conceptual relationship |
| `/Volumes/Asylum/repos/Dionysus2.0/EXTRACTION_SUMMARY.md` | Claims extracted `thoughtseed-active-inference` package under `/Volumes/Asylum/dev/thoughtseeds` | Historical note; target path missing locally |

## Prototype And External-Package Evidence

| Path | What it proves | Cleanup disposition |
| --- | --- | --- |
| `/Volumes/Asylum/repos/thoughtseeds_vipassana/README.md` | Prototype is tied to "Thoughtseeds Framework: A Hierarchical and Agentic Framework for Investigating Thought Dynamics in Meditative States" by Prakash Chandra Kavi, Gorka Zamora-Lopez, Daniel Ari Friedman, and Gustavo Patow | Cite as paper/prototype lineage |
| `/Volumes/Asylum/repos/thoughtseeds_vipassana/thoughtseed_network.py` | ThoughtSeeds as activation agents competing in a global workspace | Prototype lineage only; do not copy code without license review |
| `/Volumes/Asylum/repos/thoughtseeds_vipassana/learning_thoughtseeds_revised.py` | State-specific attractors shape ThoughtSeed activations | Prototype lineage only; do not copy code without license review |
| `/Volumes/Asylum/repos/metatotai/docs/extraction-plan.md` | ThoughtSeed should be an optional adapter target, not a core dependency | Supports package boundary |

## Adjacent Package Boundary Evidence

| Path | What it proves | Cleanup disposition |
| --- | --- | --- |
| `/Volumes/Asylum/dev/autonoesis` | Owns self-modeling, computational phenomenology, meta-awareness, metacognitive feelings, transparency/opacity, agency, and ownership | Keep ontology in Autonoesis; use adapter only for self-model/meta-awareness context |
| `/Volumes/Asylum/dev/elume` | Owns immutable ThoughtSeed records, EFE-style competition, prior-gated cognition, curiosity scoring, and replayable competition operations | Optional deterministic cognition adapter; no hard dependency |
| `/Volumes/Asylum/dev/sakshi` | Owns witness/gating/verification surfaces, expectation checking, write guards, plan soundness, intervention validation, and monitor-assess-control flow | Optional witness/gate adapter; do not move host policy into Sakshi |
| `/Volumes/Asylum/dev/linoss-dynamics` | Owns oscillator trajectories, stability diagnostics, energy/convergence signals, Kalman filtering, smoothing, and fitted latent dynamics | Optional numerical substrate for basin movement; no metacognitive policy ownership |

## Missing Or Unresolved

| Path or item | Status | Next cleanup action |
| --- | --- | --- |
| `/Volumes/Asylum/dev/thoughtseeds` | Not present on disk during this pass | Locate package elsewhere or remove stale references from future plans |
| `thoughtseed-active-inference` package | Mentioned by Dionysus2.0 extraction notes, not verified locally | Check PyPI/GitHub only if needed before adapter work |
| Thoughtseeds Vipassana prototype license | GitHub repository metadata reports `license: null`; no local LICENSE file found; raw `LICENSE` URLs returned 404; paper is CC BY 4.0 but code has no explicit software license | Treat as design evidence only until software license is verified |
| Autonoesis stale-shadow risk | `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models.py` duplicates the active package directory `/Volumes/Asylum/dev/autonoesis/src/autonoesis/models/` | Track in Autonoesis cleanup, not this package |
| Sakshi README version drift | Sakshi package metadata says `0.12.0`; README status still says `0.11.0 pre-1.0` | Track in Sakshi cleanup, not this package |

## Cleanup Decisions So Far

1. Keep `dionysus-metacognition` core host-neutral.
2. Do not add a first-class package-owned `ThoughtSeed` model yet.
3. Add a future `ThoughtSeedLike` adapter/protocol if we need direct ingestion.
4. Treat Dionysus3 as the current host runtime for adapter compatibility.
5. Treat Dionysus2.0 as lineage and migration evidence.
6. Treat missing extraction paths as unresolved until verified.
7. Treat the Thoughtseeds Vipassana prototype as attributed paper/prototype
   lineage only unless code reuse is explicitly cleared.
8. Keep adjacent packages out of core dependencies; add optional adapters only
   when tests prove a stable translation boundary.

## Next Inventory Pass

Before implementing adapters:

1. Start with Elume for ThoughtSeed/EFE competition.
2. Add Sakshi next for witness/gating validation.
3. Add linoss-dynamics only when basin movement needs trajectory/stability math.
4. Add Autonoesis only for self-model/meta-awareness context.
5. Locate any restored `thoughtseed-active-inference` repo/package before
   referencing it as available source.
