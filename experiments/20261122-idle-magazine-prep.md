# Threat-gated gun magazine preparation (22 November 2026)

**Status: pending 144-game screening; NOT promoted.** Immutable production control: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. The new `TUNE.idle_reload` defaults 0, leaving prior bot behavior exactly intact.

## Causal defect

The production `aim_and_fire` returns immediately if no enemy or farm target is selected, before the gun reload decision. As a consequence, an empty gun can stay empty throughout quiet travel, then incur a full 2.4-second reload at the start of the next encounter. This modification starts reload with zero ammo immediately if the gun is not already reloading, and proactively reloads ≤65% magazine in quiet periods with no threat tracks, recent damage, recent weapon sounds or near acoustic contacts. Combat targeting, shooting, zone, movement, upgrades, and loot remain unchanged.

## Reproducibility / gate

Pinned third-party MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Paired 0 vs 1 variant, v1/v2/mixed opponents, 12 fresh cooperative-squad seeds per population (3175101–3175112), 12 one-hero FFA seeds per population (3176101–3176112). Total 144 independent games; aggregate validates all rows and reports paired bootstrap 95% CIs, low finishes, rear damage, out-of-zone, early deaths, damage dealt and latency. Candidate-enabled native 300-observation and Docker sandbox conformance separately required.

Predefined gate: reject any opponent/mode placement decrease, increased early deaths or low-scoring finishes, or increased FFA rear damage or out-of-zone exposure. If screening passes, require fresh ≥64 FFA + ≥32 squad matched holdout each opponent group and endgame review before any production consideration. **Local means are not official 48-match practice scores.** No official entry, no main promotion without validation, and no public competitor research in the repository.
