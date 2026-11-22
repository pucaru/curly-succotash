# Stalled weapon pursuit failsafe — 22 November 2026

**Isolated opt-in experiment, initial paired screen pending.** Control: production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Official 48-match practice result remains unmeasured.

## Causal hypothesis

An independent **diagnostic-only** baseline squad run found the mech spending the majority of its short life in `weapon` mode without actually acquiring a secondary weapon in multiple seeds (e.g., seed 3672001: 671 weapon-mode decisions, death 96.4s, gun only, 0 kills; seed 3672005: 1001 weapon decisions, death 139.1s, gun only). Merely tuning laser search distance/value was previously rejected. Unlike those constant sweeps, this proposal detects objectively stalled pursuit regardless of pickup value: if the *same* chosen weapon has not become at least 12m closer after 8 seconds of continuous `weapon`-mode decisions, temporarily veto it for 25 seconds. Preserve pursuit if making progress, and preserve all combat, upgrade, zone and FFA rules. The independently tested toggle `MECH_TUNE={"weapon_stall_veto":0}` reproduces baseline.

## Precommitted evaluation

Pinned independent MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Test toggle 0 vs 1 against v1/v2/mixed with both coordinated squad and one-hero FFA, 12 fresh paired seeds per cell = 144 games. Squad seeds 2681301–2681312, FFA seeds 2682301–2682312. Audit matched placements with bootstrap 95% CI, low-score outcomes ≤2, rear damage, zone exposure, squad early deaths, damage dealt, stuck time and maximum action latency; candidate-enabled native 300-observation and Docker sandbox conformance.

Reject if any opponent/mode subgroup mean placement worsens, more low finishes, higher mean FFA rear damage/zone exposure, or increased early squad deaths. Positive screen alone is not promotion: require held-out ≥64 FFA + ≥32 squad **per population**, end-circle robustness and protocol audit. Local simulator results are approximate, not organizer's official scorer. No official entry, main/history rewrite or competitor research/code added.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/weapon-stall-veto.yml) · [Conformance workflow](https://github.com/pucaru/curly-succotash/actions/workflows/weapon-stall-veto-check.yml).

## Final independent matched-screen audit — rejected, 22 Nov 2026

**All 144 matches, exact paired-seed coverage, six cells, and aggregate passed** in [workflow 44968338109](https://github.com/pucaru/curly-succotash/actions/runs/44968338109). [Candidate-enabled 300-observation native/Docker conformance 44968338159](https://github.com/pucaru/curly-succotash/actions/runs/44968338159) and [default conformance 44968338218](https://github.com/pucaru/curly-succotash/actions/runs/44968338218) passed. Game-policy commit evaluated: `41118bfb7a58a814efb34e9c13dece8bb440c71f`. No official practice score.

| Opponents | Squad control→candidate | One-hero FFA control→candidate | Paired FFA Δ [95% bootstrap CI], W/L/T | Mean FFA rear Δ | Mean FFA zone Δ |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.750→0.750 | 9.333→9.083 | **−0.250** [−1.250,+0.500], 1/1/10 | −45.0 | +0.000 s |
| v2 | 0.333→0.083 | 6.500→6.750 | +0.250 [−1.000,+1.500], 6/4/2 | **+321.9** | **+0.275 s** |
| mixed | 0.583→0.667 | 6.750→7.000 | +0.250 [−0.333,+1.083], 2/2/8 | **+82.8** | **+0.008 s** |

Squad paired delta with 95% CI/W-L-T: v1 +0.000 [0,0], 0/0/12; **v2 −0.250 [−0.667,0], 0/2/10**; mixed +0.083 [0,+0.250], 1/0/11. Low finishes ≤2: v1 squad 11→11 and FFA 0→0, v2 squad 12→12 and FFA 1→1, mixed squad 12→12 and FFA 0→0. Squad early deaths (<60s): v1 5→5, **v2 6→7**, mixed 2→1. Squad v2 mean death time 75.21→64.42s and damage dealt 1425.52→1091.12. Squad mixed damage dealt 2320.12→2536.12. Peak independent FFA action latency 11.84ms (not Docker guarantee).

**REJECT; no further holdout or production promotion.** A targeted retry limit addresses an observable inefficiency but still reduced v1 FFA placement and v2 squad placement; v2 and mixed FFA rear/zone safety gates also failed. The v2/mixed FFA mean gains are insufficient. Abandoning a non-progressing weapon pursuit can leave the mech exposed or force alternative navigation while coordinated hunters approach. Avoid rerunning this exact 8s/12m stall-veto hypothesis without a new causal mechanism. Keep `main` immutable and no official submission.
