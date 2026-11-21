# Crate aiming height — corrective controlled experiment (21 November 2026)

**Status: experimental screening launched; score impact unknown.**
Base production SHA: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. All edits on an isolated, non-submitted branch. Current main remains unmodified.

## Bug hypothesis
Official observations provide `obs.crates` without a `kind` property. Original aiming code calls `active.get("kind","mech")`, treating crates as 9m-tall mechs and aiming at 4.5m instead of the intended small crate impact height (the original fallback for a non-mech/non-NPC was 1.4m but unreachable for crates). This can waste gun and laser shots, generate sound and impede cube/upgrades. The official rules describe crates as destructible loot; their true collision height is not specified in the text spec, so test plausible impact heights rather than assume a fix guarantees hits.

Change only center-z selection of actively targeted crates: `MECH_TUNE.crate_target_height` = 4.5 (exact production control), 1.4, 2.0 meters. Enemy/NPC aim unchanged. No other tactics, scoring or arena code modified.

## Preregistered test
Pin MIT-licensed independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb` (not official match engine). 24 new cooperative squad seeds 1024211–1024234, and 24 single-entrant FFA seeds 1034211–1034234 per variant × v1, v2 and mixed opponent profiles. Nine cells of 48, **432 total matches**. Report paired placement wins/losses/ties, early FFA deaths, rear damage, zone exposure and max latency.

Require no mean deterioration in any of six populations/modes, no increase in early deaths or outside-zone seconds. Candidates require an independent held-out ≥64 FFA and 32 squad fresh-seed games per opponent profile, collision check against true engine when possible, final-circle review, native/Docker conformance before any promotion. Crate effects can be negative if noisy farming alerts enemy squad.

No official tournament submission; no competitor source code or public competitor research stored in this repository. Preserve submitted history.

## Aggregation recovery — reporting failure, not a simulation failure

[Original 432-game screening run](https://github.com/pucaru/curly-succotash/actions/runs/44912264906): all **9/9 simulation cells passed**, as did [native/unit/Docker conformance](https://github.com/pucaru/curly-succotash/actions/runs/44912264689). The aggregate job failed before displaying the summary because GitHub Actions rendered YAML matrix value `2.0` as artifact suffix `2`, while our parser expected `2.0`. The aggregator also printed its first two numeric column labels in the wrong order.

The parser now canonicalizes integer-valued YAML floats and labels columns in the true `VALUES=(4.5,1.4,2.0)` order. A recovery workflow downloads the **original immutable nine artifacts by run ID** and recomputes the audit, without simulating a single extra game. No results have been promoted or discarded to hide the reporting failure.
