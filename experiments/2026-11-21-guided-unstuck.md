# Terrain-guided stall recovery, independent A/B (2026-11-21)

Base: main at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
Experiment branch: `experiment/guided-unstuck-20261121-1630`, benchmark commit `db4db3b20cdeff37692cb694400d5ede16fadc85`.

An opt-in `guided_unstuck` flag tests choosing a short open corridor in the terrain when repeated movement stalls, rather than taking the existing random escape heading. The default preserves the production policy.

Independent MIT-licensed simulator with paired new seeds: cooperative 15-opponent squad, 12 games with seed 208101; FFA, 6 lobbies with seed 550981. Two opponent policies: `tools.baseline.brain_v1` and `tools.baseline.brain_v2`. All values are mean placement points (16 - place), **not** official hidden practice scores.

| Guided | Squad v1 | FFA v1 | Squad v2 | FFA v2 |
| --- | ---: | ---: | ---: | ---: |
| Off (control) | 0.25 | 7.73 | 0.33 | 6.90 |
| On | 0.33 | 8.06 | 0.25 | 6.79 |
| Difference | +0.08 | +0.33 | -0.08 | -0.11 |

Decision: **do not promote**. A modest gain in v1 reverses in v2, which undermines robustness. The experiment is still useful as a test of stall handling, but not evidence of a general placement improvement. FFA lobbies have correlated hero copies; no independent official score has been established.

All unit tests passed; native and container checks each answered 300/300 observations within 50 ms, no misses. Main and prior submitted history remain unchanged.

Benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44885326522
Conformance: https://github.com/pucaru/curly-succotash/actions/runs/44885326508
