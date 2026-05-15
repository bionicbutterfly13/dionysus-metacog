import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def _load_example(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_host_runtime_pipeline_builds_guarded_payload() -> None:
    build_host_pipeline_output = _load_example(
        "host_runtime_pipeline"
    ).build_host_pipeline_output
    output = build_host_pipeline_output()

    payload = output["payload"]
    assert payload["payload_type"] == "metacog.attractor_assessment"
    assert payload["context"]["autonoesis_self_model"]["subject_id"] == (
        "agent-runtime"
    )
    assert output["control_action"]["target"] == "source-risk"
    assert output["guard_payload"]["requires_guard"] is True
    json.dumps(output)


def test_elume_to_sakshi_example_builds_guard_payload() -> None:
    build_guard_payload = _load_example("elume_to_sakshi").build_guard_payload
    output = build_guard_payload()

    guard_payload = output["guard_payload"]
    assert guard_payload["source_origin"] == "dionysus-metacognition"
    assert guard_payload["control_action"]["target"] == "license-risk"
    assert output["np_state_snapshot"]["dominant_thoughtseed_id"] == (
        "seed-license-risk"
    )
    json.dumps(output)


def test_linoss_state_input_example_builds_payloads() -> None:
    build_linoss_payloads = _load_example("linoss_state_input").build_linoss_payloads
    output = build_linoss_payloads()

    assert output["direct_payload"]["context"]["basin_id"] == "trajectory-basin"
    assert output["elume_like_payload"]["signal"]["metadata"]["basin_id"] == (
        "trajectory-basin"
    )
    assert output["elume_like_payload"]["signal"]["metadata"]["policy"] in {
        "hold",
        "stabilize",
        "escalate",
    }
    json.dumps(output)


def test_examples_run_as_scripts() -> None:
    for example in (
        "host_runtime_pipeline.py",
        "elume_to_sakshi.py",
        "linoss_state_input.py",
    ):
        result = subprocess.run(
            [sys.executable, str(EXAMPLES / example)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert json.loads(result.stdout)
