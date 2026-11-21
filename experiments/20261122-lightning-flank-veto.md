# Threat-aware lightning spacing — 22 November 2026, 06:32 SGT

**EXPERIMENT ONLY; not validated; do not promote.** Production immutable baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

## New causal mechanism
Earlier isolated-lightning spacing increased v2 FFA placement on 12 paired seeds by +1.750 but increased v2/mixed FFA rear damage and reduced mixed FFA placement. The likely failure mechanism is retreating away from one selected target while entering a second shooter's firing lane. This isolated experiment preserves the prior useful near-lightning separation **only when no second fresh enemy is within 165m and no damage was recently received from a substantially different direction**. It selects a zone-safe, reachable point with multiple directional fallbacks. Non-lightning combat, targeting, upgrades, farming, loot, and all default behavior are unchanged. `MECH_TUNE={"lightning_flank_veto":0}` exactly restores the immutable production policy.

## Prespecified gates
Pinned independently implemented MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. 144 total games (12 FRESH paired seeds for each of cooperative squad/one-entrant FFA, v1/v2/mixed, candidate/control), squad 2253301–2253312, FFA 2254301–2254312. Require complete paired results, 95% bootstrap intervals, low finishes (≤2), FFA rear damage, zone exposure, squad early deaths <60s, stuck time, damage dealt, action latency and native+Docker 300-observation conformance.

Reject on any subgroup negative mean placement, increased low finishes, FFA rear damage or zone exposure, or early squad deaths. Even if screen passes, do not promote without fresh ≥64 FFA and ≥32 squad seeds per opponent profile and endgame/adversarial review. Official 48-game practice score NOT measured; local proxy score does not establish official ≥6.00. No tournament submission or Git history rewrite. No public-competitor research/code in repo.

## Final independent screening outcome (22 November 2026)

GitHub Actions [paired screening](https://github.com/pucaru/curly-succotash/actions/runs/44957490159) and [native/Docker conformance](https://github.com/pucaru/curly-succotash/actions/runs/44957637204) both completed successfully. 144 simulator games total: 12 paired seeds for each of six opponent/mode cells (control and candidate); this is not an official practice score.

| Opponents | Squad control→candidate (Δ) | One-hero FFA control→candidate (Δ) |
| --- | --- | --- |
| v1 | 0.250→0.333 (+0.083) | 8.250→8.250 (+0.000) |
| v2 | 0.083→0.083 (+0.000) | 4.583→5.833 (+1.250) |
| mixed | 0.917→0.750 (−0.167) | 7.250→6.667 (−0.583) |

Paired 95% bootstrap CIs: v1 squad [+0.000,+0.250], v1 FFA [0,0]; v2 squad [−0.250,+0.250], v2 FFA [−0.083,+2.750]; mixed squad [−0.417,0], mixed FFA [−1.833,+0.500]. FFA low placements ≤2: v1 1→1, v2 4→2, mixed 2→2. FFA rear damage delta: v1 +0.0, v2 **+215.5**, mixed −24.6. FFA zone exposure delta 0.000s throughout. Squad deaths <60s: v1 6→5, v2 9→9, mixed 5→5. Squad rear damage v1 618.10→610.86, v2 564.13→620.96, mixed 381.04→446.97. Squad stuck time v1 0.49→0.53s, v2 0.71→1.88s, mixed 1.52→1.56s. Squad damage dealt v1 1276.90→1464.55, v2 827.77→992.08, mixed 2587.75→2560.30. Peak proxy FFA action latency 15.31ms.

**REJECT.** Predefined placement gates failed for mixed squads and mixed FFA; v2 FFA rear damage worsened by +215.5. The large v2 FFA gain is neither safe across populations nor robustly separated from zero by bootstrap CI. No larger holdout justified. No change to production, no official submission.


