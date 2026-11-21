# Preemptive line-of-sight break against an aimed attacker (21 November 2026)

**Status: independent screening in progress. No verified promotion.** Source production baseline: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. This is a fresh isolated branch; `main` and its prior submitted commits remain unchanged.

## Causal hypothesis
The bot normally seeks cover only after losing substantial HP or sustaining fire. A recently observed enemy within 95–155 metres that is **already aiming at our mech** can fire first, preventing regeneration and creating a losing chase. Try moving behind actual nearby wall geometry *before the first shot*; do not react if the enemy is looking away, the direct firing line is already blocked, or the proposed cover does not break that line. The original combat, loot, navigator, scoring, and emergency zone policy are not changed.

The new `MECH_TUNE.preempt_cover_range` is zero by default, preserving the production behavior. Experimental values: 95 m and 155 m. The bot requires a fresh observation (age ≤1.1s), enemy yaw within 0.65 radians of our direction, HP ≥78%, no recent hit, a safe and reachable cover location >4m away, and verified 2D blocked sight from that enemy to cover. 2D line-of-sight is an approximation (terrain and elevations matter); this is an empirical test, not a guaranteed defensive improvement.

## Controlled experiment
Pinned independent match approximation: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, not the official hidden scorer. Three cover ranges (0, 95, 155) × three fixed opponent profiles (v1, v2, mixed), with twelve new matched cooperative-squad seeds 1510211–1510222 and twelve new single-entrant FFA seeds 1520211–1520222 per cell = **216 games**. These are wholly separate seeds from the other active holdout and other concurrently running branch. The aggregator verifies exact per-seed coverage, paired placement W/L/T, early FFA deaths, rear-damage and out-of-zone exposure; comparison is always with simultaneous baseline control. Native 300-observation + constrained Docker conformance must pass.

Reject on any negative opponent/mode mean, increased early FFA deaths or increased out-of-zone exposure. If screening passes, demand a fully independent ≥64 FFA + ≥32 squad fresh-seed holdout per population, bootstrap confidence intervals and final-circle review before proposing production. A simulator win cannot establish an official 6.00 practice mean. No tournament submission without user authorization; no external competitor research or copied competitor code in this repository.

CI screen: https://github.com/pucaru/curly-succotash/actions/workflows/preempt-cover.yml
