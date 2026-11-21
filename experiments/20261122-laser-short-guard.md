# Isolated lightning short-risk precharge guard — 22 November 2026

**PRE-REGISTERED; UNVALIDATED. DO NOT PROMOTE.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No organizer practice or tournament entry authorized.

## Causal mechanism
The official protocol specifies that charging a laser halves movement speed and lightning (45 m radius, 30° yaw cone) shorts a charged laser and disables it for 2 s. The baseline starts charging even while a freshly seen lightning-equipped opponent within 49 m is aiming into our position. This can incur slowed movement without earning laser damage. The opt-in guard avoids starting a **new** laser charge only in this fresh geometric short-risk scenario. It preserves all already-started charges, gun aim/fire, opponent selection, zone logic, combat movement, upgrades, and all other behavior. No claim that a noisy proxy precisely models opponent lightning.

## Prespecified screen
Exact control `MECH_TUNE={"laser_short_guard":0}` (baseline code behavior) vs candidate value `1`; independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New paired seeds squad 2130211–2130222 and one-hero FFA 2140211–2140222, each against v1/v2/mixed opponents: 144 matches total.

Record subgroup matched placement, 95% paired bootstrap confidence intervals, W/L/T, low finishes (≤2), early squad deaths <60 seconds, damage dealt, rear-hit damage, stuck time, zone exposure, and proxy action latency. Reject candidate on *any* negative subgroup mean placement, increase in low finishes, or FFA rear damage/zone exposure. Native 300-observation plus Docker sandbox conformance required. Passing screen only justifies new heldout seeds ≥64 FFA and ≥32 squad per opponent, end-circle review, and fresh conformance. Do not confuse proxy scores with official 48-game practice.

No external competitor research/code in repository. No main change, official entry, or history rewrite.

## Completed 144-game independent screen — 2026-11-22, 04:42 SGT

**REJECTED. Do not promote, hold out, or resubmit this candidate.** All six paired-control/candidate jobs and aggregation completed **SUCCESS** at evaluated code commit `7e171941f804f10439fe4057937d97df34165f75`: [144-match reproducible evaluation, Actions 44947198832](https://github.com/pucaru/curly-succotash/actions/runs/44947198832). Independent native and Docker sandbox conformance [Actions 44947198758](https://github.com/pucaru/curly-succotash/actions/runs/44947198758) **SUCCESS**, 10 unit tests, native 300/300 and Docker 300/300 responses within 50ms. Simulator is approximate, **not the official 48-match practice score**.

| Opponent profile | Squad control→guard | One-hero FFA control→guard | Paired FFA Δ [95% bootstrap CI]; W/L/T | FFA rear damage Δ | FFA zone Δ |
| --- | ---: | ---: | --- | ---: | ---: |
| v1 | 0.250→0.250 | 7.500→7.500 | +0.000 [0,0]; 0/0/12 | +0.0 | +0.000s |
| v2 | 0.250→0.333 | 6.917→7.167 | +0.250 [−0.250,+0.917]; 2/2/8 | **+14.2** | +0.000s |
| mixed | **0.917→0.750** | **6.667→6.250** | **−0.417 [−1.250,0.000]; 0/1/11** | −0.5 | +0.000s |

Squad paired Δ and CI: v1 +0.000 [0,0] 0/0/12; v2 +0.083 [0,+0.250] 1/0/11; mixed **−0.167 [−0.500,0.000]** 0/1/11. Low placements ≤2: squad v1 12→12, v2 12→12, **mixed 10→11**; FFA v1 3→3, v2 3→3, **mixed 2→3**.

| Squad opponent | Early deaths before 60s | Mean death time | Mean rear damage | Mean stuck | Mean outside zone | Mean damage dealt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 4→4 | 90.23→90.23s | 343.84→343.84 | 5.59→5.59s | 2.23→2.23s | 1456.62→1456.62 |
| v2 | 4→2 | 84.02→92.13s | 187.65→193.28 | 2.20→2.23s | 0→0s | 1234.58→1465.21 |
| mixed | 2→2 | 116.55→117.38s | 317.70→292.48 | 7.15→7.16s | 2.08→2.08s | **1967.28→1847.28** |

Maximum one-hero FFA proxy action latency 7.71ms, not an official sandbox bound. The v2-only gain (and fewer early squad deaths) does not outweigh mixed-squad and mixed-FFA regressions or greater v2 FFA rear exposure. The mechanism trades laser offense for avoiding a potential short under a lightning-bearing target, but suppressing a charge during an imminent duel can sacrifice damage conversion; the mixed squad dealt 120 less damage on average. Avoid rerunning the same narrow trigger without a new causal design.

**Safety gates failed**: v2 FFA rear +14.2; mixed squad mean placement −0.167 and low-finish count +1; mixed FFA mean −0.417 and low-finish count +1. Holdout not justified. Production main remains `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official entry, official practice measurement, history rewrite, or public competitor research/code. Official ≥6.00 objective **not verified**.
