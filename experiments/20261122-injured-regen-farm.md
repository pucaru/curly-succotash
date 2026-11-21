# Injured noncombat farming versus healing-window discipline — 22 November 2026

**PRE-REGISTERED, not yet evaluated.** Immutable production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official practice run or tournament submission; local scores are approximate.

## Causal hypothesis
Official `mechfight/1` §7 says health regeneration starts after **5 s without dealing or receiving damage**, at **45 HP/s**, and stops in the zone. The original bot opportunistically shoots crates and NPC drones while travelling/scouting if no opponent is nearby. This *dealing damage* can repeatedly reset the regeneration clock for a mech that is already injured, even when passive restoration would provide hundreds of HP before the next hunter duel.

Unlike the rejected `quiet-farm` experiment (silence before t=60 regardless of health), this is exclusively **injury and healing-window dependent**, at any match time. `MECH_TUNE={"injured_farm_silence":0}` is unchanged baseline; `1` bypasses noncombat crate/NPC targeting when own HP <82% and no currently selected mech target, while preserving enemy targeting, gun/laser logic in combat, supply/cube collection, movement, threats, loot and health-independent farming. The economic cost is lost crate cubes/upgrades; this must be measured rather than assumed away. No other code changes.

## Independent paired screen
Pinned MIT independent physics proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb` (not authoritative scoring). Fresh 12 identical paired seeds per `(cooperative squad, one-entrant FFA) × (v1, v2, mixed opponents) × (toggle 0,1)`, **144 simulated matches**. Squad seeds 1930211–1930222, FFA seeds 1940211–1940222. Audit all per-seed placements and 95% paired bootstrap intervals, W/L/T, low finishes ≤2 points, early deaths, rear damage, stuck time, out-of-zone time, damage dealt, and decision latency. Run 300-record native and sandbox Docker conformance.

Reject if any six group mean-placement decreases or any low-placement count rises; FFA mean rear damage and outside-zone time must not rise. If screen passes, run independent ≥64 FFA and ≥32 squad holdout **per opponent population**, review endgame, and rerun native+Docker conformance on same gameplay commit before proposing production. No automatic merge or official entry; no competitor research/code in repository. All prior submissions/history untouched.

## Result
Pending CI. This report must not be interpreted as a passing or promotion-ready candidate.
