# Safe final approach to live pickups — independent paired screen (22 November 2026)

**Status: screening pending. Not promoted.** Immutable control baseline is main `60b5438af4d45af989f63bffcbe0b03250a23ae4`; in this branch the `safe_loot_arrival` toggle defaults to zero, retaining original gameplay.

## Causal hypothesis

The production six-metre navigation stop exceeds the official weapon collection and cube pickup radii. Unconditionally correcting that mismatch was separately tested for weapons and cubes and rejected for multiple opponent-safety regressions. This experiment instead closes just the final ~3 metres only when the selected pickup was observed within the last 1.25 seconds, no recently tracked opponent is within 155m, no recent weapon sound or damage was observed, and the pickup lies safely within the current / upcoming circle. It keeps the original stop in unsafe or stale situations. In other words, this is an explicit risk-gated final approach, not a rerun of either rejected unconditional fix.

## Independent test protocol

MIT-licensed external proxy pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Exactly 144 new matched-seed matches: 12 cooperative-squad and 12 one-hero FFA each under v1/v2/mixed opponents, with candidate/control paired seed schedules 3075101–3075112 and 3076101–3076112. Each paired cell compares candidate and original behavior in separate processes. Native and sandboxed Docker 300-observation conformance with candidate toggle enabled; deterministic tests include active loot, hostile presence and stale goals.

Predefined *reject* gates: any mode/population mean placement regression, increases in low-scoring finishes or squad early deaths (<60s), FFA rear damage or out-of-zone time increase. Audit paired bootstrap 95% CIs, win/loss/ties, latencies, and matchup diagnostics. No expansion to fresh >=64 FFA + >=32 squad holdout unless all safety gates pass. End-circle behavior must be reviewed separately. Proxy results are NOT official 48-match practice results; no official tournament submission.

No external competitor strategy material or code is included.
