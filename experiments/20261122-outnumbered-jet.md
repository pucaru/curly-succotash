# Outnumbered jump-plus-jet evasion — independent structural experiment

**Status: initial screen pending, 2026-11-22.** Fixed production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official practice score measurement or entry submission.

## Official rule and new causal mechanism

The organizer's `mechfight/1` protocol (§7) permits vertical ascent up to about 60m using jump plus airborne boost (jets), while the original bot only jumps after repeated wall stalls; its ordinary `cover`/`flee` behavior moves horizontally. A single grounded mech cannot outrun a coordinated pack of hunters with comparable horizontal speed. Vertical flight may create breathing room or reach building heights that walkers cannot, at the cost of energy and aerial exposure. This is not a retune of the previous rejected panic-boost experiment, which never commanded a deliberate jump plus sustained airborne jet.

Candidate `MECH_TUNE={"outnumbered_jet":1}`: when squad-like inference remains active, ≥3 fresh threats are within 115m, the bot took damage ≤1.2s ago, HP <86%, energy >75, and 18s have elapsed since any prior escape, initiate a single 2.2s aerial retreat. Hold boost while airborne and energy >26, retain horizontal retreat away from current threats, preserving all existing weapon targeting, fire and other movement logic. Toggle `0` is exact production control. Unit test exercises jump, flight boost and toggle.

## Prespecified independent evaluation

Pinned MIT independent proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`, an approximate model of official physics, not official practice scoring. 12 fresh matched seeds for squad 1890211–1890222 and one-entrant FFA 1900211–1900222 versus v1/v2/mixed each, two variants; 144 games. Analyze paired mean placement, W/L/T, bootstrap 95% CI, low finishes ≤2 points, FFA rear damage, zone exposure and peak proxy decision latency. Verify native 300-observation and sandbox Docker conformance.

Reject for any negative group mean placement, increase in low placements, FFA rear damage or FFA zone exposure. If all pass, run ≥64 new paired FFA and ≥32 paired squad seeds **per opponent** with a final-circle and energy/height review before considering production. No auto-merge, no official submission, no competitor research/code in repo, no rewrite of prior commits.
