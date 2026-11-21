# Early cover recovery thresholds — 21 November 2026

Base: `main@60b5438af4d45af989f63bffcbe0b03250a23ae4`. No production code was changed. The benchmark toggles existing `cover_hp` and `hurt_cover_hp` parameters through `MECH_TUNE`.

Paired new-seed evaluation in the pinned MIT-licensed independent simulator: 24 practice-squad matches from seed 230621 and 12 eight-hero FFA lobbies from seed 440621 per opponent profile, against v1 and v2 separately. Metric is mean `16 - place` placement points, **not official scoring**.

| Cover thresholds (cover HP / hurt cover HP) | Squad v1 | FFA v1 | Squad v2 | FFA v2 |
| --- | ---: | ---: | ---: | ---: |
| 0.47 / 0.75 (control) | 0.50 | 7.59 | 0.17 | 7.21 |
| 0.72 / 0.96 (gradual) | 0.33 | 7.95 | 0.08 | 6.67 |
| 0.90 / 0.995 (proactive) | 0.50 | 7.33 | 0.21 | 6.52 |
| Gradual minus control | -0.17 | +0.36 | -0.09 | -0.54 |
| Proactive minus control | 0.00 | -0.26 | +0.04 | -0.69 |

Decision: **reject both variants**. The small FFA v1 gain on the gradual variant reverses sharply on the independent v2 policy and squad scores fall. Proactive policy reduces FFA survival in both profiles. All six benchmark jobs succeeded and all available syntax/unit/native/Docker conformance checks passed. No change to the submitted `main` branch.

Benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44891412665
Conformance: https://github.com/pucaru/curly-succotash/actions/runs/44891412471

FFA scores derive from eight clone heroes per lobby (12 correlated lobbies). Results are local diagnostics only.
