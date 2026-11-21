# Shootable-target selection under competing hunters — preregistered causal experiment

**Status: initial 144-game screen pending, 2026-11-22.** Production baseline remains `60b5438af4d45af989f63bffcbe0b03250a23ae4`, no official practice result known.

## New mechanism versus rejected occluded duel movement experiment

The failed `occluded-duel-lane` experiment changed **movement** when the *already selected* target was behind a barrier, causing major v2 FFA regression. An independent code inspection reveals a different issue: `enemy()` ranks attacker recency/stickiness/HP before visibility, while `aim_and_fire()` forbids primary gun shots when a target is behind an arena wall. With two recent enemies, the bot can deliberately aim at an unshootable enemy when another could be damaged immediately.

Opt-in `MECH_TUNE={"visible_target_switch":1}` narrows candidate targets to those with fresh (<1.8s) observation positions and a direct uninflated map line when at least two enemies are candidates **and at least one is exposed**. Existing priority scoring is retained among exposed enemies. If no exposed alternative, fall back to the original target selection exactly. Flag 0 is control. No changes to navigation, aim/fire, upgrades or mode inference. A unit test forces two opponents, one hidden and one exposed, and asserts 0 picks the occluded high-priority one while 1 picks the exposed one.

## Local protocol and placement gates

Pinned independent MIT proxy simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; results are approximate, not official. Compare control/candidate matched new seeds 1870211–1870222 (cooperative squad) and 1880211–1880222 (one-entrant FFA), against v1/v2/mixed opponents: 2×3×2×12 = **144** simulated games.

Require 300-observation native and Docker sandbox conformance, nonnegative paired mean placement and no rise in placements ≤2 for every subgroup, plus no average FFA increase in rear damage or out-of-zone time. Summarize bootstrap 95% CI, W/L/T, low-finishes, and latency. If any safety or subgroup regression, reject without holdout. Otherwise holdout new seeds ≥64 one-bot FFA + ≥32 squad **per opponent group**, endgame and conformance audit before any possible production proposal.

No production change, official submission, Git history rewrite, or public-competitor research/code.
