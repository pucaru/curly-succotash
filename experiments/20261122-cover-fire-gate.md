# Defensible-cover firing vs false-cover fire suppression — 22 November 2026

**REJECTED AFTER COMPLETE 144-MATCH PROXY EVALUATION. DO NOT PROMOTE.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

## Mechanism and isolation

The prior LOS-verified waypoint screen (experiment/cover-los-gate-20261122-0530) found that all-exposed points may be labelled `cover` under baseline. Rejecting such waypoints increased v1/v2 squad damage but caused v1 FFA zone exposure and v2 FFA rear damage. Here **the original cover waypoint, movement and combat-selection paths are left unchanged**. Only the existing low-HP `cover`-mode fire suppression is bypassed when **no observed enemy sightline is actually blocked from the chosen waypoint**. All firing still passes baseline target, range, aim, cooldown, and LOS requirements. All genuine cover behavior and all `flee`-mode quiet recovery remain as before. Control `MECH_TUNE={"cover_fire_gate":0}`, candidate `1`; no edits to main.

## Prespecified evaluation

Pinned independently implemented MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New 12 fresh paired seeds per mode×opponent: squad 2251301–2251312; one-hero FFA 2252301–2252312; v1/v2/mixed. 144 matches. All subgroup paired mean-placement, 95% paired bootstrap CIs, wins/losses/ties, low placements ≤2, deaths <60s, rear damage, zone exposure, stuck time, damage dealt, action latency. Any mean-placement regression or increase in low finishes, FFA rear damage or FFA out-of-zone, or early squad deaths rejects. Native and Docker 300-observation official kit conformance required. If promising, independent fresh >=32 squad and >=64 FFA seeds per opponent profile, adversarial/end-circle review and repeat conformance BEFORE any promotion proposal. The proxy cannot verify the official practice objective ≥6.00.

No official tournament entry, account authorization, competitor code/research in repo, or rewrite of submitted history.

## Completed experiment — 22 November 2026, 05:50 SGT

**REJECTED.** All six comparative jobs and aggregate completed **SUCCESS** at evaluated commit `03e3173f54a203d93af9aa6f0642af7c6f4b93b7`: [144-match independent paired benchmark 44953053982](https://github.com/pucaru/curly-succotash/actions/runs/44953053982). Official-kit 300-observation native and Docker checks and deterministic regression tests **SUCCESS**: [conformance 44953053948](https://github.com/pucaru/curly-succotash/actions/runs/44953053948). Independent simulator is approximate, **not** the organizer's 48-game practice score.

| Opponents | Squad control → candidate | One-hero FFA control → candidate | FFA paired Δ [95% bootstrap CI], W/L/T |
| --- | ---: | ---: | --- |
| v1 | 0.500 → 0.583 | 8.750 → 9.667 | +0.917 [0,+2.333], 3/0/9 |
| v2 | 0.167 → 0.333 | **5.833 → 5.750** | **−0.083 [−2.083,+1.917]**, 5/5/2 |
| mixed | 1.167 → 1.167 | 6.750 → 6.833 | +0.083 [−1.750,+2.000], 1/1/10 |

Squad paired Δ [95% CI], W/L/T: v1 +0.083 [0,+0.250], 1/0/11; v2 +0.167 [0,+0.417], 2/0/10; mixed +0.000 [0,0], 0/0/12. Low placements ≤2: squad v1 12→12, v2 12→12, mixed 10→10; FFA v1 0→0, **v2 1→3**, mixed 2→2.

| Opponents | FFA rear damage Δ | FFA outside-zone Δ | Squad deaths before 60s | Squad rear damage control → candidate | Squad damage dealt control → candidate |
| --- | ---: | ---: | ---: | ---: | ---: |
| v1 | −112.8 | 0.000s | 5→4 | 700.73→591.42 | 1444.88→1795.50 |
| v2 | −48.9 | **+2.742s** | **3→4** | 368.68→492.09 | 900.16→1037.70 |
| mixed | −46.4 | 0.000s | **4→5** | 486.27→570.05 | 2826.48→2831.09 |

Mean squad death time / stuck / zone exposure: v1 83.82→89.88s / 10.78→12.57s / 5.75→5.74s; v2 82.40→80.88s / 9.18→17.15s / 3.62→5.91s; mixed 99.64→97.27s / 20.12→20.58s / 6.26→6.26s. Local proxy peak action latency 8.07ms.

**Pre-registered gates violated** by v2 FFA placement regression −0.083, low outcomes 1→3, and outside-zone +2.742s, as well as extra deaths before 60s in both v2 and mixed squads. No holdout or promotion justified despite v1 FFA +0.917, lower rear damage in all FFA groups, and increased v1/v2 squad damage dealt. In v2 squad, the added damage did not translate into survival: early deaths increased and stuck time almost doubled. Preserving fire during unprotected recovery can sacrifice positioning or healing; needs a different safety-conditional mechanism, not another unconditional toggle.

Production `main` remains `60b5438af4d45af989f63bffcbe0b03250a23ae4`, without tournament submission, organizer practice measurement, account action, history rewrite, or competitor research/code. The official ≥6.00 objective remains **unverified**.
