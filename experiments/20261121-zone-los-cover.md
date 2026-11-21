# Threat line-of-sight-aware safe-zone holding — controlled experiment (21 November 2026)

**Status:** Screening launched. No score outcome, holdout result or promotion claimed.

Production base `60b5438af4d45af989f63bffcbe0b03250a23ae4`; changes remain exclusively on an isolated experiment branch. No reversion, submitted history rewrite or former removed research section.

## Design rationale
The current holding-site planner approximates cover by nearby walls and distance from tracked enemies. A cell next to a wall can nevertheless be exposed to a visible shooter. We test a limited geometric line-of-sight penalty to four nearby, recently tracked opponents **only when choosing a fresh safe-zone hold target**, retaining original combat, movement, emergency routing, and late-zone logic.

Hypothesis: favoring positions with solid obstacles directly between nearby opponents and the holding site reduces exposed stationary time, rear damage and early deaths. Raycasting on 2D wall footprints is only a proxy for actual eye-height visibility; false safe or unsafe decisions are possible.

Tunable `MECH_TUNE.zone_los_penalty`: 0 (exact production control), 55 and 125 positioning-score units. Bounded maximum four threat raycasts per candidate; zero default leaves old behavior and no additional raycasts.

## Reproducible matched-seed screen
Independent MIT-licensed proxy simulator at pinned commit `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Not the official practice/final engine. 24 **new** squad seeds 973911–973934 and 24 one-hero FFA seeds 983911–983934 for every penalty × v1/v2/mixed opponent type; 432 matches and nine CI jobs. Same seeds for all variants; one tested bot per FFA lobby.

Report paired placement change, early FFA deaths (≤2 points), rear damage, outside-zone time and maximum latency. Reject any candidate that worsens *any* opponent/mode mean, increases early FFA deaths or zone exposure. If it passes screening, require an independent holdout of ≥64 new FFA and ≥32 squad seeds *per opponent type*, final-circle audit, native protocol and Docker conformance before any production promotion.

All competitor study remains off-repository, no copied competitor code or public research material included. No official submission authorized.


## Verified screening audit

[All nine matrix cells, all 432 simulations and aggregate completed successfully](https://github.com/pucaru/curly-succotash/actions/runs/44911868217). Native, unit and [Docker conformance passed](https://github.com/pucaru/curly-succotash/actions/runs/44911868170). Maximum observed local proxy decision time 7.66ms. No official practice score or final robustness measured.

The launched aggregate printed the correct numeric column sequence from `VALUES=(0,55,125)` but had column labels 55 and 0 transposed. The correctly labeled verified results are recorded below; the aggregator heading was repaired.

| Opponents | Control squad | Control FFA | 55 squad | 55 FFA | 125 squad | 125 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.333 | 8.292 | 0.333 | 8.208 | 0.333 | 8.208 |
| v2 | 0.167 | 7.458 | 0.125 | 7.292 | 0.167 | 7.083 |
| mixed | 0.375 | 8.042 | 0.333 | 8.125 | 0.542 | 8.250 |

**55 rejected:** FFA changes v1 -0.083, v2 -0.167, mixed +0.083. Squad v2/mixed each -0.042; v2 outside-zone time +0.31s, rear damage +86.2.

**125 rejected:** FFA changes v1 -0.083, v2 **-0.375**, mixed +0.208. Squad mixed +0.167, v1 unchanged, v2 unchanged; v2 rear damage reduces -192.6 and early FFA deaths 4→3, but these secondary benefits do not compensate for a -0.375 placement regression in the stronger FFA profile. Matched v2 FFA 6 wins/11 losses/7 ties. Mean FFA mixed rear damage increases +40.7.

**Decision:** neither variant advances to fresh-seed holdout or main. An improved local cover proxy is not itself a verified placement improvement. Preserve production and existing submitted commits.
