# Shorter urgent safe-zone entry — controlled placement experiment (21 November 2026)

**Status:** 432-game screening launched; no results or promotion claimed.
Exact production base: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Isolated branch. No modification of main or any submitted commit.

## Failure mode and hypothesis
The existing emergency code orders movement to the **future zone center** even when the mech is just outside the future ring. In large early circles, this can add hundreds of meters of avoidable exposure. Change *only the emergency waypoint*: on urgent relocation and next radius ≥100 m, point to the nearest entry into the future safe ring with an inward buffer. The small, dangerous final rings retain the original center-seeking behavior.

Tune `MECH_TUNE.urgent_zone_entry_margin`: 0 (control, exact production decisions), 24 m, 64 m.

## Independent paired-seed screening
Use MIT-licensed independent approximation `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, not the official engine. For each margin × v1/v2/mixed opponent population, 24 independent cooperative-squad seeds 953611–953634 plus 24 single-entrant FFA seeds 963611–963634, paired by seed. 432 games over nine CI jobs.

Measure 16-place, early FFA deaths (≤2 points), rear damage, time outside safe zone, action latency and matched seed deltas. Reject if any opponent/mode mean falls, early-death count rises, or mean outside-zone exposure rises. If a candidate passes, use at least 64 fresh FFA and 32 fresh squad holdout seeds per opponent profile; inspect final-circle behavior and rerun Docker and native protocol conformance. These local results cannot establish organizer practice or hidden-final scores.

No official submission without explicit approval; competitor research is not stored in this repo.
