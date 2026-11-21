# Urgent safe-zone travel versus laser-charge movement penalty — 22 November 2026

**Status: 144-game independent screen not yet evaluated.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`, no official 48-match score known, no tournament submission or production edit.

## Causal mechanism

Official laser charge slows mech movement to half speed. Production `aim_and_fire()` can continue charging the laser even when `choose_goal()` has set an urgent safe-zone return. This is a control inconsistency: evasive boost attempts to maximize movement, while laser charge halves it. Experiment **only** suppresses secondary laser charge/recharge while `urgent=True`, leaving primary gun, target selection, normal combat, and all nonurgent gameplay unchanged. A charged laser may release if already winding up. `MECH_TUNE.zone_laser_mobility=0` reproduces production; `1` activates the candidate.

## Preregistered evaluation

Pinned MIT independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, an approximation, NOT the official practice engine. Each of v1, v2, mixed opponents: 12 new paired squad seeds 1910211–1910222, 12 new paired one-hero FFA seeds 1920211–1920222, ×2 toggle variants = 144 games. Paired mean placement, 95% seed bootstrap interval, W/L/T, low results (≤2 pts), rear damage, out-zone time, and squad early deaths/stuck/survival reported. Compare identical opponent and spawn seeds. Native 300-observation and Docker sandbox conformance must pass. All six subgroups must have nonnegative mean placement, no low-result rise, and FFA rear/zone safety regressions for further consideration.

If screen passes, independently hold out ≥64 fresh FFA + ≥32 squad paired matches **for each opponent population**, verify endgame and protocol in the same tested commit before any contemplated production proposal. Do not promote based on local FFA average >6. No official submission, main branch changes, history rewrites, or copied competitor code/research.


## Final screening audit — 22 November 2026

**REJECTED.** [Complete 144-game paired proxy evaluation, run 44933201533](https://github.com/pucaru/curly-succotash/actions/runs/44933201533), including 12 distinct seeds for each of 6 opponent/mode subgroups ×2 variants and exact seed/placement/diagnostics parser, completed successfully. Evaluated candidate commit: `4b1d859d0a921a0aab10c16874189e96e8b8d88f`. [Candidate 300-observation native + Docker sandbox conformance, run 44933266346](https://github.com/pucaru/curly-succotash/actions/runs/44933266346), passed at commit `31576e6b6ba0a6a4aca9c7ea8767e29e61ef1e58`, which only added the candidate-check workflow after the evaluated code commit; no bot code difference. [Default unit, native and Docker conformance, run 44933201589](https://github.com/pucaru/curly-succotash/actions/runs/44933201589) also passed on evaluated code. An initial CI run failed **before simulations** due to a missing aggregator filename in a workflow reference. Commit `4b1d859d` fixed the filename; no unsuccessful simulation needed rerunning.

| Opponent | Squad control→candidate | One-hero FFA control→candidate | Paired FFA Δ [95% bootstrap CI], W/L/T | FFA rear Δ | FFA zone Δ |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.333→0.333 | 7.667→7.667 | +0.000 [0,0], 0/0/12 | **+7.4** | +0.000s |
| v2 | 0.083→0.250 | 5.417→6.583 | +1.167 [−0.583,+3.167], 5/5/2 | −15.0 | +0.000s |
| mixed | 0.833→0.333 | 5.917→6.583 | +0.667 [−0.417,+2.250], 2/2/8 | −38.3 | +0.000s |

Low finishes (≤2 points): squad v1 12→12, v2 12→12, mixed **11→12**; FFA v1 1→1, v2 **1→3**, mixed 1→1. Additional squad diagnostics: early deaths before 60s mixed **3→5**; mean survival mixed **115.89→84.48s**; v2 mean out-of-zone **3.56→5.13s**, stuck time **10.18→11.83s**. Peak independent proxy FFA decision latency 10.82ms. All values reflect a third-party approximation, not the official 48-match tournament practice evaluation.

The mechanism changes meaningful game outcomes (especially v2 and mixed groups), but fails the no-regression gate in mixed squad placement (−0.500), v2 FFA low finishes (+2), and v1 FFA rear damage (+7.4). The mixed squad survival decrease is a separate safety concern. We therefore do **not** proceed to a larger holdout and do **not** promote the patch to production. The positive v2 FFA sample mean has a wide paired interval and is not reliable enough to compensate for observed losses. The main branch and all prior submitted commits remain unchanged; there was no official practice or tournament submission, and no competitor research/code was committed.
