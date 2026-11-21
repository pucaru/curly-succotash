# Laser release window — 21 November 2026

**Status: provisional; do not promote before independent holdout.**
Production main remains at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

The [official rulebook](https://www.joinbuilders.org/buildathon/tracks/builders/files/protocol.md?inline=1) confirms that charging the laser limits movement to half speed. Hypothesis: releasing the beam earlier than the existing `charge_s - 0.10` threshold may reduce exposure, particularly against stronger free-for-all opponents. This sweep parameterized the laser release margin as `TUNE.laser_release_margin`, default **0.10**; the default bot behavior remains unchanged.

Source commits: bot parameter `cbe90a2a6578ac1a6998919dca0af0616fd1100f`, one-hero FFA runner `6420aee431c4a944c0aff466d5ceaeb79db7d35b`, regression test `8695c1cea3a7a7d572affc46087a71190febda70`, sweep workflow `4112d67b8f124cca656a195a0a6f883b0cc87090`.

Independent MIT-licensed simulator pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; 24 matched cooperative-squad seeds starting **991121** and 24 matched **one-hero FFA** seeds starting **1091121**, independently for v1, v2 and mixed opponent populations. FFA pits one candidate against 15 opponents that fight each other. Scores are local mean `16 - place` points per match, **not the organizer's practice or final score**.

| Opponent profile | 0.0 squad | 0.0 FFA | 0.1 control squad | 0.1 control FFA | 0.2 squad | 0.2 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.29 | 7.958 | 0.29 | 8.167 | 0.25 | 8.125 |
| v2 | 0.08 | 6.292 | 0.08 | 5.875 | 0.12 | 6.667 |
| mixed v1/v2 | 0.62 | 7.625 | 0.62 | 7.417 | 0.58 | 7.958 |

One-hero FFA placement deltas versus the matched 0.1 control:
- 0.0: v1 **−0.209** (2 better, 3 worse, 19 tied); v2 **+0.417** (4/4/16); mixed **+0.208** (5/6/13).
- 0.2: v1 **−0.042** (2/2/20); v2 **+0.792** (12/7/5); mixed **+0.541** (5/4/15).

**Interpretation:** margin 0.0 is inconsistent; do not promote. Margin 0.2 is a holdout candidate: gains are positive versus v2 and mixed opponents, but its v1 FFA score is slightly lower, as are v1/mixed squad scores. There are only 24 FFA observations per profile and plenty of placement variance. No production promotion based on the first sweep.

First sweep: https://github.com/pucaru/curly-succotash/actions/runs/44899934015 (all nine matrix jobs succeeded).
Default-configuration Docker/native protocol, unit tests: https://github.com/pucaru/curly-succotash/actions/runs/44899933824 (passed).

A separate, precommitted **64-new-seed FFA + 32-new-seed squad** holdout uses seeds **1291121** / **1191121**, comparing only the original margin 0.1 against 0.2 for all three opponent profiles. Holdout workflow commit `5fc00bd62b252fd6a9a8586e2b66c5ec8519992a`; results: https://github.com/pucaru/curly-succotash/actions/runs/44900935696 (pending at report creation).

No official submission, rewrite, or change to main. Do not restore the removed public research section. Final-round FFA has unknown human opponents and seeds, so the independent local simulator is a proxy rather than proof of hidden-score improvement.
