# Laser loot value — controlled paired placement experiment (21 November 2026)

**Status: initial 432-match benchmark started; not for submission or promotion.**

Production main is still `60b5438af4d45af989f63bffcbe0b03250a23ae4`. This new branch is based exactly on that production commit and does not touch submitted history.

## Hypothesis and controls

The current `laser_value=300` competes with power cubes, supply drops, and scouting inside the existing 270-unit laser radius. Over-prioritizing a distant laser may expose the bot to a squad or an opportunistic FFA attack. Under-prioritizing it could sacrifice strong late-game shots. Test **180, 300 (production control), 420** with `MECH_TUNE`; leave all other game parameters and bot code unchanged.

Use the same existing original one-hero FFA harness, with exactly one tested bot and 15 independent fighting opponents, and a separate coordinated-squad proxy. Simulator source pinned to the independently implemented MIT-licensed `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. This simulator is not the organizer's exact hidden engine.

Nine jobs test three opponent populations (v1, v2, mixed) × three values. Every job runs 24 new squad seeds **581121–581144** plus 24 new single-entrant FFA seeds **681121–681144**. Total **432 simulated matches**. Baseline and candidate share the same seed and opponent population. The comparison includes per-opponent means, matched-seed wins/losses/ties, and early-death counts (0–2 points).

**Strict promotion gate:** zero negative opponent/mode mean deltas and no increase in early FFA deaths, then independently repeat on fresh 32-seed squad and 64-seed FFA holdouts, with special attention to v2, mixed lobbies and final-circle survival. Conformance and runtime margins must still pass. Never automatically merge or make an official submission.

Workflow: [laser-loot-value.yml](../.github/workflows/laser-loot-value.yml). Machine-readable aggregator: [aggregate_laser_value.py](../bench/aggregate_laser_value.py). [Actions runs](https://github.com/pucaru/curly-succotash/actions/workflows/laser-loot-value.yml).

## Results — completed and rejected (21 November 2026)

[Final 9-job benchmark plus strict aggregate: SUCCESS](https://github.com/pucaru/curly-succotash/actions/runs/44904028607). All **432** trial placements were parsed and checked against exact seed sets. The [branch-head conformance run](https://github.com/pucaru/curly-succotash/actions/runs/44904053581) also passed.

| Opponents | 180 squad | 180 FFA | 300 squad | 300 FFA | 420 squad | 420 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.417 | 7.708 | 0.542 | 7.542 | 0.542 | 7.542 |
| v2 | 0.125 | 6.375 | 0.083 | 6.458 | 0.083 | 6.750 |
| mixed | 0.708 | 7.167 | 0.708 | 7.833 | 0.708 | 7.583 |

Paired FFA deltas versus 300: value 180 changes **v1 +0.167, v2 -0.083, mixed -0.667**, increases mixed FFA early deaths from **5 to 6 of 24**, and reduces v1 squad by **0.125**. Value 420 changes **v1 +0.000, v2 +0.292, mixed -0.250**; its squad means are unchanged. Both candidates **REJECTED** under the predeclared gate. The v2 benefit of 420 is too small and not consistent across opponents, and the mixed loss demonstrates possible final-round damage. No subsequent holdout required for rejected variants.

Full paired wins/losses/ties, early-death counts and per-seed logs are in the [aggregate job summary and its downloadable artifacts](https://github.com/pucaru/curly-succotash/actions/runs/44904028607).

Commit record: `4947243d65d9` (single-hero evaluator), `b287b9b32e5a` (auditor), `ddce616833dd` (benchmark workflow), `515b558fb65c` (pre-registered experiment record).

## Recent completed independent rejections

- **Energy boost reserve** (18, 30 control, 42): 9/9 paired jobs and aggregate passed. Reserve 18 FFA v2 +1.000 but mixed -0.250 and v1 -0.083. Reserve 42 FFA v1 +0.500 but mixed -0.917; mixed squad -0.042. Both rejected. [Paired benchmark](https://github.com/pucaru/curly-succotash/actions/runs/44903097762).
- **Laser scout radius** (200, 270 control, 340): all 9 comparison jobs passed. FFA v1 8.917 / 9.375 / 9.375; v2 5.917 / 6.167 / 6.000; mixed 8.208 / 7.625 / 8.083. Both alternatives decrease at least one FFA profile and cooperative-squad mean. Rejected. [Paired benchmark](https://github.com/pucaru/curly-succotash/actions/runs/44902043800).

Prior independent sound-repulsion and laser-release experiments were also rejected due to stronger-opponent or mixed-FFA regression.

No production change, history rewrite, removed-public-research restoration, or official scoring submission occurred.
