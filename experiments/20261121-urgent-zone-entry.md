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


## Verified screening result

**[All 432 placements and safety metrics audited; all 9 matrix cells and aggregate SUCCESS](https://github.com/pucaru/curly-succotash/actions/runs/44911421295).** All syntax/unit/native and [Docker conformance passed](https://github.com/pucaru/curly-succotash/actions/runs/44911421263); worst proxy action latency 10.37 ms.

The CI summary's numeric values were in correct `VALUES=(0,24,64)` order, but its column headings erroneously listed 24 before 0. The correction below reflects the verified run; the aggregator heading has been fixed for future runs.

| Opponents | Control squad | Control FFA | 24m squad | 24m FFA | 64m squad | 64m FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.208 | 8.250 | 0.125 | 8.000 | 0.125 | 8.000 |
| v2 | 0.167 | 5.542 | 0.333 | 6.292 | 0.167 | 5.833 |
| mixed | 0.458 | 7.583 | 0.417 | 7.292 | 0.500 | 7.292 |

**24m rejected:** FFA changes v1 -0.250, v2 +0.750, mixed -0.292. Squad v1 -0.083 and mixed -0.042; v1/v2 outside-zone time increases +0.33s/+0.71s. Paired FFA wins/losses/ties v1 1/4/19, v2 9/4/11, mixed 3/5/16. Not robust across the field.

**64m rejected:** FFA changes v1 -0.250, v2 +0.292, mixed -0.292. Squad v1 -0.083; outside-zone time v1/v2 +1.16s/+0.61s; paired FFA v1 1/3/20, v2 6/3/15, mixed 3/5/16. Slight early-death gains in v2 cannot outweigh mixed/v1 losses.

**Decision:** no holdout, no promotion, no official submission. The shortest geographic route does not necessarily maximize placement; the existing center-seeking route remains production. Scores are simulator proxies, not official practice 48-match scores.
