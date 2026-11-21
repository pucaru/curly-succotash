# Anchored duel steering — isolated causal experiment (22 November 2026)

**Status:** exploratory screen planned, not validated. Original production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Leave production `main` and existing published commits untouched.

## Causal bug hypothesis

`enemy()` chooses a target using recent attacker priority, pursuit stickiness, and low-health finishing preference, but `steer()` originally always strafed around `threats[0]` (the nearest enemy) whenever a duel started. When the target differs from the closest enemy, this can point the mech's distance-control and lateral trajectory around a different threat than its chosen shooting target. It risks positioning poorly for the intended single-hunter duel.

The candidate passes the *selected target* into duel steering; control uses the original closest-threat steering. Everything else (target selection, aim, weapon fire, movement outside duels, zone logic) remains unchanged. `MECH_TUNE={"duel_target_tracking":0}` reconstructs the control exactly. Candidate default is 1 on this isolated branch so conformance evaluates candidate directly.

## Preregistered local screen

Pinned MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New matched seeds 1710211–1710222 for cooperative squad, 1720211–1720222 for one-entrant FFA, against v1/v2/mixed opponents. 2 modes × 2 policies × 3 populations × 12 seeds = 144 independent simulated games. Parse exact coverage; report paired mean placement, bootstrap 95% CI, W/L/T, low placements, rear hits, zone exposure and observed action latency. Run local unit tests and native 300-observation + Docker sandbox conformance. Require no subgroup or safety regression before any fresh ≥64 FFA + ≥32 squad holdout per population and final-circle review. Never confuse proxy scoring with organizer's private 48-match practice result.

No official entry submission, no external competitor code or public-competitor research in this repo. No automatic promotion.

## Completed 144-match screening audit (22 November 2026 SGT)

**REJECTED under no-subgroup-regression gate; no holdout or production merge.** The independent simulator [screen run 44925511193](https://github.com/pucaru/curly-succotash/actions/runs/44925511193) completed all six opponent/variant jobs plus aggregate successfully at commit `f440a63a0a9043250d9bea9d5facdeb756a3f65c`; [300-observation native and Docker conformance run 44925511097](https://github.com/pucaru/curly-succotash/actions/runs/44925511097) passed. The first workflow attempt had two incorrect deterministic test assertions for the sign of an existing strafe vector, which were corrected (without altering strategy) and all tests passed before the successful independent screen. This was a test-specification issue, not a bot crash.

| Opponents | Control squad | Anchor squad | Squad Δ | Control FFA | Anchor FFA | FFA Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.500 | 0.583 | +0.083 | 6.250 | 6.250 | 0.000 |
| v2 | 0.333 | 0.417 | +0.083 | 5.417 | 5.250 | **-0.167** |
| mixed | 0.750 | 1.083 | +0.333 | 6.167 | 6.333 | +0.167 |

12 fresh paired seeds per mode, variant and opponent population. Paired v2 FFA delta -0.167, 95% bootstrap CI [-1.000,+0.500], W/L/T 1/1/10; v1 FFA all 12 scores identical. Mixed squad improvement +0.333 [0.000,+0.750], W/L/T 3/0/9, but no evidence it is robust outside this small proxy. FFA rear-damage changes: v1 +0.0, v2 -46.3, mixed -43.1 mean units; zone exposure unchanged; low FFA placements unchanged. Max observed proxy FFA latency 4.46ms (not authoritative sandbox timing). The v2 FFA mean regression breaches the pre-registered hard gate, despite directional squad gains.

**Key conclusion:** A real mismatch exists between selected target and steering reference and the regression test demonstrates it, but merely aligning them is insufficient to justify replacement of production behavior; the population tradeoff persists. No further re-run of this exact change without a new causal explanation. Official practice score remains unmeasured and local squad scores are not official.
