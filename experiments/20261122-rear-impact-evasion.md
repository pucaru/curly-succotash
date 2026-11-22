# Rear-impact lateral escape — 22 November 2026

**Experimental, screen pending.** Immutable production reference `60b5438af4d45af989f63bffcbe0b03250a23ae4`; official practice score unmeasured.

## Mechanism and counterfactual

Prior lightning spacing and long duel strafing harmed rear-hit safety. Production receives actual `damaged` event fields `rear`, `by`, `bearing`, but discards the rear flag. It continues duelling its frontal selected target even when a *different* shooter just landed a 1.5×-multiplier rear hit. Candidate `MECH_TUNE={"rear_impact_evade":1}` triggers for 1.5 seconds following a distinct rear hit between 75% and 90% HP (without overriding pre-existing critical-health cover/flee logic), selects a reachable zone-safe lateral waypoint taking account of other hunters and available line-of-sight barriers, briefly boosts, and **retains fire on the target**. Flag 0 has unchanged decisions. This is impact-triggered positional intervention, not the previously rejected simple lightning distance-retreat or fixed orbit timing.

## Preregistered tests

Pinned MIT independent match proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Simultaneous paired candidate/control, three v1/v2/mixed adversary populations, two modes (15 coordinated house-like squad; 1-hero real FFA), 12 new seeds per cell = **144 matches**. Squad 2611201–2611212; FFA 2612201–2612212. Audit completeness, mean placement, bootstrap 95% CI, W/L/T, low (≤2) finishes, FFA rear damage and zone exposure, squad early deaths (<60s), damage/stuck/zone metrics and action latency. Native 300-observation and sandbox Docker conformance with candidate flag required.

Reject on any subgroup placement regression, higher low finishes, increased FFA rear damage/zone exposure or more early squad deaths. Passing the screen only licenses **new held-out ≥64 FFA and ≥32 squad per population**, end-circle review and protocol audit, NOT promotion. Independent proxy cannot establish official 48-match practice score ≥6.00. No official submission, production/history changes, or competitor-derived research/code.

CI workflows: [paired screen](https://github.com/pucaru/curly-succotash/actions/workflows/rear-impact-evasion.yml), [candidate conformance](https://github.com/pucaru/curly-succotash/actions/workflows/rear-impact-evasion-check.yml).
