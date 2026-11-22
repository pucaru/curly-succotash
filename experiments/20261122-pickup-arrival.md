# Weapon-pickup arrival deadzone — 22 November 2026

**Status:** initial independent 144-match paired screen and candidate-enabled conformance pending. This branch never changes production `60b5438af4d45af989f63bffcbe0b03250a23ae4`, submits official scores, rewrites history, or imports public-competitor research.

## Verified source-level causal defect

The original bot stops its movement in `steer` when distance to a weapon goal is **under 6.0m** but `act` takes the weapon only when distance is **under pickup_radius - 0.1m** (usually 3.9m). In the interval [3.9m, 6.0m), the bot can repeatedly choose a weapon while stopped just outside the take radius. This is a different, direct structural mechanism from the previously rejected 8-second weapon-stall veto. It plausibly contributes to the 10/18 gun-only deaths and 45.6% weapon-mode share observed in the baseline diagnostic but their link is not yet proved.

Candidate opt-in `MECH_TUNE={"pickup_approach_fix":1}` reduces the weapon stopping radius to `max(1.2, pickup_radius - 1.0)`m. All other goals retain the old 6m stop, and combat, upgrades, threats and zone decisions are unchanged. Toggle 0 reproduces production. Unit tests cover original stuck at 5.2m, candidate approach and take at 3.2m, nonweapon behavior, and pickup radius changes.

## Evaluation gate

Pinned MIT independent simulator: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Six population/mode cells: coordinated squad and one-entrant FFA against v1, v2, mixed; 12 new matched seeds per cell = 144 games; FFA and squad baseline/candidate evaluated simultaneously. Full paired placement and 95% bootstrap CIs, low finishes ≤2, squad early deaths <60s, damage dealt, rear damage, zone exposure, latency. Native official-kit 300 observations and Docker sandbox run with candidate enabled.

Reject for *any* subgroup placement regression, increase in low placements, FFA rear/zone exposure or early squad deaths. Passing this screen requires separate fresh >=64 FFA and >=32 squad matched seeds **per population**, end-circle audit and conformance before promotion. Local simulator is approximate and not official 48-match practice scoring.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/pickup-arrival.yml) · [Candidate conformance](https://github.com/pucaru/curly-succotash/actions/workflows/pickup-arrival-check.yml).
