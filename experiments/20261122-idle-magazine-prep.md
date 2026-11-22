# Threat-gated gun magazine preparation (22 November 2026)

**Status: pending 144-game screening; NOT promoted.** Immutable production control: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. The new `TUNE.idle_reload` defaults 0, leaving prior bot behavior exactly intact.

## Causal defect

The production `aim_and_fire` returns immediately if no enemy or farm target is selected, before the gun reload decision. As a consequence, an empty gun can stay empty throughout quiet travel, then incur a full 2.4-second reload at the start of the next encounter. This modification starts reload with zero ammo immediately if the gun is not already reloading, and proactively reloads ≤65% magazine in quiet periods with no threat tracks, recent damage, recent weapon sounds or near acoustic contacts. Combat targeting, shooting, zone, movement, upgrades, and loot remain unchanged.

## Reproducibility / gate

Pinned third-party MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Paired 0 vs 1 variant, v1/v2/mixed opponents, 12 fresh cooperative-squad seeds per population (3175101–3175112), 12 one-hero FFA seeds per population (3176101–3176112). Total 144 independent games; aggregate validates all rows and reports paired bootstrap 95% CIs, low finishes, rear damage, out-of-zone, early deaths, damage dealt and latency. Candidate-enabled native 300-observation and Docker sandbox conformance separately required.

Predefined gate: reject any opponent/mode placement decrease, increased early deaths or low-scoring finishes, or increased FFA rear damage or out-of-zone exposure. If screening passes, require fresh ≥64 FFA + ≥32 squad matched holdout each opponent group and endgame review before any production consideration. **Local means are not official 48-match practice scores.** No official entry, no main promotion without validation, and no public competitor research in the repository.

## Completed results — 22 November 2026, 11:33 SGT

**Final decision: REJECT; do not promote or expand to holdout.** Both candidate-enabled [native 300-observation plus sandbox Docker conformance](https://github.com/pucaru/curly-succotash/actions/runs/44980740849) and baseline-default [conformance](https://github.com/pucaru/curly-succotash/actions/runs/44980740807) passed. All six comparison cells, 144 simulated games, and aggregate successfully completed in [benchmark run 44980740902](https://github.com/pucaru/curly-succotash/actions/runs/44980740902); [aggregate artifact 14737238667](https://github.com/pucaru/curly-succotash/actions/runs/44980740902/artifacts/14737238667). Gameplay experiment commit: `4775deabe66b6e27e4721b059cf588fc40eed04f`. All tests used the candidate toggle explicitly, baseline control 0 versus candidate 1, pinned independent MIT proxy, and 12 matched fresh seeds per opponent/mode.

| Opponents | Squad control→candidate (Δ; paired 95% bootstrap CI) | One-hero FFA control→candidate (Δ; paired CI) | FFA rear damage Δ | FFA zone time Δ |
| --- | --- | --- | ---: | ---: |
| v1 | 0.333→0.250 (**−0.083**; [−0.250,+0.000]) | 8.917→8.500 (**−0.417**; [−1.000,+0.000]) | −169.0 | +0.000s |
| v2 | 0.167→0.000 (**−0.167**; [−0.417,+0.000]) | 5.917→6.667 (+0.750; [+0.167,+1.417]) | −137.9 | +0.000s |
| mixed | 0.917→0.833 (**−0.083**; [−0.500,+0.250]) | 7.250→7.583 (+0.333; [+0.000,+1.000]) | **+13.3** | +0.000s |

Matched W/L/T (squad then FFA): v1 0/1/11 and 0/2/10; v2 0/2/10 and 4/0/8; mixed 1/1/10 and 1/0/11. Low-scoring finishes (≤2 pts) in FFA: v1 1→1, v2 3→2, mixed 2→2. Squad deaths before 60s: v1 6→6, v2 8→8, mixed 4→4. Mean squad damage dealt fell v1 1294.45→1031.47; v2 670.05→610.95; mixed 2581.88→2554.95. Mean squad survival seconds fell v1 74.78→72.03; v2 65.00→55.91; mixed 101.10→98.42. Peak proxy FFA action latency 7.06ms; this does not guarantee sandbox timing.

**Interpretation.** The code-level empty-magazine no-target reload gap is real, but proactively preparing the magazine does not translate into robust placement improvements. The candidate does improve v2 FFA (+0.750) while losing v1 FFA (−0.417), losing all three squad mean placement subgroups, and increasing mixed FFA rear damage. Reload activity can introduce a vulnerability when an attacker arrives immediately after a quiet interval and also alters future movement/combat trajectories. The matched proxy cannot isolate the causal share attributable to empty-magazine recovery versus the partial-magazine rule. A future investigation would need distinct triggers and diagnostics rather than retesting this combination unchanged.

The apparent v2 FFA benefit is **not** an official practice result or acceptable compensation for the squad regressions. The production `main` hash was reverified unchanged at `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No official tournament entry, practice submission, production merge, history rewrite, or external competitor research addition.
