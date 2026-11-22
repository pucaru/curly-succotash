# Baseline damage-to-elimination causal diagnostic — 22 Nov 2026

Diagnostic-only independent MIT simulator instrumentation (pinned `b76c216d8a7829e14409a42058eea93e46e9ccdb`) for baseline main `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Does not modify production bot or score tournament matches. No competitor research imported.

**Question:** Against one-at-a-time cooperative hunters, is poor placement associated with low hit frequency, damage spread over multiple enemies, stale target tracks, unproductive defensive modes, or rear-hit exposure?

Six new baseline squad seeds per opponent population (v1/v2/mixed), 18 independent proxy games. Record *per-target* damage from official-shaped hit events, kills, damaged target count, top-target share, target switches/stale tracks, movement modes and rear-damage causes. Disaggregate actor damage from crate/NPC damage to avoid treating farming as kills. This is descriptive diagnosis rather than a causal A/B improvement; do not promote changes based on it.

[Diagnostic workflow](https://github.com/pucaru/curly-succotash/actions/workflows/hunter-diagnostics.yml).

No official practice score, submission, production write or history rewrite.
