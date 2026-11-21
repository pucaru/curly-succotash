# Selective squad engagement — independent screen (21 November 2026)

**Status:** 216-game screening launched; no improvement claimed.

The official 48-match practice adversaries are a 15-mech coordinated squad. They share vision and never kill each other. To achieve a mean 6-point practice score our mech must, on average, survive six opponent eliminations (whether from our kills or environmental attrition). Current local squad means (0–1) are well below target, even when local FFA is high. Prior experiments adjusted duel movement radius, but not the range at which this bot voluntarily acquires and shoots healthy, unprovoked squad targets.

## Controlled change
Target selection previously treated any enemy in range <190m as shootable, even if it has not attacked, is fully healthy, and is far outside reliable gun impact range. Newly added `TUNE.squad_unprovoked_range` only gates *unprovoked, relatively healthy* squad enemies. It never prevents returning fire at a recent attacker or finishing a target ≤45% HP. FFA targeting remains byte-for-byte equivalent once FFA mode is recognized.

Variants: 190m (original production control), 85m, 125m. Existing movement, upgrades, regen, aim, cover, and weapons unchanged; all defaults preserve baseline behavior.

## Reproducible screening protocol
Pinned, independent MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; NOT the organizer's real official simulator (squad hunting/visibility approximated). Twelve fresh paired seeds for squad (1410211–1410222) and twelve fresh one-hero FFA (1420211–1420222) per control/variant × v1/v2/mixed opponents = 216 matches. Paired score deltas and wins/losses/ties; early deaths, rear damage, zone time and latency monitored.

This is a small screening sample only. A candidate must avoid *any* opponent/mode regression and secondary safety regressions, then pass a separate fresh-seed ≥64 FFA +32 squad holdout per population, endgame inspection, and native+Docker conformance before consideration. No official submission, no main modification, no competitor-code copying, no removal-history reversal and no external competitive research written into repo.

## Completed screening and gate decision (22 November 2026 SGT)

[All 216 proxy matches and aggregate, run 44913988617](https://github.com/pucaru/curly-succotash/actions/runs/44913988617) completed successfully at commit `f1eabd28950911e414b2e0799f8a9e3308d3932c`. [300-observation native and Docker conformance, run 44913988553](https://github.com/pucaru/curly-succotash/actions/runs/44913988553) passed.

| Opponents | Control squad/FFA | 85m squad/FFA | 125m squad/FFA |
| --- | --- | --- | --- |
| v1 | 0.250 / 8.167 | 0.167 / 8.250 | 0.250 / 8.417 |
| v2 | 0.167 / 6.000 | 0.000 / 5.500 | 0.250 / 7.167 |
| mixed | 0.500 / 7.917 | 0.917 / 7.667 | 1.083 / 8.583 |

**85m REJECTED**: squad v1 -0.083, squad v2 -0.167, FFA v2 -0.500, FFA mixed -0.250, plus v2 FFA low placements 3→4 and zone exposure +1.06 s.

**125m has positive small-sample placement directions but FAILS the predefined safety gate**, so is **not promotion-ready and is rejected under the current strict criteria**: v1/v2/mixed FFA rear-damage increases of +58.2/+23.6/+99.9 mean units. Its FFA paired wins/losses/ties (v1 3/3/6; v2 3/4/5; mixed 4/3/5) are not persuasive despite positive mean deltas (+0.250/+1.167/+0.667), suggesting high variance/individual extreme outcomes. Squad deltas (+0.000/+0.083/+0.583) are promising only as an exploratory observation. The previously published aggregator's phrase "125 holdout candidate only" did not account for the explicit no-safety-regressions promotion criterion; neither variant meets all gates. A redesigned, independently motivated protective mechanism would require new screening and fresh holdouts, not promotion of this variant.

No production change, official practice measurement, or official entry submission.
