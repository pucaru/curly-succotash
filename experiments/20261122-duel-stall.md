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
