# Stalled weapon pursuit failsafe — 22 November 2026

**Isolated opt-in experiment, initial paired screen pending.** Control: production main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Official 48-match practice result remains unmeasured.

## Causal hypothesis

An independent **diagnostic-only** baseline squad run found the mech spending the majority of its short life in `weapon` mode without actually acquiring a secondary weapon in multiple seeds (e.g., seed 3672001: 671 weapon-mode decisions, death 96.4s, gun only, 0 kills; seed 3672005: 1001 weapon decisions, death 139.1s, gun only). Merely tuning laser search distance/value was previously rejected. Unlike those constant sweeps, this proposal detects objectively stalled pursuit regardless of pickup value: if the *same* chosen weapon has not become at least 12m closer after 8 seconds of continuous `weapon`-mode decisions, temporarily veto it for 25 seconds. Preserve pursuit if making progress, and preserve all combat, upgrade, zone and FFA rules. The independently tested toggle `MECH_TUNE={"weapon_stall_veto":0}` reproduces baseline.

## Precommitted evaluation

Pinned independent MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Test toggle 0 vs 1 against v1/v2/mixed with both coordinated squad and one-hero FFA, 12 fresh paired seeds per cell = 144 games. Squad seeds 2681301–2681312, FFA seeds 2682301–2682312. Audit matched placements with bootstrap 95% CI, low-score outcomes ≤2, rear damage, zone exposure, squad early deaths, damage dealt, stuck time and maximum action latency; candidate-enabled native 300-observation and Docker sandbox conformance.

Reject if any opponent/mode subgroup mean placement worsens, more low finishes, higher mean FFA rear damage/zone exposure, or increased early squad deaths. Positive screen alone is not promotion: require held-out ≥64 FFA + ≥32 squad **per population**, end-circle robustness and protocol audit. Local simulator results are approximate, not organizer's official scorer. No official entry, main/history rewrite or competitor research/code added.

[Benchmark workflow](https://github.com/pucaru/curly-succotash/actions/workflows/weapon-stall-veto.yml) · [Conformance workflow](https://github.com/pucaru/curly-succotash/actions/workflows/weapon-stall-veto-check.yml).
