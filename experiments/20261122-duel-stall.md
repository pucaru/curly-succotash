# A true zero-progress duel — bounded diagnostic experiment (2026-11-22)

**Status: screen pending; main unchanged.** Immutable baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`; official practice score unmeasured.

## New causal mechanism (different from prior guided-unstuck tuning)

Squad failures show near-zero placement even when damage is dealt. On 12 previously held v1 squad seeds (prior selected-target screen baseline), average rear damage was 730 units, average time stuck was 11.9 seconds, 6/12 died before 60 seconds, and 1 died to zone after 125 seconds stuck. Some v2 squad games died while stuck nearly throughout a 41-second life. Simulator is approximate; this is diagnostic, not official evidence.

Code inspection found a structural guard: `moving = mode != "duel" and distance(p,goal)>13`. A `duel` requests continuous lateral movement, but by construction its goal is the mech's current position. This means even **zero displacement with nonzero attempted strafe** never increments the recovery counter. The earlier rejected `guided-unstuck` experiment changed **escape direction after recovery already triggered**, not whether a stuck duel can trigger it. This isolates the missing trigger.

- Toggle `MECH_TUNE={"duel_stall_recovery":0}` is exact production control.
- Toggle `1` counts sustained <0.35m displacement when in duel with nonzero strafe and invokes existing random heading + jump recovery after 17 such decisions, without changing ordinary movement, aim, combat or pathfinder.

## Protocol and screening gates

Independent MIT proxy pinned to `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Twelve fresh paired seeds for each squad/one-entrant-FFA and v1/v2/mixed opponent population, × 2 policies = 144 games. Squad seeds 1830211–1830222 and FFA seeds 1840211–1840222.

No subgroup decrease in mean placement, no increase in low placements (≤2 points), FFA rear damage or time out of zone. Report 95% paired bootstrap CIs, W/L/T, latency. Native and Docker 300-observation protocol check must pass. Even a positive screen requires an independent holdout ≥64 paired FFA and ≥32 paired squad seeds per opponent, plus endgame review, before considering any main change.

No official tournament entry; no public competitor research in repository and no rewrite of existing commits.

## Completed screen audit — 2026-11-22

**REJECT for production, no holdout and no merge.** All 144 matched proxy games and aggregate completed [successfully, run 44930965084](https://github.com/pucaru/curly-succotash/actions/runs/44930965084), and [300-observation native plus Docker sandbox conformance, run 44930964995](https://github.com/pucaru/curly-succotash/actions/runs/44930964995), completed successfully at evaluation SHA `4c04f59e36e3317c9572dcc1403a0cbc776a029a`.

| Opponent | Squad control→candidate | One-hero FFA control→candidate | Paired FFA delta [95% bootstrap CI], W/L/T | FFA rear damage delta | FFA zone delta |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.500→0.500 | 9.083→9.083 | +0.000 [0,0], 0/0/12 | +0.0 | +0.000s |
| v2 | 0.000→0.000 | 6.083→5.417 | **-0.667 [-2.583,+0.833]**, 4/3/5 | -255.4 | +0.000s |
| mixed | 0.583→0.583 | 6.667→7.333 | +0.667 [+0.250,+1.167], 6/0/6 | **+111.7** | +0.000s |

All squad paired deltas were 0.000 (v1 0/0/12, v2 0/0/12, mixed 1/1/10); mixed squad 95% CI [-0.250,+0.250]. Counts of placements ≤2 are squad v1 12→12, v2 12→12, mixed 11→11; FFA v1 0→0, v2 3→3, mixed 0→0. Peak independent proxy FFA action latency 9.63ms, not an authoritative sandbox timing measure.

The hard gates reject both the negative v2 FFA placement direction and mixed FFA increased rear damage despite mixed FFA improvement. No evidence of robust squad placement advantage.

**Extra 12-seed squad diagnostics** (control→candidate):

| Opponent | Death before 60s | Mean death time | Mean rear damage | Mean stuck seconds | Zone time |
| --- | --- | --- | --- | --- | --- |
| v1 | 5→5 | 80.18→80.18s | 359.1→359.1 | 0.64→0.64s | 0→0s |
| v2 | 6→8 | 66.63→61.24s | 371.9→368.5 | 2.33→0.81s | 0→0s |
| mixed | 4→4 | 93.90→93.16s | 499.9→366.5 | 0.77→0.80s | 0→0s |

The v2 candidate indeed reduced no-progress time (2.33→0.81s), but deaths before 60s worsened (6→8) while squad score remained at zero, so fixing the stall trigger alone is insufficient. It can change FFA risk exposure adversely; do not rerun this exact minimal tweak absent a new causal mechanism. The local simulator cannot verify any official practice score. Production and submitted history untouched.
