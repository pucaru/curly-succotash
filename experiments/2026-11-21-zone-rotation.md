# Zone rotation buffer, independent A/B (2026-11-21)

Base: main at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
Experiment: `experiment/zone-rotation-20261121-1630`, benchmark commit `3062b8fad15d3b91041c6b889d8f62524d0285b9`.

An opt-in `zone_rotation_buffer` (0, 25, 45 seconds) makes the bot turn toward the next safe circle earlier. Default 0 preserves the previous behavior. No gameplay change was merged into main.

Independent MIT-licensed simulator, same seeds per variant: cooperative 15-opponent squad, 12 games beginning with seed 106731; FFA with eight bot copies per lobby, 6 lobbies beginning with seed 550241. Two different opponent policies `tools.baseline.brain_v1` and `tools.baseline.brain_v2`. The simulator is an approximation, not the official 48-match practice scorer.

| Rotation buffer | Squad v1 | FFA v1 | Squad v2 | FFA v2 |
| ---: | ---: | ---: | ---: | ---: |
| 0 (control) | 0.58 | 8.12 | 0.17 | 6.29 |
| 25 | 0.25 | 8.17 | 0.00 | 6.56 |
| 45 | 0.33 | 8.04 | 0.08 | 6.17 |

All entries are mean `16 - place` points per game. FFA represents 6 correlated lobbies (the individual hero placements are not independent). Scores reflect these particular new seeds, not the organizer's hidden score.

Decision: **reject both buffers**. Improvements in FFA (at most +0.27) are small and inconsistent across opponents, while both buffers substantially reduce cooperative squad placements. No production/main promotion. The 300-observation native and Docker protocol checks both passed with 0 late answers, and unit checks passed.

Action run: https://github.com/pucaru/curly-succotash/actions/runs/44885068648
Conformance run: https://github.com/pucaru/curly-succotash/actions/runs/44885068514
