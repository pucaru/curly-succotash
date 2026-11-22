# Weapon-pickup arrival deadzone — 22 November 2026

**Status:** initial independent 144-match paired screen and candidate-enabled conformance pending. This branch never changes production `60b5438af4d45af989f63bffcbe0b03250a23ae4`, submits official scores, rewrites history, or imports public-competitor research.

## Verified source-level causal defect

The original bot stops its movement in `steer` when distance to a weapon goal is **under 6.0m** but `act` takes the weapon only when distance is **under pickup_radius - 0.1m** (usually 3.9m). In the interval [3.9m, 6.0m), the bot can repeatedly choose a weapon while stopped just outside the take radius. This is a different, direct structural mechanism from the previously rejected 8-second weapon-stall veto. It plausibly contributes to the 10/18 gun-only deaths and 45.6% weapon-mode share observed in the baseline diagnostic but their link is not yet proved.

Candidate opt-in `MECH_TUNE={"pickup_approach_fix":1}` reduces the weapon stopping radius to `max(1.2, pickup_radius - 1.0)`m. All other goals retain the old 6m stop, and combat, upgrades, threats and zone decisions are unchanged. Toggle 0 reproduces production. Unit tests cover original stuck at 5.2m, candidate approach and take at 3.2m, nonweapon behavior, and pickup radius changes.

## Evaluation gate

Pinned MIT independent simulator: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Six population/mode cells: coordinated squad and one-entrant FFA against v1, v2, mixed; 12 new matched seeds per cell = 144 games; FFA and squad baseline/candidate evaluated simultaneously. Full paired placement and 95% bootstrap CIs, low finishes ≤2, squad early deaths <60s, damage dealt, rear damage, zone exposure, latency. Native official-kit 300 observations and Docker sandbox run with candidate enabled.

Reject for *any* subgroup placement regression, increase in low placements, FFA rear/zone exposure or early squad deaths. Passing this screen requires separate fresh >=64 FFA and >=32 squad matched seeds **per population**, end-circle audit and conformance before promotion. Local simulator is approximate and not official 48-match practice scoring.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/pickup-arrival.yml) · [Candidate conformance](https://github.com/pucaru/curly-succotash/actions/workflows/pickup-arrival-check.yml).

## Completed 144-game paired screen — rejected (22 Nov 2026)

[All six compared populations, matched seeds, complete aggregate (run 44972304182)](https://github.com/pucaru/curly-succotash/actions/runs/44972304182) **SUCCESS**. [Explicit candidate native/Docker 300-observation check (44972304171)](https://github.com/pucaru/curly-succotash/actions/runs/44972304171) **SUCCESS**; [default check (44972304160)](https://github.com/pucaru/curly-succotash/actions/runs/44972304160) **SUCCESS**. Tested gameplay commit: `d230e11780c9e554c65e6c5aa686f883a2c2f780`.

| Opponent | Squad control → candidate (Δ) | One-hero FFA control → candidate (Δ) | FFA rear Δ | FFA zone Δ |
| --- | --- | --- | ---: | ---: |
| v1 | 0.333 → 0.583 (+0.250) | 8.750 → 8.833 (+0.083) | **+22.2** | **+2.658 s** |
| v2 | 0.000 → 0.000 (0) | 8.083 → 7.833 (**−0.250**) | −7.4 | **+0.017 s** |
| mixed | 1.333 → 0.917 (**−0.417**) | 8.833 → 8.167 (**−0.667**) | −125.3 | −0.083 s |

Paired 95% bootstrap CIs: squad v1 +0.250 [+0.000,+0.667], v2 0 [0,0], mixed −0.417 [−1.333,+0.250]. One-hero FFA v1 +0.083 [−0.333,+0.500], v2 −0.250 [−1.667,+1.333], mixed −0.667 [−1.500,0]. Low finishes ≤2: squad v1 12→11, v2 12→12, **mixed 9→11**; FFA v1 0→0, **v2 1→2**, mixed 1→1. Squad early deaths <60s: **v1 4→5**, v2 8→8, mixed 3→3. Mean squad damage dealt increased v1 1045.53→1482.25 and v2 836.52→882.58 but fell mixed 3088.87→2487.77. Proxy maximum observed FFA action latency 7.88ms; this is not a Docker timing guarantee.

**Reject: no holdout or production promotion.** The 6m/3.9m pickup mismatch is real and deterministic, but resolving it does **not** robustly improve placement across the opponent populations. More aggressive weapon acquisition changes exposure/positioning and can shorten survival. The observed outcome cannot establish that weapon acquisition itself caused every regression; it does establish the proposed unconditional fix fails multiple predefined safety and placement gates. Do not rerun this exact unconditional fix without a new causal mechanism. No official practice measurement or entry submission.

