"""End-to-end host-runtime pipeline example.

Run with:

    python examples/host_runtime_pipeline.py

The example uses host-shaped dataclasses instead of importing Elume,
linoss-dynamics, Autonoesis, or Sakshi. That mirrors the package boundary:
adapters are structural and optional.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from dionysus_metacog.adapters.autonoesis import enrich_payload_with_self_model
from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.linoss import linoss_filter_to_pomdp_record
from dionysus_metacog.adapters.sakshi import (
    meta_payload_to_control_action,
    meta_payload_to_write_guard_payload,
    signal_to_witness_event,
)


@dataclass(frozen=True)
class HostThoughtSeed:
    id: str = "seed-source-risk"
    content: str = "Protect source attribution before adapting prototype code"
    activation_level: float = 0.74
    layer: str = "metacognitive"
    blanket_tag: str = "internal"
    dominant_basin: str | None = "source-risk"
    source_id: str | None = "conversation"


@dataclass(frozen=True)
class HostPhenomenalState:
    salience: float = 0.62
    valence: float = -0.2
    arousal: float = 0.46
    perspective: str = "first_person"
    transparency: str = "partly_opaque"


@dataclass(frozen=True)
class HostAgency:
    confidence: float = 0.81
    intention_strength: float = 0.9
    outcome_match: float = 0.64
    external_override: float = 0.08


@dataclass(frozen=True)
class HostOwnership:
    confidence: float = 0.78
    continuity: float = 0.84
    source_alignment: float = 0.69
    alienation: float = 0.12


@dataclass(frozen=True)
class HostBoundary:
    self_world_separation: float = 0.88
    tool_incorporation: float = 0.22
    social_permeability: float = 0.16


@dataclass(frozen=True)
class HostPerspective:
    vantage: str = "first_person"
    temporal_continuity: float = 0.86
    embodied_anchor: str | None = "breath"


@dataclass(frozen=True)
class HostMetaState:
    agency_precision: float = 0.67
    ownership_precision: float = 0.61
    introspective_access: float = 0.73
    mode: str = "active"


@dataclass(frozen=True)
class HostSelfModel:
    subject_id: str = "agent-runtime"
    phenomenal: HostPhenomenalState = field(default_factory=HostPhenomenalState)
    agency: HostAgency = field(default_factory=HostAgency)
    ownership: HostOwnership = field(default_factory=HostOwnership)
    boundary: HostBoundary = field(default_factory=HostBoundary)
    perspective: HostPerspective = field(default_factory=HostPerspective)
    meta: HostMetaState = field(default_factory=HostMetaState)
    revision: int = 3


def build_host_pipeline_output() -> dict[str, object]:
    """Build an end-to-end host-runtime output bundle."""

    model = linoss_filter_to_pomdp_record(
        {
            "m_f": [[0.2, 0.4], [0.55, 0.7]],
            "P_f": [
                [[0.5, 0.0], [0.0, 0.5]],
                [[0.25, 0.0], [0.0, 0.25]],
            ],
            "loglik": -1.2,
        },
        hidden_state="source-risk",
        observation="trajectory-shifted-toward-source-risk",
        policy="stabilize",
    )
    assessment = thoughtseed_winner_to_assessment(
        HostThoughtSeed(),
        model,
        source_ids=("host-runtime-thought-competition",),
    )
    payload = assessment.to_payload()
    payload.signal.metadata["thoughtseed_id"] = HostThoughtSeed().id
    enriched = enrich_payload_with_self_model(
        payload,
        self_model=HostSelfModel(),
    )
    return {
        "payload": enriched.as_dict(),
        "control_action": meta_payload_to_control_action(enriched),
        "guard_payload": meta_payload_to_write_guard_payload(enriched),
        "witness_event": signal_to_witness_event(enriched.signal),
    }


def main() -> None:
    print(json.dumps(build_host_pipeline_output(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
