# Isolated lightning-envelope spacing — 22 November 2026

**PRE-REGISTERED SCREEN: NOT VALIDATED FOR PROMOTION.** Production baseline is immutable `60b5438af4d45af989f63bffcbe0b03250a23ae4`; no official practice or tournament submission is authorized. This experiment is distinct from prior rejected zone, duel, defensive-facing, and generic escape hypotheses.

## Causal mechanism

The official rules specify that lightning has a short range (45m) but can deliver 60 damage at a 0.25s cadence, with a 30-degree aiming cone. The baseline bot's stationary single-hunter duel and nearest-enemy strafe can enter or remain inside that range; this risks sustained damage and laser shorts. Unlike blanket fleeing, the candidate ONLY applies when the currently selected opponent was observed under 2s ago, carries lightning, is within 58m and own HP exceeds 25%. It walks/boosts away to a zone-safe 14–34m position while preserving enemy targeting and firing. It does not change aim, choice of target, route algorithm, loot valuation, recovery, upgrades, or any behavior when the toggle is zero. Do not infer that proxy enemy loadouts match the hidden expert squad.

## Audit plan (before simulation)

`MECH_TUNE={"lightning_spacing":0}` is exact unchanged main behavior; `1` enables the experiment. Pinned MIT independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Compare 12 matched FRESH seeds each for squad and **one-entrant FFA** against v1, v2, and mixed opponents, two policies (144 total, 72 per policy), squad seeds 2050211–2050222 and FFA 2060211–2060222. Audited placements and 95% paired bootstrap intervals, low finishes <=2, W/L/T, early squad deaths before 60s, squad dealt damage, rear hit damage, stuck duration, zone exposure and proxy decision latency.

Reject immediately if any of six populations lose mean placement, any increases in low-placement finishes, or any FFA group increases average rear damage or zone exposure. If promising on screening, require new holdout >=64 FFA and >=32 squad seeds *per opponent profile*, end-circle review, native 300-observation and Docker sandbox checks before proposal. No automatic production merge or official practice submission. Do not store public competitor research/code in repo. All previously submitted commits stay unchanged.

## Screening status

Workflow scheduled by isolated branch commit; actual results pending. No evidence of score >=6.00 from the official 48-match scorer.
