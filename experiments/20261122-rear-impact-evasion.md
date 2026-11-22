# Rear-impact lateral escape — 22 November 2026

**Experimental, screen pending.** Immutable production reference `60b5438af4d45af989f63bffcbe0b03250a23ae4`; official practice score unmeasured.

## Mechanism and counterfactual

Prior lightning spacing and long duel strafing harmed rear-hit safety. Production receives actual `damaged` event fields `rear`, `by`, `bearing`, but discards the rear flag. It continues duelling its frontal selected target even when a *different* shooter just landed a 1.5×-multiplier rear hit. Candidate `MECH_TUNE={"rear_impact_evade":1}` triggers for 1.5 seconds following a distinct rear hit between 75% and 90% HP (without overriding pre-existing critical-health cover/flee logic), selects a reachable zone-safe lateral waypoint taking account of other hunters and available line-of-sight barriers, briefly boosts, and **retains fire on the target**. Flag 0 has unchanged decisions. This is impact-triggered positional intervention, not the previously rejected simple lightning distance-retreat or fixed orbit timing.

## Preregistered tests

Pinned MIT independent match proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Simultaneous paired candidate/control, three v1/v2/mixed adversary populations, two modes (15 coordinated house-like squad; 1-hero real FFA), 12 new seeds per cell = **144 matches**. Squad 2611201–2611212; FFA 2612201–2612212. Audit completeness, mean placement, bootstrap 95% CI, W/L/T, low (≤2) finishes, FFA rear damage and zone exposure, squad early deaths (<60s), damage/stuck/zone metrics and action latency. Native 300-observation and sandbox Docker conformance with candidate flag required.

Reject on any subgroup placement regression, higher low finishes, increased FFA rear damage/zone exposure or more early squad deaths. Passing the screen only licenses **new held-out ≥64 FFA and ≥32 squad per population**, end-circle review and protocol audit, NOT promotion. Independent proxy cannot establish official 48-match practice score ≥6.00. No official submission, production/history changes, or competitor-derived research/code.

CI workflows: [paired screen](https://github.com/pucaru/curly-succotash/actions/workflows/rear-impact-evasion.yml), [candidate conformance](https://github.com/pucaru/curly-succotash/actions/workflows/rear-impact-evasion-check.yml).

## Final independent screen — rejected, 22 November 2026

**All 144 games, 6 paired cells and exact-seed aggregator succeeded** in [Actions 44967898506](https://github.com/pucaru/curly-succotash/actions/runs/44967898506). Candidate code evaluated at `d18015716382a01f3b8b0ec1cc979f0dbe5ca085`. Candidate-flag-enabled [300-observation native and Docker conformance 44967898470](https://github.com/pucaru/curly-succotash/actions/runs/44967898470) succeeded; production-default conformance [44967898484](https://github.com/pucaru/curly-succotash/actions/runs/44967898484) succeeded. Early workflow/test failures occurred before simulations and were repaired by restricting the intervention to HP 75–90%; no already-completed game was rerun.

| Opponents | Squad mean control→candidate | FFA mean control→candidate | Paired FFA Δ [bootstrap 95% CI], W/L/T | FFA rear-damage Δ | FFA zone Δ |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.667→0.667 | 9.167→9.083 | −0.083 [−0.250,0], 0/1/11 | **+72.2** | 0.000 s |
| v2 | 0.333→0.000 | 7.917→8.000 | +0.083 [−2.083,+2.250], 4/5/3 | **+327.4** | 0.000 s |
| mixed | 0.833→0.750 | 7.333→7.500 | +0.167 [−0.333,+0.750], 3/3/6 | **+3.1** | 0.000 s |

Paired squad Δ [95% bootstrap CI], W/L/T: v1 +0.000 [0,0], 0/0/12; v2 **−0.333 [−0.750,0]**, 0/3/9; mixed −0.083 [−0.333,+0.167], 1/2/9. Low finishes ≤2 points: squad v1 12→12, v2 12→12, **mixed 11→12**; FFA v1 1→1, v2 1→0, mixed 1→1. Squad early deaths <60s: v1 6→6, v2 8→8, **mixed 2→3**. Squad v2 mean death time declined 78.41→57.76s, with damage dealt 1394.22→921.17, despite modest v2 FFA placement improvement. FFA proxy peak action latency 12.21ms. All results come from matched independent approximate simulations, not the official 48-match score.

**DECISION: REJECT; do not initiate large holdout or promote.** Prespecified gates fail on v1 FFA mean placement, v2/mixed squad placement, mixed low finishes and early deaths, plus increased FFA rear damage in **all three** populations. The trigger adds tactical lateral escape without suppressing shooting, but its positional exposure offsets benefits. A different attacker having just dealt rear damage does not itself establish that either perpendicular displacement is safe. Production `main` remains at `60b5438`; no tournament submission, public competitor research, or Git history rewriting. Do not repeat this particular causal hypothesis without a new explanatory mechanism.
