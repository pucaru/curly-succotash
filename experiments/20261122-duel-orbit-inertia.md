# Inertia-aware sustained solo-duel strafing — 22 November 2026, 07:30 SGT

**Experimental only. Not promoted.** Control is immutable `main` commit `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official practice score measured.

## Structural mechanism
The official rulebook says ground motion accelerates rather than instantly changing direction (ground_accel ~58.5 m/s², walk_speed ~11.7 m/s). During a duel the production mech reverses its strafe direction every **0.7–1.4 seconds**, spending a material fraction of each brief orbit cancelling lateral velocity rather than moving far enough to cross an opponent's firing arc. This is distinct from earlier stuck-recovery experiments: here the mech is not stuck on map geometry; it is cancelling its *own* sideways motion by command.

Toggle `MECH_TUNE={"duel_orbit_commit":1}` creates longer 2.8–3.8-second lateral arcs only in `mode=="duel"` and reverses before an unsafe-zone or immediate obstacle direction. All target selection, weapon controls, cover/zone logic, FFA hold steering, and other modes stay unchanged. Toggle 0 exactly reproduces production decision logic.

## Preregistered validation
Pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Two toggles × v1/v2/mixed opponents × cooperative house-like squad vs one-hero FFA × 12 fresh paired seeds = **144 proxy simulations**, squad 2313301–2313312, FFA 2314301–2314312. A paired aggregator will check all seed sets, mean placements and 95% bootstrap CI, low finishes (≤2 points), FFA rear damage, zone exposure, squad early deaths, sticking and damage dealt, and proxy action latency. Separate native 300-observation and sandbox Docker conformance required.

Reject if any subgroup's mean placement worsens, low finishes increase, FFA rear damage rises, or FFA outside-zone time increases, or squad early deaths worsen. Even a safe positive screen is **not sufficient**: use held-out ≥64 FFA and ≥32 squad per opponent profile, adverse opponent/endgame review and conformance before any production consideration. Independent simulator is not the official 48-match scorer; cannot validate ≥6.00.

No official tournament entry submission, account authorization, rewrite of submitted commits, restoration of removed public-research section, or competitor-derived code. External conceptual research remains outside this repository.

## Final independent screening results — 22 November 2026

**REJECTED.** All 144 proxy games across 12 fresh matched control/candidate seeds for each of 6 populations plus the aggregate **completed successfully**: [paired benchmark run 44962273212](https://github.com/pucaru/curly-succotash/actions/runs/44962273212). [Baseline native/Docker conformance 44962273213](https://github.com/pucaru/curly-succotash/actions/runs/44962273213) and [candidate-enabled 300-observation native/Docker conformance 44962315277](https://github.com/pucaru/curly-succotash/actions/runs/44962315277) both succeeded. An earlier initial workflow [44962221408](https://github.com/pucaru/curly-succotash/actions/runs/44962221408) failed **before any simulations** due incorrect harness filenames; corrected in commit `4a58f0db`, without repeating previously completed games.

| Opponents | Squad control→candidate (Δ) | FFA control→candidate (Δ) |
| --- | --- | --- |
| v1 | 0.667→0.167 (−0.500) | 8.167→8.417 (+0.250) |
| v2 | 0.167→0.250 (+0.083) | 8.583→7.167 (−1.417) |
| mixed | 0.583→0.417 (−0.167) | 8.333→9.750 (+1.417) |

Paired mean placement deltas with bootstrap 95% confidence intervals (W/L/T): v1 squad **−0.500 [−0.917,−0.167]** (0/5/7), v1 FFA +0.250 [−0.167,+0.833] (2/1/9); v2 squad +0.083 [−0.250,+0.417] (3/2/7), v2 FFA **−1.417 [−4.333,+1.083]** (6/5/1); mixed squad **−0.167 [−0.667,+0.250]** (2/3/7), mixed FFA +1.417 [+0.333,+2.750] (5/0/7). Low-point finishes ≤2: squad v1 12→12, v2 12→12, mixed 12→12; FFA v1 0→0, **v2 0→4**, mixed 1→1. FFA rear-damage changes: **v1 +70.2**, v2 −55.2, **mixed +125.8**. FFA zone exposure changes +0.000s in all populations.

Squad early deaths <60s control→candidate: v1 4→4, v2 5→4, mixed 3→3. Mean squad death time: v1 115.99→92.21s, v2 77.55→95.21s, mixed 107.32→92.72s. Squad rear damage: v1 290.25→552.28, v2 158.47→195.94, mixed 386.27→269.99. Squad time stuck: v1 8.94→8.92s, v2 4.40→4.33s, mixed 19.28→17.85s. Squad time outside zone: v1 2.46→0.00s, v2 0→0s, mixed 4.51→4.51s. Squad mean damage dealt **decreased in all profiles**: v1 1394.03→1117.05, v2 1203.86→1121.88, mixed 1975.73→1311.40. Peak proxy FFA action latency was 7.86ms (not a Docker latency guarantee).

**Decision:** Do not promote or spend larger holdout on this exact orbit-timing hypothesis. Multiple prespecified safety/placement gates failed: v1/mixed squad placement, v2 FFA placement and low finish count, v1/mixed FFA rear damage. The mixed FFA advantage cannot compensate. The longer orbit may mitigate continuous back-and-forth movement in some scenarios, but worsens damage conversion and positional exposure. The independent MIT simulator is approximate; **no official 48-game practice score** or ≥6.00 verification. Production `main` and prior submitted history unchanged; no tournament submission or competitor research added.

