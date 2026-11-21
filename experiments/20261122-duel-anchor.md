# Anchored duel steering — isolated causal experiment (22 November 2026)

**Status:** exploratory screen planned, not validated. Original production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Leave production `main` and existing published commits untouched.

## Causal bug hypothesis

`enemy()` chooses a target using recent attacker priority, pursuit stickiness, and low-health finishing preference, but `steer()` originally always strafed around `threats[0]` (the nearest enemy) whenever a duel started. When the target differs from the closest enemy, this can point the mech's distance-control and lateral trajectory around a different threat than its chosen shooting target. It risks positioning poorly for the intended single-hunter duel.

The candidate passes the *selected target* into duel steering; control uses the original closest-threat steering. Everything else (target selection, aim, weapon fire, movement outside duels, zone logic) remains unchanged. `MECH_TUNE={"duel_target_tracking":0}` reconstructs the control exactly. Candidate default is 1 on this isolated branch so conformance evaluates candidate directly.

## Preregistered local screen

Pinned MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New matched seeds 1710211–1710222 for cooperative squad, 1720211–1720222 for one-entrant FFA, against v1/v2/mixed opponents. 2 modes × 2 policies × 3 populations × 12 seeds = 144 independent simulated games. Parse exact coverage; report paired mean placement, bootstrap 95% CI, W/L/T, low placements, rear hits, zone exposure and observed action latency. Run local unit tests and native 300-observation + Docker sandbox conformance. Require no subgroup or safety regression before any fresh ≥64 FFA + ≥32 squad holdout per population and final-circle review. Never confuse proxy scoring with organizer's private 48-match practice result.

No official entry submission, no external competitor code or public-competitor research in this repo. No automatic promotion.
