# Selective squad engagement — independent screen (21 November 2026)

**Status:** 216-game screening launched; no improvement claimed.

The official 48-match practice adversaries are a 15-mech coordinated squad. They share vision and never kill each other. To achieve a mean 6-point practice score our mech must, on average, survive six opponent eliminations (whether from our kills or environmental attrition). Current local squad means (0–1) are well below target, even when local FFA is high. Prior experiments adjusted duel movement radius, but not the range at which this bot voluntarily acquires and shoots healthy, unprovoked squad targets.

## Controlled change
Target selection previously treated any enemy in range <190m as shootable, even if it has not attacked, is fully healthy, and is far outside reliable gun impact range. Newly added `TUNE.squad_unprovoked_range` only gates *unprovoked, relatively healthy* squad enemies. It never prevents returning fire at a recent attacker or finishing a target ≤45% HP. FFA targeting remains byte-for-byte equivalent once FFA mode is recognized.

Variants: 190m (original production control), 85m, 125m. Existing movement, upgrades, regen, aim, cover, and weapons unchanged; all defaults preserve baseline behavior.

## Reproducible screening protocol
Pinned, independent MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; NOT the organizer's real official simulator (squad hunting/visibility approximated). Twelve fresh paired seeds for squad (1410211–1410222) and twelve fresh one-hero FFA (1420211–1420222) per control/variant × v1/v2/mixed opponents = 216 matches. Paired score deltas and wins/losses/ties; early deaths, rear damage, zone time and latency monitored.

This is a small screening sample only. A candidate must avoid *any* opponent/mode regression and secondary safety regressions, then pass a separate fresh-seed ≥64 FFA +32 squad holdout per population, endgame inspection, and native+Docker conformance before consideration. No official submission, no main modification, no competitor-code copying, no removal-history reversal and no external competitive research written into repo.
