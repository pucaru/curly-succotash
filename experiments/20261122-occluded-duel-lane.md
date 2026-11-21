# Wall-occluded duel movement — independent causal experiment (2026-11-22)

**Status:** SCREEN RUN PENDING. Production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4` remains unchanged; official practice score unmeasured.

## Hypothesis and bounded alternatives

The production bot picks `duel` when a lone target is within 140m with enough HP, even when its own `Arena.clear(..., inflated=False)` detects a solid building between it and the target. In `duel`, steering circles around an occluded target instead of following the navigator, while gun shooting is disabled by its existing visibility test. This can cause a no-damage engagement without reaching a firing lane.

Three modes controlled by `MECH_TUNE={"blocked_duel":x}`:

- `0`: byte-for-byte unchanged branch through the production duel logic (control); all other production features unchanged.
- `1`: when an otherwise valid solo duel is blocked by wall geometry, search up to 36 nearby, safe and walkable waypoints, and select one with direct line-of-sight to the target; if unavailable, return to zone-safe hold.
- `2`: same firing-lane search; if no candidate and target >68m, use the existing navigator to approach until line-of-sight is possible.

The candidate only applies in squad-like inferred mode, and only when the unchanged duel trigger is met and the wall is detected. Candidates do not change target selection, weapon aim, fire, FFA detection, or emergency zone entry. They require both traversable segment and visible firing line, check current/next circle, and hold a valid lane for at most 2.2s to reduce target switching.

## Validation plan

Pinned MIT-licensed independent proxy simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, not equivalent to the private organizer engine.

Use 12 **fresh paired** seeds for each `(squad, one-entrant FFA) × (v1, v2, mixed) × (0,1,2)` cell = 216 simulated matches; squad seeds 1810211–1810222 and FFA 1820211–1820222. All six scenario subgroups must show no negative mean placement, no increase in low finishes (points ≤2), and FFA no increase in mean rear damage or out-of-zone seconds. Report per-group paired deltas, W/L/T, seeded bootstrap 95% confidence intervals, and action latency. Verify 300-observation native conformance and Docker sandbox via existing check workflow.

Any subgroup failure rejects the corresponding variant. A passing **screen is only preliminary**, not sufficient for production: require independent holdout of ≥64 new paired one-entrant FFA and ≥32 new paired squad seeds per opponent population, endgame review, and all checks.

Do not merge automatically, do not submit to tournament, do not rewrite history. No public competitor research included in repository.

## Final screening audit — 2026-11-22 (216 matches)

**Both candidates REJECTED. Do not promote or spend additional holdout on this exact mechanism.** [Full nine-cell aggregate and 216-match reproducible run](https://github.com/pucaru/curly-succotash/actions/runs/44930651003) succeeded; [300-observation native plus Docker sandbox conformance](https://github.com/pucaru/curly-succotash/actions/runs/44930650908) succeeded at the same evaluated head `8f6eaffc13224461e7cdf206d68546449b5d8f96`. Numeric score parser validated all 216 individual placements.

| Population | Squad control | Squad lane/hold | Squad lane/route | FFA control | FFA lane/hold | FFA lane/route |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.083 | 0.000 | 0.000 | 8.583 | 8.417 | 8.417 |
| v2 | 0.083 | 0.083 | 0.083 | 8.833 | 6.833 | 8.083 |
| mixed | 0.417 | 0.417 | 0.500 | 7.500 | 7.833 | 7.917 |

All values are **independent proxy** mean placement points, 12 fresh matched squad and 12 FFA seeds per population/variant, **not** the official private 48-game score. Key paired deltas with 95% bootstrap intervals: lane/hold v2 FFA **-2.000 [-3.750,-0.583]**, W/L/T 2/7/3, low results ≤2 points 2→3, mean rear damage +109.6; lane/route v2 FFA **-0.750 [-1.833,+0.083]**, W/L/T 2/4/6, rear damage +168.8. Both also regress v1 squad -0.083 [-0.250,0.000], v1 FFA -0.167 [-0.500,0.000] and raise v1 FFA rear damage +89.3. Mixed FFA out-of-zone time increases by 0.017s for both variants. Mixed improvements fail to rescue the negative groups. Max proxy action latency 9.33ms (not an authoritative Docker timing measure).

**Additional squad safety audit from each cell's 12 per-seed `--diag` records** (control → lane/hold → lane/route):

| Population | Death before 60s | Mean rear damage taken | Mean time stuck | Mean out of zone |
| --- | --- | --- | --- | --- |
| v1 | 9→9→10 of 12 | 565.6→482.3→463.6 | 1.74→2.43→1.72s | 0→0→0s |
| v2 | 9→9→8 of 12 | 594.5→548.2→580.8 | 0.36→0.34→0.35s | 0→0→0s |
| mixed | 5→5→5 of 12 | 747.5→725.3→834.3 | 1.31→1.15→1.28s | 0→0→0s |

The regression is most clearly seen in v2 FFA, while squad early survival is not meaningfully improved. This suggests simple visible firing-lane waypoints or routing toward occluded targets are not enough, and sometimes sacrifice the original spatial evasion strategy. No official submission, main change, history rewrite, or public competitor research occurred.
