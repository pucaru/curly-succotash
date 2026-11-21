# LOS-verified defensive cover — 22 November 2026

**REJECTED AFTER 144 COMPLETED PROXY MATCHES. DO NOT PROMOTE.** Production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4` is untouched. No official practice run or tournament submission is authorized.

## Distinct causal mechanism

Baseline `find_cover` ranks 64 accessible nearby waypoints even when **all** candidates remain fully exposed to every observed nearby enemy. It can return an entirely exposed position as `mode=cover` and subsequently suppress offensive fire for low-HP users, despite providing no ballistic protection. The experiment explicitly rejects candidate waypoints with zero blocked enemy lines of sight. Existing unreachable-site checks, navigation, scoring, targeting, zone management, attack and steering remain unchanged. No gameplay changes are active for control (`MECH_TUNE={"cover_los_gate":0}`). Candidate enables only `cover_los_gate=1`.

This is distinct from previously rejected zone LOS-cover experiments: it tests whether the **cover classification itself** is false, rather than changing zone holding-point selection.

## Pre-registered screening criteria

Use pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New independent 12 matched paired seeds each for squad (2241301–2241312) and one-hero FFA (2242301–2242312), for each of v1/v2/mixed, 144 matches across control/candidate; any directional subgroup placement loss, low-placement increase, FFA rear-damage increase, FFA zone-exposure increase, or early squad death increase rejects. Record paired CIs, all subgroup W/L/T, damage dealt, early deaths, rear hits, stuck and outside-zone times. Native + Docker 300-observation conformance required. Promotion additionally requires all six independently heldout cells with fresh >=32 squad and >=64 FFA seeds, plus endgame study and sandbox verification. Proxy never equals official 48-game practice.

No public competitor research, private evaluation claims, production promotion, history rewrite or official submission.

## Completed independent evaluation — 22 November 2026, 05:42 SGT

**REJECTED.** Six of six matrix jobs plus aggregate **SUCCESS**, evaluated branch commit `4a61918bf5d9e24a4f33409b47e34ccee175e7e7`: [144-game matched screen 44952307147](https://github.com/pucaru/curly-succotash/actions/runs/44952307147). Native and Docker official-kit **300-observation conformance** and 11 unit tests all **SUCCESS**: [conformance 44952307146](https://github.com/pucaru/curly-succotash/actions/runs/44952307146). The six opponent×mode cells were run under one-hero FFA or 1-v-15 cooperative-squad simulation, not the organizer's official 48-match practice.

| Profile | Squad control → candidate | One-hero FFA control → candidate | Paired FFA Δ [95% bootstrap CI], W/L/T |
| --- | ---: | ---: | --- |
| v1 | 0.667 → 1.167 | 7.667 → 8.083 | +0.417 [−0.333,+1.250], 3/3/6 |
| v2 | 0.083 → 0.333 | **7.250 → 7.167** | **−0.083 [−1.250,+0.917]**, 3/4/5 |
| mixed | **1.083 → 0.917** | 6.583 → 7.583 | +1.000 [−0.250,+2.500], 5/3/4 |

Squad paired placement Δ [95% bootstrap CI] and W/L/T: v1 +0.500 [+0.083,+1.083], 4/0/8; v2 +0.250 [0,+0.667], 2/0/10; mixed **−0.167 [−1.000,+0.333]**, 2/1/9. Low finishes ≤2: squad v1 11→9, v2 12→11, mixed 10→10; FFA v1 0→0, v2 0→0, mixed 1→1.

| Profile | FFA rear damage Δ | FFA zone exposure Δ | Squad deaths <60s | Squad damage dealt control → candidate | Squad rear damage control → candidate |
| --- | ---: | ---: | ---: | ---: | ---: |
| v1 | −53.3 | **+1.783 s** | **4→5** | 1626.53→2586.14 | 502.98→592.33 |
| v2 | **+53.8** | +0.000 s | 8→6 | 970.80→1310.11 | 792.70→759.57 |
| mixed | −34.0 | +0.000 s | **3→4** | **2637.51→2499.81** | 479.77→432.74 |

Additional squad diagnostics (mean death time / stuck time / zone exposure): v1 81.62→80.47s / 10.43→1.08s / 4.24→0.00s; v2 64.72→80.67s / 1.40→1.39s / 0→0s; mixed 100.88→86.84s / 1.90→0.74s / 0→0s. Peak local proxy action latency 11.88 ms, not a sandbox worst-case assertion.

**Independent rejection gates violated:** v1 FFA outside-zone +1.783s, v2 FFA mean −0.083 and rear hits +53.8, mixed squad mean −0.167, v1 squad early deaths +1, and mixed squad early deaths +1. Although false-cover classification is a valid structural observation and the modification increased v1/v2 squad damage, rejecting exposed sites changes movement enough to regress cross-population placement and exposure. Reject without holdout or production promotion. Do not rerun identical geometry gating without a materially different causal design.

The first screening attempt encountered a missing branch-local `bench/one_hero_ffa.py` file, and a separate initial unit test double lacked the `inflated` keyword accepted by `Arena.clear`. Both were corrected before the **successful full 144-match evaluation**; neither failed job performed any placement simulation. No need to rerun completed matches.

Production `main` remains immutable `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official account action, submission, history rewrite, imported competitor code, or public-research content. The official mean ≥6.00 is **not verified**.
