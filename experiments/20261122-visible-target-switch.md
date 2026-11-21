# Shootable-target selection under competing hunters — preregistered causal experiment

**Status: initial 144-game screen pending, 2026-11-22.** Production baseline remains `60b5438af4d45af989f63bffcbe0b03250a23ae4`, no official practice result known.

## New mechanism versus rejected occluded duel movement experiment

The failed `occluded-duel-lane` experiment changed **movement** when the *already selected* target was behind a barrier, causing major v2 FFA regression. An independent code inspection reveals a different issue: `enemy()` ranks attacker recency/stickiness/HP before visibility, while `aim_and_fire()` forbids primary gun shots when a target is behind an arena wall. With two recent enemies, the bot can deliberately aim at an unshootable enemy when another could be damaged immediately.

Opt-in `MECH_TUNE={"visible_target_switch":1}` narrows candidate targets to those with fresh (<1.8s) observation positions and a direct uninflated map line when at least two enemies are candidates **and at least one is exposed**. Existing priority scoring is retained among exposed enemies. If no exposed alternative, fall back to the original target selection exactly. Flag 0 is control. No changes to navigation, aim/fire, upgrades or mode inference. A unit test forces two opponents, one hidden and one exposed, and asserts 0 picks the occluded high-priority one while 1 picks the exposed one.

## Local protocol and placement gates

Pinned independent MIT proxy simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; results are approximate, not official. Compare control/candidate matched new seeds 1870211–1870222 (cooperative squad) and 1880211–1880222 (one-entrant FFA), against v1/v2/mixed opponents: 2×3×2×12 = **144** simulated games.

Require 300-observation native and Docker sandbox conformance, nonnegative paired mean placement and no rise in placements ≤2 for every subgroup, plus no average FFA increase in rear damage or out-of-zone time. Summarize bootstrap 95% CI, W/L/T, low-finishes, and latency. If any safety or subgroup regression, reject without holdout. Otherwise holdout new seeds ≥64 one-bot FFA + ≥32 squad **per opponent group**, endgame and conformance audit before any possible production proposal.

No production change, official submission, Git history rewrite, or public-competitor research/code.

## Completed 144-game audit — 2026-11-22

**REJECTED; no holdout, main change, or official entry.** [Complete independent 144-game screen and aggregate 44931745749](https://github.com/pucaru/curly-succotash/actions/runs/44931745749) passed; [300-observation native + Docker conformance 44931745630](https://github.com/pucaru/curly-succotash/actions/runs/44931745630) passed at evaluated code `e5f4db7e2d101284bd96594afa9e712dc4e93e17`. The proxy is not the official 48-match practice scorer.

| Opponent | Squad control→exposed | FFA control→exposed | Paired FFA delta [bootstrap 95% CI], W/L/T | FFA rear delta | FFA zone delta |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.167→0.083 | 9.167→9.000 | -0.167 [-0.500,+0.000], 0/1/11 | +8.2 | +0.000s |
| v2 | 0.250→0.167 | 7.083→6.833 | **-0.250 [-1.750,+0.917]**, 4/3/5 | **+422.4** | **+0.150s** |
| mixed | 0.333→0.583 | 8.167→8.333 | +0.167 [-1.083,+1.583], 2/3/7 | +35.5 | +0.000s |

Squad paired deltas with CI and W/L/T: v1 -0.083 [-0.250,0], 0/1/11; v2 -0.083 [-0.333,+0.167], 1/2/9; mixed +0.250 [-0.250,+1.000], 1/1/10. Low-placement counts (≤2 points): squads v1 12→12, v2 12→12, mixed 12→11; FFAs v1 0→0, v2 2→3, mixed 1→1. Peak independent proxy decision latency 39.48ms (below 50ms but an undesirable margin, not authoritative Docker latency).

**Additional squad diagnostics** from 12 fresh match records per group:

| Population | Early death <60s, control→candidate | Mean death time | Mean rear damage | Mean stuck time | Out-zone time |
| --- | --- | --- | --- | --- | --- |
| v1 | 6→6 | 63.25→63.02s | 74.9→266.6 | 0.55→0.52s | 0→0s |
| v2 | 6→5 | 70.70→65.10s | 402.1→245.3 | 2.42→2.42s | 0→0s |
| mixed | 6→4 | 73.61→85.68s | 448.7→331.6 | 1.67→1.74s | 0→0s |

The mixed squad improvement is neither broad nor sufficient: v1/v2 squad regress, v2 FFA incurs substantial extra rear damage and zone exposure. Even choosing a geometrically shootable enemy does not ensure a safer duel. Do not rerun exactly this hypothesis without a new mechanism, and do not confuse local FFA mean >6 with official 6 target. Production remains unchanged.
