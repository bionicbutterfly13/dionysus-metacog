"""Use linoss-shaped numerical output as metacognitive model input."""

from __future__ import annotations

import json

from dionysus_metacog.adapters.elume import thoughtseed_winner_to_assessment
from dionysus_metacog.adapters.linoss import (
    linoss_filter_to_pomdp_record,
    linoss_metrics_to_attractor_state,
)
from dionysus_metacog.attractors import AttractorAssessment


def build_linoss_payloads() -> dict[str, object]:
    trajectory_state = linoss_metrics_to_attractor_state(
        {
            "energy_before": 1.4,
            "energy_after": 0.9,
            "mode": "damped",
        },
        basin_id="trajectory-basin",
    )
    model = linoss_filter_to_pomdp_record(
        {
            "m_f": [[0.1, 0.2], [0.3, 0.5]],
            "P_f": [[[0.3, 0.0], [0.0, 0.3]]],
            "loglik": -0.42,
        },
        hidden_state="trajectory-basin",
        observation="filtered-latent-state",
        policy="hold",
    )
    direct_assessment = AttractorAssessment.from_state(
        state=trajectory_state,
        model=model,
        source_ids=("linoss-trajectory",),
    )

    class ThoughtSeed:
        id = "seed-trajectory"
        content = "Trajectory data suggests the basin is stabilizing"
        activation_level = 0.68
        layer = "dynamics"
        blanket_tag = "sensory"
        dominant_basin = "trajectory-basin"
        source_id = "linoss-filter"

    elume_like_assessment = thoughtseed_winner_to_assessment(
        ThoughtSeed(),
        model,
        source_ids=("linoss-filtered-thoughtseed",),
    )
    return {
        "direct_payload": direct_assessment.to_payload().as_dict(),
        "elume_like_payload": elume_like_assessment.to_payload().as_dict(),
    }


def main() -> None:
    print(json.dumps(build_linoss_payloads(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
