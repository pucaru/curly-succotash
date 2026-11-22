# Empty-magazine-only idle reload: independent matched-seed screen (22 November 2026)

**Status: COMPLETED — REJECTED; not promoted.** Immutable control `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
Causal separation from rejected combined partial+empty idle reload: the previous
candidate reloaded magazines below 65% in quiet moments, and regressed all squad
populations. This candidate **only** reloads when gun ammo is zero and no target
is selected, irrespective of nearby sounds. Existing active-target reload behavior
and all combat, movement, zone, loot, upgrades remain identical.

Production-default `TUNE.empty_idle_reload=0` is baseline-identical.
Candidate `MECH_TUNE={"empty_idle_reload":1}` is isolated on this branch.
Control and candidate: 12 new paired squad seeds 3182101–3182112 and 12
new one-entrant FFA seeds 3183101–3183112, v1/v2/mixed opponents = 144 games.
Third-party pinned MIT proxy engine `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`.
Comparisons require paired 95% bootstrap CIs, low-finishes, deaths <60 sec,
FFA rear damage, outside-zone exposure, squad damage dealt and action latency.
Gate: reject any opponent/mode mean placement decline, increased low finishes,
early deaths, rear damage or zone exposure; no cherry-picking. Only if passes
all subgroup and safety gates run new independent holdout with >=64 FFA
and >=32 squad per group, inspect end-circle and repeat native+Docker
candidate-enabled 300-observation conformance. Local results DO NOT measure
official 48-match practice score. No official submission, no main change,
no history rewrite, no competitor research in repo.

[Screening workflow](https://github.com/pucaru/curly-succotash/actions/workflows/empty-idle-only.yml)

## Completed benchmark and conformance (22 November 2026, 12:40 SGT)

- Candidate gameplay commit: `da21a5cba22a85422a9b903e8b71b564d3fb8f16`, exactly seven inserted lines in `bot.py`, with `empty_idle_reload=0` preserving production.
- [144-match independent benchmark run 44985578001](https://github.com/pucaru/curly-succotash/actions/runs/44985578001): all six compare cells and aggregate completed successfully; [audited aggregate artifact 14740051243](https://github.com/pucaru/curly-succotash/actions/runs/44985578001/artifacts/14740051243). Benchmark ran at workflow-only commit `7d98302bd826afe43204eee7975e9c4b33f594d4`, with identical gameplay.
- [Explicitly candidate-enabled 300-observation native+Docker conformance run 44985586363](https://github.com/pucaru/curly-succotash/actions/runs/44985586363): **success**. Baseline-default conformance run 44985586349 also succeeded.

| Opponents | Squad baseline→candidate (Δ; 95% paired bootstrap CI) | One-hero FFA baseline→candidate (Δ; 95% CI) | FFA low finishes ≤2 baseline→candidate | FFA rear damage Δ | FFA zone exposure Δ |
| --- | --- | --- | ---: | ---: | ---: |
| v1 | 0.417→0.417 (+0.000; [0,0]) | 10.333→10.333 (+0.000; [0,0]) | 0→0 | +0.0 | +0.000s |
| v2 | 0.167→0.250 (+0.083; [+0.000,+0.250]) | 8.000→7.583 (**−0.417**; [−2.083,+0.833]) | **2→3** | −35.1 | +0.000s |
| mixed | 0.167→0.167 (+0.000; [0,0]) | 7.583→7.917 (+0.333; [+0.000,+1.000]) | 1→1 | **+6.3** | +0.000s |

Matched score W/L/T for squad/FFA: v1 0/0/12 and 0/0/12; v2 1/0/11 and 4/4/4; mixed 0/0/12 and 1/0/11. Squad early deaths <60s: v1 6→6, v2 10→8, mixed 5→5. Squad mean damage dealt: v1 1484→1484, v2 787→1017, mixed 1382→1125. Squad mean survival seconds: v1 91.55→91.55, v2 46.42→54.98, mixed 96.36→90.11. Peak proxy action latency 11.73ms; native and sandbox conformance passed separately.

**Final decision: REJECT.** v2 FFA mean placement declined by 0.417 points and low finishes increased 2→3; mixed FFA rear damage rose +6.3. These violate the preregistered cross-population gates even though v2 squad (+0.083) and mixed FFA (+0.333) improved in the small screen. Results are noisy; v2 FFA paired 95% CI crosses zero. Recovery of a truly empty magazine has no evidenced robust placement benefit. Combined partial+empty reload had already been rejected; no holdout on this failed candidate and no repetition without a new causal mechanism.

This run is **not** the official 48-match practice scorer; no official practice score is known. Production `main` remains `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official submission, production merge, history rewrite or competitor-research material was added.
