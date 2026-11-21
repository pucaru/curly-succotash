# First-shrink mode inference — isolated causal experiment (21 November 2026)

**Status:** screening proposed. Baseline production commit `60b5438af4d45af989f63bffcbe0b03250a23ae4`; the default candidate branch's `MECH_TUNE.pre_shrink_ffa_only=0` preserves existing FFA classification and all gameplay decisions.

## Structural diagnosis
The current implementation switches permanently to FFA behavior after just two non-self eliminations after t=50s. That evidence is ambiguous: the official coordinated house squad never attacks itself, but can lose mechs to the closing zone. A late environmental casualty can therefore make the bot *incorrectly* switch into a passive FFA policy, losing the opportunity to eliminate remaining squad hunters. Conversely, a real FFA with delayed deaths may require the current later detection. Thus we cannot assume this change improves either population.

Candidate `pre_shrink_ffa_only=1` counts one early non-self death before t=50, or two deaths between t=50 and the **first** shrink start, as FFA evidence. It records the first zone shrink timestamp once so subsequent phase updates cannot silently reopen the detection window. This is a causal distinction, not a pure hyperparameter sweep. Control `0` keeps the original logic.

## Evaluation design
Pinned MIT independent simulator: `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Compare control and strict mode using new matched seeds: 12 cooperative squad 1610211–1610222 and 12 single-hero FFA 1620211–1620222, each for v1/v2/mixed opponents, for 144 total games. Verify exact seed coverage, W/L/T placement, paired bootstrap CI, early low placements, rear damage, out-of-zone exposure, and latency. Unit-test first-shrink initialization and transition; run native 300-observation and sandbox Docker conformance.

These are only exploratory screens with an imperfect external simulator. A candidate must not regress any population or mode or safety metric, and then must be tested with fresh >=64 FFA and >=32 squad seeds *per opponent population*, plus end-circle and runtime review, **before** any production consideration. Do not merge/promote automatically. No official entry submission, no public-competitor research and no copyrighted competitor code in repo. Preserve prior history.
