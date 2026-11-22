# Cube pickup-arrival deadzone — 22 Nov 2026

**Status:** independent paired 144-game screen and candidate-enabled conformance pending. This is a new isolated test of cube autopickup, *not* a rerun of the rejected explicit weapon-take fix. Source control: immutable main `60b5438af4d45af989f63bffcbe0b03250a23ae4` (official score unmeasured).

## Exact protocol inconsistency

Cubes automatically go to the closest mech inside `config.cubes.pickup_radius` (normally **3.5 metres**); unlike weapons, there is no explicit take action. The production `steer` method stops movement once a `cube` goal is less than **6m** away, so a bot can settle 3.5–6m away from a visible cube and never collect it. Weapon and cube acquisition use distinct rules and have distinct impacts on health, damage and upgrades. The 22 Nov weapon-only deadzone fix passed conformance but **failed** opponent-mode safety gates; no production promotion.

This candidate changes only the `cube` goal stopping radius to `max(1.2, cubes.pickup_radius - 1.0)` when `MECH_TUNE={"cube_approach_fix":1}`. Default toggle 0 matches control. Weapon stop, combat, threat, route, zone and all other modes remain unchanged. Deterministic tests cover control stalling at 5.2m, candidate advancing, variable cube radius and unchanged weapon behavior.

## Precommitted tests and gates

Pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, 12 fresh paired seeds per 2 modes × 3 opponent profiles (v1/v2/mixed) = **144 total games**. Native official-kit 300-observation and Docker conformance explicitly enabled. Audit paired placement, CIs, low finishes ≤2, squad early deaths <60s and damage dealt, FFA rear damage and zone exposure. Reject on any regression; positive screen requires new ≥64 FFA + ≥32 squad seeds per population with end-circle and protocol review, never automatic promotion. Proxy is not official 48-match scoring.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/cube-arrival.yml) · [Conformance workflow](https://github.com/pucaru/curly-succotash/actions/workflows/cube-arrival-check.yml).

## Final independent matched-screen audit — rejected, 22 November 2026

**All 144 proxy games, six matrix jobs and aggregate passed** in [GitHub Actions 44972730946](https://github.com/pucaru/curly-succotash/actions/runs/44972730946). The [candidate-enabled official-kit native and Docker 300-observation conformance run 44972730897](https://github.com/pucaru/curly-succotash/actions/runs/44972730897) and [default conformance 44972730877](https://github.com/pucaru/curly-succotash/actions/runs/44972730877) **both passed**. Tested gameplay commit `a6f042856d04a697a547788854b8f7b37c8a8c70`.

| Opponents | Squad mean control→candidate | One-hero FFA mean control→candidate | FFA rear damage Δ | FFA out-of-zone Δ |
| --- | ---: | ---: | ---: | ---: |
| v1 | 0.333→0.333 (0) | 7.917→7.917 (0) | 0.0 | +0.000s |
| v2 | 0.000→0.083 (+0.083) | 7.083→8.167 (**+1.083**) | −42.6 | **+2.892s** |
| mixed | 1.000→1.333 (+0.333) | 7.833→7.833 (0) | **+213.9** | +0.000s |

Paired 95% bootstrap CIs: v1 squad [0,0], FFA [0,0]; v2 squad +0.083 [0,+0.250], FFA +1.083 [+0.417,+2.000]; mixed squad +0.333 [−0.167,+0.917], FFA 0 [−0.500,+0.417]. Low placements ≤2: squad v1 12→12, v2 12→12, mixed 11→10; FFA v1 0→0, v2 1→1, mixed 0→0. Squad early deaths (<60s): v1 5→5, v2 5→5, **mixed 1→3**. Squad mean death time v2 73.79→62.14s despite a small placement gain; mixed 128.96→133.88s. Squad damage dealt v1 unchanged at 1240.33, v2 720.83→848.83, mixed 2103.34→2474.01. Independent proxy peak FFA action latency 5.53ms (not Docker guarantee).

**REJECT.** Although candidate cube arrival increased v2 FFA by +1.083 and mixed squad by +0.333, it **fails the predefined FFA safety gates** (v2 zone +2.892s, mixed rear damage +213.9) **and the mixed early squad death gate** (1→3). The aggregation script flags rear/zone regressions; manual audit additionally flagged the early-death regression, which was printed but not added to the script's invalid gate list. This does not change the decision. The cube collection stop-radius mismatch is genuine, but the unconditional close-in approach is not robustly beneficial. Do not expand to holdout, change production main, or submit any official entry based on this proxy.

