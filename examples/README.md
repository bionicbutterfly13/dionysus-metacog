# Host Runtime Examples

These examples show how a host can use `dionysus-metacognition` without taking
hard dependencies on Elume, linoss-dynamics, Autonoesis, or Sakshi. Each script
uses small host-shaped dataclasses or dictionaries, runs from a clean install,
and prints JSON-safe output.

## Run

```bash
python examples/host_runtime_pipeline.py
python examples/elume_to_sakshi.py
python examples/linoss_state_input.py
```

## Examples

| File | Shows |
| --- | --- |
| `host_runtime_pipeline.py` | Elume-shaped ThoughtSeed input, linoss-shaped filter output, Autonoesis-style self-model context, and Sakshi-style guard/witness output |
| `elume_to_sakshi.py` | ThoughtSeed winner to `AttractorAssessment`, then Sakshi write-guard and dominant ThoughtSeed snapshot payloads |
| `linoss_state_input.py` | linoss-shaped trajectory and filter dictionaries feeding attractor/POMDP records and payloads |

The important boundary is structural compatibility: hosts can pass objects with
the required fields, and adapters return package-native records and payloads.
