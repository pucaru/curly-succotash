# Preemptive line-of-sight break against an aimed attacker (21 November 2026)

**Status: independent screening in progress. No verified promotion.** Source production baseline: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. This is a fresh isolated branch; `main` and its prior submitted commits remain unchanged.

## Causal hypothesis
The bot normally seeks cover only after losing substantial HP or sustaining fire. A recently observed enemy within 95–155 metres that is **already aiming at our mech** can fire first, preventing regeneration and creating a losing chase. Try moving behind actual nearby wall geometry *before the first shot*; do not react if the enemy is looking away, the direct firing line is already blocked, or the proposed cover does not break that line. The original combat, loot, navigator, scoring, and emergency zone policy are not changed.

The new `MECH_TUNE.preempt_cover_range` is zero by default, preserving the production behavior. Experimental values: 95 m and 155 m. The bot requires a fresh observation (age ≤1.1s), enemy yaw within 0.65 radians of our direction, HP ≥78%, no recent hit, a safe and reachable cover location >4m away, and verified 2D blocked sight from that enemy to cover. 2D line-of-sight is an approximation (terrain and elevations matter); this is an empirical test, not a guaranteed defensive improvement.

## Controlled experiment
Pinned independent match approximation: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, not the official hidden scorer. Three cover ranges (0, 95, 155) × three fixed opponent profiles (v1, v2, mixed), with twelve new matched cooperative-squad seeds 1510211–1510222 and twelve new single-entrant FFA seeds 1520211–1520222 per cell = **216 games**. These are wholly separate seeds from the other active holdout and other concurrently running branch. The aggregator verifies exact per-seed coverage, paired placement W/L/T, early FFA deaths, rear-damage and out-of-zone exposure; comparison is always with simultaneous baseline control. Native 300-observation + constrained Docker conformance must pass.

Reject on any negative opponent/mode mean, increased early FFA deaths or increased out-of-zone exposure. If screening passes, demand a fully independent ≥64 FFA + ≥32 squad fresh-seed holdout per population, bootstrap confidence intervals and final-circle review before proposing production. A simulator win cannot establish an official 6.00 practice mean. No tournament submission without user authorization; no external competitor research or copied competitor code in this repository.

CI screen: https://github.com/pucaru/curly-succotash/actions/workflows/preempt-cover.yml

## Final 216-match screening outcome (21 November 2026, completed)
**Completed CI:** [run 44914314223](https://github.com/pucaru/curly-succotash/actions/runs/44914314223); all nine simulator jobs and aggregate **success**. [Aggregate artifact](https://github.com/pucaru/curly-succotash/actions/runs/44914314223/artifacts/14711073276). One-hero FFA + cooperative squad, 12 matched seeds per mode and each v1/v2/mixed profile. These are exploratory noisy screens, not an official score and not sufficient for promotion.

| Opponents | 0 squad | 0 FFA | 95 squad | 95 FFA | 155 squad | 155 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.333 | 9.333 | 0.333 | 9.250 | 0.333 | 9.417 |
| v2 | 0.250 | 5.833 | 0.250 | 7.250 | 0.167 | 7.083 |
| mixed | 1.250 | 8.167 | 1.250 | 8.000 | 0.833 | 8.250 |

For **95m**, FFA deltas v1 −0.083 (0/1/11), v2 +1.417 (4/2/6), mixed −0.167 (0/2/10); squad deltas all 0. Mixed FFA rear-damage +122.1 even though zone exposure improves 0.13s. Early low-placement counts v1 1→1, v2 4→2, mixed 1→1. **Reject:** two FFA groups have negative mean placement.

For **155m**, FFA deltas v1 +0.083 (1/2/9), v2 +1.250 (4/3/5), mixed +0.083 (3/4/5); squad deltas v1 0.000, v2 **−0.083**, mixed **−0.417**. V2 FFA rear-damage +14.2. Early low-placement counts v1 1→1, v2 4→2, mixed 1→1. **Reject:** v2 and mixed coordinated-squad groups regress. Outside-zone time changes ~0 in 155m groups. Peak proxy action latency 8.35ms.

**Final decision: reject both preemptive-cover ranges.** The apparent +v2 FFA gains do not justify the v1/mixed regression or loss against the coordinated squad. No large holdout is warranted on unchanged variants. No modification of main, submission, or restoration of removed research material.
