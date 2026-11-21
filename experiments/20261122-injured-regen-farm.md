# Injured noncombat farming versus healing-window discipline — 22 November 2026

**FINAL: REJECTED after complete 144-game independent screen and conformance.** Immutable production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official practice run or tournament submission; local scores are approximate.

## Causal hypothesis
Official `mechfight/1` §7 says health regeneration starts after **5 s without dealing or receiving damage**, at **45 HP/s**, and does not occur while outside the safe zone. The original bot opportunistically shoots crates and NPC drones while travelling/scouting if no opponent is nearby. This *dealing damage* can repeatedly reset the regeneration clock for a mech that is already injured, even when passive restoration would provide hundreds of HP before the next hunter duel.

Unlike the rejected `quiet-farm` experiment (silence before t=60 regardless of health), this is exclusively **injury and healing-window dependent**, at any match time. `MECH_TUNE={"injured_farm_silence":0}` is unchanged baseline; `1` bypasses noncombat crate/NPC targeting when own HP <82% and no currently selected mech target, while preserving enemy targeting, gun/laser logic in combat, supply/cube collection, movement, threats, loot and health-independent farming. The economic cost is lost crate cubes/upgrades; this must be measured rather than assumed away. No other code changes.

## Independent paired screen
Pinned MIT independent physics proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb` (not authoritative scoring). Fresh 12 identical paired seeds per `(cooperative squad, one-entrant FFA) × (v1, v2, mixed opponents) × (toggle 0,1)`, **144 simulated matches**. Squad seeds 1930211–1930222, FFA seeds 1940211–1940222. Audit all per-seed placements and 95% paired bootstrap intervals, W/L/T, low finishes ≤2 points, early deaths, rear damage, stuck time, out-of-zone time, damage dealt, and decision latency. Run 300-record native and sandbox Docker conformance.

Reject if any six group mean-placement decreases or any low-placement count rises; FFA mean rear damage and outside-zone time must not rise. If screen passes, run independent ≥64 FFA and ≥32 squad holdout **per opponent population**, review endgame, and rerun native+Docker conformance on same gameplay commit before proposing production. No automatic merge or official entry; no competitor research/code in repository. All prior submissions/history untouched.

## Final 144-game screen — 22 November 2026

**REJECTED under prespecified directional and safety gates; no holdout and no main promotion.** [All six paired comparisons and validated aggregate, run 44936324146](https://github.com/pucaru/curly-succotash/actions/runs/44936324146), **SUCCESS**, evaluated the exact candidate and control at commit `580b4c43b5932934c21223876197b657ab95f2e7`. [300-observation native plus Docker sandbox conformance, run 44936324107](https://github.com/pucaru/curly-succotash/actions/runs/44936324107), **SUCCESS** at the same commit. All 144 per-seed placements validated. These are private-free proxy games, **not** the official 48-match score.

| Opponent | Squad control→silence | One-hero FFA control→silence | Paired FFA delta [95% bootstrap CI], W/L/T | FFA rear damage delta | FFA out-of-zone delta |
| --- | ---: | ---: | --- | ---: | ---: |
| v1 | 0.333→0.333 | 9.917→10.000 | +0.083 [0.000,+0.250], 1/0/11 | −5.6 | +0.000s |
| v2 | **0.167→0.000** | 5.833→6.583 | +0.750 [0.000,+2.250], 1/0/11 | **+12.2** | +0.000s |
| mixed | 0.750→1.000 | **7.167→6.833** | −0.333 [−2.500,+2.000], 2/3/7 | **+10.2** | **+2.700s** |

Squad paired deltas: v1 +0.000 [0,0], 0/0/12; v2 **−0.167 [−0.500,0.000]**, 0/1/11; mixed +0.250 [−0.167,+0.833], 2/1/9. Low placements ≤2 points: squads v1 12→12, v2 12→12, mixed 12→11; FFAs v1 0→0, v2 1→1, mixed 1→1. One-entrant FFA action latency peaked at 9.67ms in the proxy (not an official sandbox latency measure).

**Squad structural diagnostics** (12 paired seeds per opponent): deaths before 60 seconds v1 7→7, v2 7→7, mixed 3→3. Mean squad death time v2 **57.49→52.88s** and mean damage dealt **1308.87→912.73**, both adverse. Mixed death time 91.45→93.45s and rear damage 604.12→418.73, but mean stuck time rose 4.68→5.33s. Squad out-of-zone time remained zero.

The health-dependent quiet shooting decision has real effects in the approximate simulator, including a sampled v2 FFA placement gain. It nevertheless loses v2 squad placement, mixed FFA placement, mixed FFA zone safety, and rear protection in both v2 and mixed FFA. The v2 FFA mean gain is not enough to satisfy any precommitted robust gate. Do **not** promote, combine opportunistically with rejected experiments, or spend additional held-out seeds on the identical mechanism without new causal evidence.

Production `main` remains at `60b5438`; no official practice/entry submission, competitor research/code, prior commit rewrites, or production gameplay changes. The official ≥6.00 practice objective remains unverified.
