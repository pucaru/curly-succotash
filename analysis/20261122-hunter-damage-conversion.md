# Baseline damage-to-elimination causal diagnostic — 22 Nov 2026

Diagnostic-only independent MIT simulator instrumentation (pinned `b76c216d8a7829e14409a42058eea93e46e9ccdb`) for baseline main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Does not modify production bot or score tournament matches. No competitor research imported.

**Question:** Against one-at-a-time cooperative hunters, is poor placement associated with low hit frequency, damage spread over multiple enemies, stale target tracks, unproductive defensive modes, or rear-hit exposure?

Six new baseline squad seeds per opponent population (v1/v2/mixed), 18 independent proxy games. Record *per-target* damage from official-shaped hit events, kills, damaged target count, top-target share, target switches/stale tracks, movement modes and rear-damage causes. Disaggregate actor damage from crate/NPC damage to avoid treating farming as kills. This is descriptive diagnosis rather than a causal A/B improvement; do not promote changes based on it.

[Diagnostic workflow](https://github.com/pucaru/curly-succotash/actions/workflows/hunter-diagnostics.yml).

No official practice score, submission, production write or history rewrite.

## Completed independent diagnostic — 22 November 2026 (18 proxy squad games)

[All 3 diagnostic jobs, 18 per-match JSON records and complete CI run 44968062381](https://github.com/pucaru/curly-succotash/actions/runs/44968062381) **SUCCESS**. No experiment modification or production change. Only 6 fresh squad seeds per opponent profile, descriptive association rather than causal proof. Pinned independent MIT simulator is an approximation, not official 48-match scoring.

| Opponent | Mean placement pts | Kills / game | Gun only at death | Weapon-mode share of decision ticks | ≥501 weapon-mode ticks | Mean damage to mechs | Mean dominant-target damage fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.333 | 0.333 | 4/6 | 46.3% | 2/6 | 1420.5 | 92.5% |
| v2 | 0.167 | 0.000 | 2/6 | 43.2% | 3/6 | 1352.6 | 82.5% |
| mixed | 0.500 | 0.333 | 4/6 | 47.7% | 3/6 | 2064.5 | 89.2% |

Across all 18 independent matches, **17/18 placement outcomes scored ≤2**, **15/18 had zero kills**, **10/18 ended with gun only**, and **8/18 recorded >500 weapon-mode decisions**. Weapon-mode decisions amounted to 45.6% of decision ticks pooled across all matches, versus an already high dominant-target damage fraction. This **does not establish target switching as the primary failure**: raw concentration of damage among hit targets is high. Instead, repeated decisions to chase an apparent secondary weapon can coexist with inability to acquire it or survive long enough to realize offensive value. There are also v2 cases with successfully equipped secondaries and no kills, so weapon access is not the whole explanation.

Concrete v1 cases: seed 3672001 spent 671 decision ticks in weapon mode before death at 96.4 s, died gun-only with 900 damage and zero kills; seed 3672005 spent 1001 weapon ticks before death at 139.1 s, gun-only with 720 damage and zero kills. In mixed seed 3672005, 1001 weapon ticks and gun-only with zero kills. A diagnostic instrumentation caveat: weapon-mode tick count does **not** reveal whether the bot pursued one pickup continuously or switched among many; target-switch counts measure combat targets, not pickups. The next experiment must measure / intervene in genuine lack of progress, not infer it from counts.

The independent opt-in weapon-stall-veto screen is on separate branch `experiment/weapon-stall-veto-20261122-0900` and does not modify this diagnostic branch. Diagnostic source only records original hit/mode signals and never supplies opponent knowledge to production. Do not extrapolate an official ≥6 practice score.
