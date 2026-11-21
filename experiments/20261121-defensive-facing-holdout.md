# Front-armor defensive-facing experiment — 2026-11-21

Base production: `main@60b5438af4d45af989f63bffcbe0b03250a23ae4`.
Behavior: `ae6da524b0e3c4f54f2ff115342a47f7670bf31a`.
Unit tests: `8cb717ae6c5efa246f162fa33c40ea4337f417aa`.
First A/B workflow: `0cc6eb255788f85c698c7afb80cabcb5e606f96d`.
Independent one-hero FFA harness: `2fba813bc551fd35c1414bb482981139b0b9bfdd`.
Independent mixed-opponent holdout: `2b8d08ad840e3ea8c05e8a613b06d9cfef9d9d6f`.

Hypothesis: with no offensive target, face a recently tracked nearby threat to reduce damage against the rear arc. `MECH_TUNE.defensive_facing_range` defaults to zero, preserving the original bot.

## Initial paired A/B, selected on these seeds

Independent MIT-licensed simulator pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`.
16 cooperative-squad seeds beginning 651221; 8 eight-clone FFA lobbies beginning 991221 for each policy and opponent.

| Facing radius | Squad v1 | Eight-clone FFA v1 | Squad v2 | Eight-clone FFA v2 |
| ---: | ---: | ---: | ---: | ---: |
| 0 (original) | 0.56 | 7.17 | 0.12 | 5.92 |
| 85 | 0.56 | 8.05 | 0.31 | 6.17 |
| 155 | 0.56 | 7.59 | 0.25 | 6.20 |

The initial experiment favored 85, but its eight identical hero copies per FFA lobby risked a large opponent-composition bias.

## Independent, single-entry FFA holdout

A new runner simulates **one** candidate bot against **15 opponents all fighting one another**. Every candidate and control shares the same 32 new FFA seeds beginning 941221 (one independent hero per lobby), with a separate 24-squad-seed comparison beginning 731221. Three distinct opponent profiles: v1, v2, and mixed (8 v1 + 7 v2 bots). Score is mean `16-place`, higher better.

| Opponent | Control squad | 85 squad | Control one-hero FFA | 85 one-hero FFA | FFA Δ |
| --- | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.29 | 0.29 | 8.250 | 8.312 | +0.062 |
| v2 | 0.08 | 0.08 | 7.688 | 7.219 | -0.469 |
| mixed | 0.83 | 0.75 | 8.094 | 7.750 | -0.344 |

One-hero paired per-seed FFA improvements/worsenings/ties: v1 = 1/1/30, v2 = 6/11/15, mixed = 5/8/19. Thus v1's small positive average arose from only two of 32 matches changing placement, while two independent opponent profiles clearly regress.

Mean rear damage: v1 327.8 → 309.3; v2 535.9 → 517.9; mixed 330.9 → 384.4. Rear-damage changes do not consistently translate into better placement.

**Decision: reject the facing change. Do not promote to main.** Both the v2 and mixed 32-match real single-entry FFA profiles worsen, and mixed squad performance worsens. The first eight-hero-clone benchmark materially overstated the upside. Local simulator behavior is approximate, not the organizer's official hidden score; no official submission was made.

All six A/B and six independent holdout jobs succeeded. Unit and default-config native/Docker conformance checks succeeded. The 85 setting itself was evaluated under the benchmark environment variable, not promoted into Docker's default runtime.

A/B benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44890730906
Independent holdout: https://github.com/pucaru/curly-succotash/actions/runs/44891292648
Conformance: https://github.com/pucaru/curly-succotash/actions/runs/44891292568
