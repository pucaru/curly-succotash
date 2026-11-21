# Isolated lightning-envelope spacing — 22 November 2026

**PRE-REGISTERED SCREEN: NOT VALIDATED FOR PROMOTION.** Production baseline is immutable `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official practice or tournament submission is authorized. This experiment is distinct from prior rejected zone, duel, defensive-facing, and generic escape hypotheses.

## Causal mechanism

The official rules specify that lightning has a short range (45m) but can deliver 60 damage at a 0.25s cadence, with a 30-degree aiming cone. The baseline bot's stationary single-hunter duel and nearest-enemy strafe can enter or remain inside that range; this risks sustained damage and laser shorts. Unlike blanket fleeing, the candidate ONLY applies when the currently selected opponent was observed under 2s ago, carries lightning, is within 58m and own HP exceeds 25%. It walks/boosts away to a zone-safe 14–34m position while preserving enemy targeting and firing. It does not change aim, choice of target, route algorithm, loot valuation, recovery, upgrades, or any behavior when the toggle is zero. Do not infer that proxy enemy loadouts match the hidden expert squad.

## Audit plan (before simulation)

`MECH_TUNE={"lightning_spacing":0}` is exact unchanged main behavior; `1` enables the experiment. Pinned MIT independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Compare 12 matched FRESH seeds each for squad and **one-entrant FFA** against v1, v2, and mixed opponents, two policies (144 total, 72 per policy), squad seeds 2050211–2050222 and FFA 2060211–2060222. Audited placements and 95% paired bootstrap intervals, low finishes <=2, W/L/T, early squad deaths before 60s, squad dealt damage, rear hit damage, stuck duration, zone exposure and proxy decision latency.

Reject immediately if any of six populations lose mean placement, any increases in low-placement finishes, or any FFA group increases average rear damage or zone exposure. If promising on screening, require new holdout >=64 FFA and >=32 squad seeds *per opponent profile*, end-circle review, native 300-observation and Docker sandbox checks before proposal. No automatic production merge or official practice submission. Do not store public competitor research/code in repo. All previously submitted commits stay unchanged.

## Screening status

**COMPLETE, REJECTED.** Details below. No evidence of score >=6.00 from the official 48-match scorer.

## FINAL 144-game audit — 22 November 2026, 03:41 SGT

**REJECTED: does not meet prespecified FFA placement and rear-damage safety gates.** All 144 independent paired simulations completed successfully at code commit `65d57098154b1c4d6ceaa70bdd43ba530909950e`. [Validated aggregate + six comparison jobs, Actions 44941681018](https://github.com/pucaru/curly-succotash/actions/runs/44941681018) **SUCCESS**. [300-observation native and Docker conformance, Actions 44941680958](https://github.com/pucaru/curly-succotash/actions/runs/44941680958) **SUCCESS** at the same code commit. These are **proxy simulations**, not organizer practice results. Held-out 64-FFA/32-squad evaluation **not warranted** given negative groups. Main remains `60b5438`.

| Opponent population | Cooperative squad control→candidate | One-entrant FFA control→candidate | Paired FFA delta [95% bootstrap CI]; W/L/T | FFA rear-damage Δ | FFA zone Δ |
| --- | ---: | ---: | --- | ---: | ---: |
| v1 | 0.167→0.167 | 8.500→8.500 | +0.000 [0.000,0.000]; 0/0/12 | +0.0 | +0.000s |
| v2 | 0.417→0.417 | 5.250→7.000 | **+1.750 [+0.750,+3.000]; 8/0/4** | **+25.5** | +0.000s |
| mixed | 0.417→0.583 | **7.583→7.417** | **−0.167 [−0.583,+0.167]; 1/2/9** | **+78.5** | +0.000s |

Squad paired delta 95% bootstrap intervals: v1 +0.000 [0,0] (0/0/12); v2 +0.000 [−0.250,+0.250] (1/1/10); mixed +0.167 [0,+0.417] (2/0/10). Low placements (≤2): squad v1 12→12, v2 12→12, mixed 11→10; FFA v1 1→1, v2 3→2, mixed 1→1. Average squad deaths before 60s: v1 4→4, v2 5→4, mixed 5→5. Mean squad death time: v1 77.40→77.42s, v2 78.75→81.28s, mixed 83.28→88.15s. Mean squad damage dealt: v1 1460.63→1460.63, v2 1391.62→1461.15, mixed 1510.31→1661.10. Mean squad rear damage: v1 462.80→462.80, v2 452.93→560.13, mixed 509.92→409.92. Squad stuck time: v1 2.98→2.98s, v2 3.42→4.78s, mixed 6.78→6.52s. Squad out-of-zone: v1 0→0s, v2 2.46→2.46s, mixed 0→0s. Peak proxy FFA action latency 10.01ms (separate successful native+Docker conformance, not a sandbox latency guarantee).

**Interpretation:** Extremely large measured v2 FFA improvement on 12 paired seeds is a *real effect in this proxy*, with bootstrap CI above zero; however, retreating from lightning-armed enemies is not safe across opponent profiles. It compromises mixed FFA placement and increases rear-hit exposure in v2 and mixed FFA. This may be a tactical tradeoff or stochastic path divergence, not proof of improvement under hidden official house hunters. The v2 squad does not gain placement on average despite reduced early deaths. Do not adopt selected v2-only evidence or combine with previously rejected experiments absent independent new mechanism. **Production not promoted, no official tournament entry/practice submission, no public competitor research/code or history rewrite. Official target ≥6.00 remains unverified.**
