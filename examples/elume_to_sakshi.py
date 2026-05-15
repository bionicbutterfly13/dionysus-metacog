"""Convert an Elume-shaped winner into Sakshi-shaped guard payloads."""

from __future__ import annotations

import json
from dataclasses import dataclass

from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.sakshi import (
    meta_payload_to_write_guard_payload,
    signal_to_np_state_snapshot,
)


@dataclass(frozen=True)
class ThoughtSeed:
    id: str = "seed-license-risk"
    content: str = "The prototype has no explicit software license"
    activation_level: float = 0.82
    layer: str = "metacognitive"
    blanket_tag: str = "internal"
    dominant_basin: str | None = "license-risk"
    source_id: str | None = "thoughtseeds-vipassana-audit"


@dataclass(frozen=True)
class EFEResult:
    hidden_state: str = "license-risk"
    observation: str = "code-reuse-request"
    policy: str = "stabilize"
    expected_free_energy: float = 0.68
    precision: float = 0.58


def build_guard_payload() -> dict[str, object]:
    assessment = thoughtseed_winner_to_assessment(
        ThoughtSeed(),
        EFEResult(),
        source_ids=("elume-thought-competition",),
    )
    payload = assessment.to_payload()
    payload.signal.metadata["thoughtseed_id"] = ThoughtSeed().id
    return {
        "guard_payload": meta_payload_to_write_guard_payload(payload),
        "np_state_snapshot": signal_to_np_state_snapshot(payload.signal),
    }


def main() -> None:
    print(json.dumps(build_guard_payload(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
