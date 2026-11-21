# Sound-contact steering scale, 21 November 2026

**Decision: reject both non-default variants. Do not promote.** Production `main` remains on `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

Compared sound-based movement repulsion multipliers `0.0` (disabled), `1.0` (production-equivalent control), and `2.0` (doubled). The change adds `TUNE.sound_steer_scale`, default `1.0`, without changing the main branch or default bot behavior.

Independent external match simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; 24 matched cooperative-squad seeds beginning **781121**, and 24 matched **one-entry FFA** seeds beginning **881121**, separately for v1, v2 and mixed v1/v2 opponents. In each FFA lobby, exactly one of 16 bots is the tested hero; the other 15 fight independently. Scoring below is local `16 - placement`, **not** an organizer's official 48-match practice score nor a prediction of the hidden final.

| Opponents | Scale 0 squad | Scale 0 FFA | Scale 1 squad | Scale 1 FFA | Scale 2 squad | Scale 2 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.62 | 7.750 | 0.38 | 7.667 | 0.38 | 8.208 |
| v2 | 0.29 | 5.500 | 0.21 | 5.875 | 0.25 | 5.542 |
| mixed | 0.96 | 6.750 | 1.08 | 7.500 | 0.88 | 7.833 |

On paired FFA placements, scale 0 versus scale 1 changed v1 by +0.083 (12 better, 8 worse, 4 tied), v2 by -0.375 (6/10/8), and mixed by -0.750 (8/12/4). Scale 2 changed v1 by +0.542 (12/6/6), v2 by -0.333 (10/10/4), and mixed by +0.333 (11/11/2). Variant 2 also reduced the mixed squad score 1.08 → 0.88. The 24-seed estimates have substantial placement variance; modest wins in individual profiles are not credible evidence of a reliable overall gain.

All **nine** matrix jobs succeeded, each running Python/unit tests and both simulation modes. Default-configuration native and Docker conformance at the evaluation branch head passed independently; that check verifies the 300 official protocol observations and runtime sandbox, not placement.

- Sweep results and raw logs: https://github.com/pucaru/curly-succotash/actions/runs/44894652045
- Branch-head conformance: https://github.com/pucaru/curly-succotash/actions/runs/44894652028
- Parameterizing commit: `fd6905838d890766f452f79f7938a767342da3fd`
- One-entry FFA harness: `4c384fc30f456a936884da8a1a11a8a1a76edd06`
- Controlled experiment workflow: `0a0425e08ce27d53f166373e5b50b47291ceca88`

No tournament submission performed. No main-branch or submitted-history rewrite. The independent simulator only approximates the organizer's house-bot squad, and final FFA opponents will differ.
