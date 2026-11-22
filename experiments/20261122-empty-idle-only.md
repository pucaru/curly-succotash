# Empty-magazine-only idle reload: independent matched-seed screen (22 November 2026)

**Status:** experiment launched, not promoted. Immutable control `60b5438af4d45af989f63bffcbe0b03250a23ae4`.
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
