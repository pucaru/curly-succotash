# Inertia-aware sustained solo-duel strafing — 22 November 2026, 07:30 SGT

**Experimental only. Not promoted.** Control is immutable `main` commit `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official practice score measured.

## Structural mechanism
The official rulebook says ground motion accelerates rather than instantly changing direction (ground_accel ~58.5 m/s², walk_speed ~11.7 m/s). During a duel the production mech reverses its strafe direction every **0.7–1.4 seconds**, spending a material fraction of each brief orbit cancelling lateral velocity rather than moving far enough to cross an opponent's firing arc. This is distinct from earlier stuck-recovery experiments: here the mech is not stuck on map geometry; it is cancelling its *own* sideways motion by command.

Toggle `MECH_TUNE={"duel_orbit_commit":1}` creates longer 2.8–3.8-second lateral arcs only in `mode=="duel"` and reverses before an unsafe-zone or immediate obstacle direction. All target selection, weapon controls, cover/zone logic, FFA hold steering, and other modes stay unchanged. Toggle 0 exactly reproduces production decision logic.

## Preregistered validation
Pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Two toggles × v1/v2/mixed opponents × cooperative house-like squad vs one-hero FFA × 12 fresh paired seeds = **144 proxy simulations**, squad 2313301–2313312, FFA 2314301–2314312. A paired aggregator will check all seed sets, mean placements and 95% bootstrap CI, low finishes (≤2 points), FFA rear damage, zone exposure, squad early deaths, sticking and damage dealt, and proxy action latency. Separate native 300-observation and sandbox Docker conformance required.

Reject if any subgroup's mean placement worsens, low finishes increase, FFA rear damage rises, or FFA outside-zone time increases, or squad early deaths worsen. Even a safe positive screen is **not sufficient**: use held-out ≥64 FFA and ≥32 squad per opponent profile, adverse opponent/endgame review and conformance before any production consideration. Independent simulator is not the official 48-match scorer; cannot validate ≥6.00.

No official tournament entry submission, account authorization, rewrite of submitted commits, restoration of removed public-research section, or competitor-derived code. External conceptual research remains outside this repository.

## Results
Screening and conformance not yet inspected. No score claimed.
