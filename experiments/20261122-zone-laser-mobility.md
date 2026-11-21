# Urgent safe-zone travel versus laser-charge movement penalty — 22 November 2026

**Status: 144-game independent screen not yet evaluated.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`, no official 48-match score known, no tournament submission or production edit.

## Causal mechanism

Official laser charge slows mech movement to half speed. Production `aim_and_fire()` can continue charging the laser even when `choose_goal()` has set an urgent safe-zone return. This is a control inconsistency: evasive boost attempts to maximize movement, while laser charge halves it. Experiment **only** suppresses secondary laser charge/recharge while `urgent=True`, leaving primary gun, target selection, normal combat, and all nonurgent gameplay unchanged. A charged laser may release if already winding up. `MECH_TUNE.zone_laser_mobility=0` reproduces production; `1` activates the candidate.

## Preregistered evaluation

Pinned MIT independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, an approximation, NOT the official practice engine. Each of v1, v2, mixed opponents: 12 new paired squad seeds 1910211–1910222, 12 new paired one-hero FFA seeds 1920211–1920222, ×2 toggle variants = 144 games. Paired mean placement, 95% seed bootstrap interval, W/L/T, low results (≤2 pts), rear damage, out-zone time, and squad early deaths/stuck/survival reported. Compare identical opponent and spawn seeds. Native 300-observation and Docker sandbox conformance must pass. All six subgroups must have nonnegative mean placement, no low-result rise, and FFA rear/zone safety regressions for further consideration.

If screen passes, independently hold out ≥64 fresh FFA + ≥32 squad paired matches **for each opponent population**, verify endgame and protocol in the same tested commit before any contemplated production proposal. Do not promote based on local FFA average >6. No official submission, main branch changes, history rewrites, or copied competitor code/research.
