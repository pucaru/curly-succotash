# Outnumbered jump-plus-jet evasion — independent structural experiment

**Status: initial screen pending, 2026-11-22.** Fixed production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official practice score measurement or entry submission.

## Official rule and new causal mechanism

The organizer's `mechfight/1` protocol (§7) permits vertical ascent up to about 60m using jump plus airborne boost (jets), while the original bot only jumps after repeated wall stalls; its ordinary `cover`/`flee` behavior moves horizontally. A single grounded mech cannot outrun a coordinated pack of hunters with comparable horizontal speed. Vertical flight may create breathing room or reach building heights that walkers cannot, at the cost of energy and aerial exposure. This is not a retune of the previous rejected panic-boost experiment, which never commanded a deliberate jump plus sustained airborne jet.

Candidate `MECH_TUNE={"outnumbered_jet":1}`: when squad-like inference remains active, ≥3 fresh threats are within 115m, the bot took damage ≤1.2s ago, HP <86%, energy >75, and 18s have elapsed since any prior escape, initiate a single 2.2s aerial retreat. Hold boost while airborne and energy >26, retain horizontal retreat away from current threats, preserving all existing weapon targeting, fire and other movement logic. Toggle `0` is exact production control. Unit test exercises jump, flight boost and toggle.

## Prespecified independent evaluation

Pinned MIT independent proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, an approximate model of official physics, not official practice scoring. 12 fresh matched seeds for squad 1890211–1890222 and one-entrant FFA 1900211–1900222 versus v1/v2/mixed each, two variants; 144 games. Analyze paired mean placement, W/L/T, bootstrap 95% CI, low finishes ≤2 points, FFA rear damage, zone exposure and peak proxy decision latency. Verify native 300-observation and sandbox Docker conformance.

Reject for any negative group mean placement, increase in low placements, FFA rear damage or FFA zone exposure. If all pass, run ≥64 new paired FFA and ≥32 paired squad seeds **per opponent** with a final-circle and energy/height review before considering production. No auto-merge, no official submission, no competitor research/code in repo, no rewrite of prior commits.

## Final 144-game audit — 2026-11-22

**REJECTED under the predeclared hard safety gate. No holdout, no main promotion, no official submission.** [All 144 independent proxy matches and aggregate run 44932109475](https://github.com/pucaru/curly-succotash/actions/runs/44932109475) succeeded, and [300-observation native plus Docker sandbox conformance run 44932109415](https://github.com/pucaru/curly-succotash/actions/runs/44932109415) succeeded at evaluated head `22fd9002e822237aefaf06d4a6adbf04bb76ec85`.

| Opponent | Squad control→jet | FFA control→jet | Paired FFA delta [95% bootstrap CI], W/L/T | FFA rear delta | FFA out-zone delta |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.167→0.167 | 9.667→9.667 | +0.000 [0,0], 0/0/12 | +0.0 | +0.000s |
| v2 | 0.000→0.083 | 5.833→6.500 | +0.667 [-1.083,+2.667], 2/1/9 | -48.0 | +0.000s |
| mixed | 0.833→0.833 | 6.667→6.667 | +0.000 [-0.250,+0.250], 1/1/10 | **+24.5** | +0.000s |

Squad paired deltas and 95% intervals: v1 +0.000 [0,0], 0/0/12; v2 +0.083 [0,0.250], 1/0/11; mixed +0.000 [-0.417,+0.333], 2/1/9. Low-placement counts ≤2 points: squads v1 12→12, v2 12→12, mixed 11→11; FFAs v1 0→0, v2 2→1, mixed 0→0. Peak proxy FFA action latency 8.77ms, not an official Docker timing guarantee.

**Additional squad survival metrics** across 12 matched seeds per population:

| Opponents | Deaths before 60s control→jet | Mean death time | Mean rear damage | Mean stuck seconds | Mean outside-zone |
| --- | --- | --- | --- | --- | --- |
| v1 | 6→6 | 73.32→73.32s | 500.8→500.8 | 1.64→1.64s | 0→0s |
| v2 | 5→4 | 74.71→81.87s | 489.5→643.8 | 3.27→2.63s | 0→0s |
| mixed | 4→3 | 82.38→107.00s | 682.9→556.4 | 2.25→9.64s | 0→0s |

The vertical escape creates an intriguing but inconclusive survival signal in some squad seeds and +0.667 sampled v2 FFA mean, but the hard mixed FFA rear-damage regression (+24.5), v2 squad rear increase (+154.4) and increased mixed squad sticking show the policy is not robust. No official proof of the ≥6 target; the independent local simulator remains approximate. A future distinct investigation may examine altitude-aware routing to reachable rooftops, but should not simply rerun this jet trigger or weaken gates.
