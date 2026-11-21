# Target-lock age experiment — 2026-11-21

Base: production `main` at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
Working branch: `experiment/fresh-targets-20261121-1740`.
Behavior commit: `590e4b50c7327a51273202d01145279fd3ef704d`.
Test commit: `b7acb62f76cc97ca86dff469bb599bbd1deb15bd`.
Benchmark workflow commit: `a9dc6d45422720665bacf8c9e530d9bba529c6c7`.

Hypothesis: Stop offensively pursuing tracks older than 1.2 s or 0.3 s while continuing to remember them for defensive avoidance. The baseline 5.2 s target window is the original policy. `MECH_TUNE` controls the window; defaults are unchanged.

Independent MIT-licensed simulator pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Each variant is paired on the same seeds per opponent policy: 16 cooperative 15-opponent squad matches from seed 421121; eight free-for-all lobbies from seed 881121, with eight copies of our policy per lobby. Opponents `tools.baseline.brain_v1` and `tools.baseline.brain_v2`. Scores are mean `16 - place` points; **not official** organizer hidden/practice scores.

| Offensive lock age | Squad v1 | FFA v1 | Squad v2 | FFA v2 |
| --- | ---: | ---: | ---: | ---: |
| 5.2 s (control) | 0.12 | 8.20 | 0.06 | 6.81 |
| 1.2 s | 0.38 | 7.95 | 0.12 | 6.70 |
| 0.3 s | 0.25 | 7.78 | 0.25 | 6.98 |
| Difference 1.2 vs control | +0.26 | -0.25 | +0.06 | -0.11 |
| Difference 0.3 vs control | +0.13 | -0.42 | +0.19 | +0.17 |

**Decision: reject and do not promote.** Slight squad improvement does not justify FFA damage, especially on v1. The 0.3-s variant reverses between FFA opponents. The simulator's approximation cannot guarantee official robustness; FFA hero copies are correlated within lobby, so 8 lobbies rather than 64 independent units.

All six placement jobs passed; the unit and native/Docker conformance checks passed. No changes to `main`, previously submitted history, or official tournament entries.

Benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44890560116
Conformance: https://github.com/pucaru/curly-succotash/actions/runs/44890560106
