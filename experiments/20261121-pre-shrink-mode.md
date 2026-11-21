# First-shrink mode inference — isolated causal experiment (21 November 2026)

**Status:** screening proposed. Baseline production commit `60b5438af4d45af989f63bffcbe0b03250a23ae4`; the default candidate branch's `MECH_TUNE.pre_shrink_ffa_only=0` preserves existing FFA classification and all gameplay decisions.

## Structural diagnosis
The current implementation switches permanently to FFA behavior after just two non-self eliminations after t=50s. That evidence is ambiguous: the official coordinated house squad never attacks itself, but can lose mechs to the closing zone. A late environmental casualty can therefore make the bot *incorrectly* switch into a passive FFA policy, losing the opportunity to eliminate remaining squad hunters. Conversely, a real FFA with delayed deaths may require the current later detection. Thus we cannot assume this change improves either population.

Candidate `pre_shrink_ffa_only=1` counts one early non-self death before t=50, or two deaths between t=50 and the **first** shrink start, as FFA evidence. It records the first zone shrink timestamp once so subsequent phase updates cannot silently reopen the detection window. This is a causal distinction, not a pure hyperparameter sweep. Control `0` keeps the original logic.

## Evaluation design
Pinned MIT independent simulator: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Compare control and strict mode using new matched seeds: 12 cooperative squad 1610211–1610222 and 12 single-hero FFA 1620211–1620222, each for v1/v2/mixed opponents, for 144 total games. Verify exact seed coverage, W/L/T placement, paired bootstrap CI, early low placements, rear damage, out-of-zone exposure, and latency. Unit-test first-shrink initialization and transition; run native 300-observation and sandbox Docker conformance.

These are only exploratory screens with an imperfect external simulator. A candidate must not regress any population or mode or safety metric, and then must be tested with fresh >=64 FFA and >=32 squad seeds *per opponent population*, plus end-circle and runtime review, **before** any production consideration. Do not merge/promote automatically. No official entry submission, no public-competitor research and no copyrighted competitor code in repo. Preserve prior history.

## Completed screening and gate decision (22 November 2026 SGT)

**REJECTED — no production promotion.** [All 144 proxy matches and paired aggregate, run 44919676111](https://github.com/pucaru/curly-succotash/actions/runs/44919676111) completed successfully at commit `df9d3ff92aa4aca8f9765f5004227956428ee8d2`. Independent MIT simulator pinned as above. [Native 300-observation and Docker conformance, run 44919676068](https://github.com/pucaru/curly-succotash/actions/runs/44919676068) both passed.

| Opponents | Control squad | Strict squad | Squad Δ | Control FFA | Strict FFA | FFA Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.667 | 0.667 | 0.000 | 7.083 | 7.083 | 0.000 |
| v2 | 0.333 | 0.083 | -0.250 | 5.750 | 5.417 | -0.333 |
| mixed | 0.833 | 0.583 | -0.250 | 8.667 | 8.500 | -0.167 |

Paired 95% bootstrap intervals: v2 squad -0.250 [-0.500, 0.000], v2 FFA -0.333 [-1.000, +0.333], mixed squad -0.250 [-0.750, 0.000], mixed FFA -0.167 [-1.250, +0.833]. The direction of the v2/mixed results violates the predefined no-subgroup-regressions gate. Mixed squad low placements (≤2) rose 11→12; v2 FFA rear damage rose +61.8 average units. The v1 results were identical. These findings do not establish that the hypothesis is categorically wrong in the official game; they *do* reject this implementation under present evidence.

Do not re-run this exact hypothesis without an independently justified causal revision. Official practice score remains unmeasured, and no tournament entry was made. Production `main` remains at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
