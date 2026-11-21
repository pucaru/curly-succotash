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
