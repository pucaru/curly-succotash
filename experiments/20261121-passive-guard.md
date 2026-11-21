# Passive defensive facing — controlled placement experiment (21 November 2026)

**Status:** Screening launched; no outcome or promotion asserted.
Base production commit: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Isolated experiment: never alter main, prior submitted history or removed public-research section.

## Hypothesis
When declining combat in FFA, the bot resumes scanning while a known enemy remains close. Being hit outside its forward arc incurs 1.5× damage. Keep movement/combat unchanged and face a recent observed threat without firing (preserving regeneration).

Controlled variants: `MECH_TUNE={"passive_guard_range":0}` (production control), 120 m, 205 m.

## Prospective protocol
Use pinned independent MIT-licensed proxy engine `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb` (not the hidden official engine), 24 fresh squad seeds 933211–933234 and 24 one-hero FFA seeds 943211–943234 against v1, v2 and mixed bot populations. Exactly one tested bot in FFA. Paired same seeds per variant, nine jobs, 432 games.

Audit placement, matched-seed wins/losses/ties, early FFA deaths, rear damage, outside-zone seconds, and per-action latency. Reject any candidate with a negative mean placement delta in *any* opponent/mode or greater early deaths or zone exposure. Promising candidates require an independent 64 FFA + 32 squad fresh-seed holdout per opponent profile, final-circle checks and Docker/protocol conformance before any production decision.

No official submission or promotion without user authorization. No competitor-source research is stored here.


## Verified screening result

**[432 simulations verified; all 9 comparison jobs and aggregation succeeded](https://github.com/pucaru/curly-succotash/actions/runs/44911170162).** Matching seed counts and FFA diagnostics were audited. [Unit, native-protocol, and Docker conformance passed](https://github.com/pucaru/curly-succotash/actions/runs/44911170115). Max proxy action time 10.36ms; not an official timing claim.

The CI aggregate produced correct cell values and paired deltas but its first two result *column labels* were misordered (120 was printed before 0 despite values being enumerated as 0,120,205). Corrected table below reflects the verified raw run; the aggregate parser header has been corrected for future runs.

| Opponents | 0 squad | 0 FFA | 120 squad | 120 FFA | 205 squad | 205 FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.375 | 8.542 | 0.375 | 8.667 | 0.333 | 8.292 |
| v2 | 0.250 | 6.958 | 0.250 | 7.042 | 0.208 | 6.667 |
| mixed | 0.958 | 6.542 | 0.750 | 7.042 | 0.958 | 6.708 |

**120m — rejected:** v1/v2/mixed FFA improve +0.125/+0.083/+0.500, but mixed squad worsens -0.208 (wins/losses/ties 2/5/17) and mixed FFA rear damage increases +42.2. This violates the predeclared all-population gate.

**205m — rejected:** v1 and v2 FFA worsen -0.250/-0.292, v1/v2 squad each fall -0.042, mixed early FFA eliminations (≤2 points) increase 3→4, and mean FFA rear damage increases +127.2/+40.9/+139.0 (v1/v2/mixed).

**Decision:** no independent holdout or production merge, and no tournament submission. Current main is still `60b5438af4d45af989f63bffcbe0b03250a23ae4`. The local approximation cannot establish a 6.0 official practice score.
