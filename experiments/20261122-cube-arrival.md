# Cube pickup-arrival deadzone — 22 Nov 2026

**Status:** independent paired 144-game screen and candidate-enabled conformance pending. This is a new isolated test of cube autopickup, *not* a rerun of the rejected explicit weapon-take fix. Source control: immutable main `60b5438af4d45af989f63bffcbe0b03250a23ae4` (official score unmeasured).

## Exact protocol inconsistency

Cubes automatically go to the closest mech inside `config.cubes.pickup_radius` (normally **3.5 metres**); unlike weapons, there is no explicit take action. The production `steer` method stops movement once a `cube` goal is less than **6m** away, so a bot can settle 3.5–6m away from a visible cube and never collect it. Weapon and cube acquisition use distinct rules and have distinct impacts on health, damage and upgrades. The 22 Nov weapon-only deadzone fix passed conformance but **failed** opponent-mode safety gates; no production promotion.

This candidate changes only the `cube` goal stopping radius to `max(1.2, cubes.pickup_radius - 1.0)` when `MECH_TUNE={"cube_approach_fix":1}`. Default toggle 0 matches control. Weapon stop, combat, threat, route, zone and all other modes remain unchanged. Deterministic tests cover control stalling at 5.2m, candidate advancing, variable cube radius and unchanged weapon behavior.

## Precommitted tests and gates

Pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, 12 fresh paired seeds per 2 modes × 3 opponent profiles (v1/v2/mixed) = **144 total games**. Native official-kit 300-observation and Docker conformance explicitly enabled. Audit paired placement, CIs, low finishes ≤2, squad early deaths <60s and damage dealt, FFA rear damage and zone exposure. Reject on any regression; positive screen requires new ≥64 FFA + ≥32 squad seeds per population with end-circle and protocol review, never automatic promotion. Proxy is not official 48-match scoring.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/cube-arrival.yml) · [Conformance workflow](https://github.com/pucaru/curly-succotash/actions/workflows/cube-arrival-check.yml).
