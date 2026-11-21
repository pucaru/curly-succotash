# Holding-point threat repulsion A/B — 2026-11-21

Base production `main@60b5438af4d45af989f63bffcbe0b03250a23ae4`. A guarded `hold_evasion_radius` option, default 0 (original behavior), stops suppressing evasive steering after arriving at the holding waypoint if recently attacked or nearby enemies have been tracked. It does not change the default production policy. Behavior commit `a484b50051dc769d6444fb4b73681eec5e9e3b27`, regression tests `7713732b0b801cea41a3ae0e9690da9cb686381b`, benchmark `90c3bddf89b7ed89f6864028016d8659ccebb093`.

Pinned MIT-licensed independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Paired new seeds: 24 cooperative squad matches starting 330621 and twelve eight-hero FFA lobbies starting 550621 for each of two distinct opponent policies. Scores: mean `16 - place` (local approximate, **not official**).

| Hold evasion radius | Squad v1 | FFA v1 | Squad v2 | FFA v2 |
| ---: | ---: | ---: | ---: | ---: |
| 0 (control) | 0.42 | 8.01 | 0.08 | 6.56 |
| 130 | 0.33 | 8.02 | 0.00 | 6.89 |
| 200 | 0.33 | 8.19 | 0.08 | 6.66 |
| Δ at 130 | -0.09 | +0.01 | -0.08 | +0.33 |
| Δ at 200 | -0.09 | +0.18 | 0.00 | +0.10 |

Decision: **do not promote either globally enabled setting**. Both diminish practice-squad performance in at least one opponent profile. FFA improvements are small/variable and derive from correlated hero copies within 12 lobbies. A dedicated FFA-only condition, if separately measured, is a different hypothesis and is not validated here.

All six benchmark jobs completed successfully and tests plus default-configuration native/Docker conformance passed. Production and submitted commit history unchanged.

Benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44891586772
Conformance: https://github.com/pucaru/curly-succotash/actions/runs/44891586664
