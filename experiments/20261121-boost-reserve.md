# Boost reserve — controlled experiment (21 November 2026)

**Status: evaluation queued; do not promote any setting without complete scores, a fresh holdout and conformance.** Production main is `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

Hypothesis: an aggressive sprint reserve may improve zone evacuation / escape, but may expose the bot after energy depletion. A conservative reserve preserves energy for late emergencies but can cost movement and early weapon acquisition. The baseline `boost_reserve=30` reproduces the current code's two boost guards (including unstuck movement).

- Isolated parameter values: **18 / 30 (control) / 42**.
- Cooperative house-squad proxy: 24 matched seeds **371121–371144** for each value and v1/v2/mixed opponent profiles.
- One-entry true FFA: 24 matched seeds **471121–471144** per value/profile, with 1 hero and 15 fighting opponents.
- Independent MIT simulator pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`.
- 9 matrix jobs; 432 simulated matches if all pass, with exact same seeds and opponent profiles per setting.
- Workflow: [boost-reserve.yml](../.github/workflows/boost-reserve.yml); [Actions runs](https://github.com/pucaru/curly-succotash/actions/workflows/boost-reserve.yml).
- Branch commits: `1237ca64d35dbb97a3950d30f447f56277d0d1c5` (parameter), `2826e617cfb473b98598b45cbb9e317e1464705f` (one-hero evaluator), `284d5baa038edc5ae4ba4f3c8162d056a4123c74` (A/B matrix).

## Scores

Pending completion of nine workflow jobs. Do not interpret the act of launching a benchmark as a score gain. Read raw seed-level artifact outputs before deciding. Compare `16 - place`, paired deltas, squad performance, v2 and mixed FFA, and catastrophic early-death rates. Reserve a fresh 64-seed holdout for any promising variant.

No main-branch change, no official tournament submission and no history rewrite. The previously removed public-research section is not included.

## Independently verified rejection: early laser release

The separate [laser release holdout](https://github.com/pucaru/curly-succotash/actions/runs/44900935696) completed 6/6 jobs successfully using 32 new squad and 64 new FFA seeds per setting/opponent. Candidate margin 0.2 versus baseline 0.1:

| Opponents | Squad control → candidate | One-hero FFA control → candidate |
| --- | ---: | ---: |
| v1 | 0.375 → 0.563 | 8.484 → 8.594 |
| v2 | 0.250 → 0.188 | 6.844 → 7.234 |
| mixed | 0.406 → 0.344 | 7.688 → 7.500 |

The candidate **fails the strict mixed-FFA and v2/mixed-squad nonregression gate**. Its v2 FFA +0.391 gain does not justify promotion. This is a holdout result from a separate branch, not a change made here.

Official metric is mean `16-place`; the qualifying/final FFA uses unseen seeds and competitors. Local scores are proxy scores only.
