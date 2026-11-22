# Safe final approach to live pickups — independent paired screen (22 November 2026)

**Status: screening pending. Not promoted.** Immutable control baseline is main `60b5438af4d45af989f63bffcbe0b03250a23ae4`; in this branch the `safe_loot_arrival` toggle defaults to zero, retaining original gameplay.

## Causal hypothesis

The production six-metre navigation stop exceeds the official weapon collection and cube pickup radii. Unconditionally correcting that mismatch was separately tested for weapons and cubes and rejected for multiple opponent-safety regressions. This experiment instead closes just the final ~3 metres only when the selected pickup was observed within the last 1.25 seconds, no recently tracked opponent is within 155m, no recent weapon sound or damage was observed, and the pickup lies safely within the current / upcoming circle. It keeps the original stop in unsafe or stale situations. In other words, this is an explicit risk-gated final approach, not a rerun of either rejected unconditional fix.

## Independent test protocol

MIT-licensed external proxy pinned at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Exactly 144 new matched-seed matches: 12 cooperative-squad and 12 one-hero FFA each under v1/v2/mixed opponents, with candidate/control paired seed schedules 3075101–3075112 and 3076101–3076112. Each paired cell compares candidate and original behavior in separate processes. Native and sandboxed Docker 300-observation conformance with candidate toggle enabled; deterministic tests include active loot, hostile presence and stale goals.

Predefined *reject* gates: any mode/population mean placement regression, increases in low-scoring finishes or squad early deaths (<60s), FFA rear damage or out-of-zone time increase. Audit paired bootstrap 95% CIs, win/loss/ties, latencies, and matchup diagnostics. No expansion to fresh >=64 FFA + >=32 squad holdout unless all safety gates pass. End-circle behavior must be reviewed separately. Proxy results are NOT official 48-match practice results; no official tournament submission.

No external competitor strategy material or code is included.

## Completed independent paired screen — 22 November 2026

**Decision: REJECT.** All six matched control/candidate cells and aggregate completed successfully in [GitHub Actions 44976287914](https://github.com/pucaru/curly-succotash/actions/runs/44976287914), with [machine-generated aggregate artifact 14735763818](https://github.com/pucaru/curly-succotash/actions/runs/44976287914/artifacts/14735763818). Candidate-enabled [native 300-observation and sandbox Docker conformance 44976284699](https://github.com/pucaru/curly-succotash/actions/runs/44976284699) **passed**; production-default [conformance 44976287890](https://github.com/pucaru/curly-succotash/actions/runs/44976287890) also passed. Evaluated candidate and control at experimental workflow commit `51887676448dcb07d191063b4763ff753434e0d8`, with `safe_loot_arrival=1` versus 0 respectively. Verified unchanged original policy for control.

| Opponents | Squad mean 0→1 (Δ; 95% paired bootstrap CI) | One-hero FFA mean 0→1 (Δ; CI) | FFA rear damage Δ | FFA out-zone Δ |
| --- | --- | --- | ---: | ---: |
| v1 | 0.417→0.500 (+0.083; [−0.250,+0.500]) | **8.667→8.500 (−0.167; [−1.000,+0.500])** | **+140.9** | +0.000s |
| v2 | **0.167→0.000 (−0.167; [−0.500,+0.000])** | 6.250→8.250 (+2.000; [+0.583,+3.917]) | **+165.8** | −0.183s |
| mixed | **1.000→0.917 (−0.083; [−0.250,+0.000])** | 9.000→9.500 (+0.500; [−0.083,+1.250]) | **+56.1** | +0.000s |

Paired W/L/T counts, ordered squad then FFA: v1 1/1/10 and 2/2/8; v2 0/1/11 and 7/1/4; mixed 0/1/11 and 4/1/7. Low-score FFA finishes ≤2: v1 0→0, v2 2→1, mixed 0→0. Squad early deaths under 60 seconds: v1 6→6, **v2 7→9**, mixed 4→4. V2 squad mean damage dealt fell **1247.97→809.15**; mean survival time fell **63.95→48.38s**. Mixed squad rear damage rose **376.87→572.63**. Peak observed proxy FFA action latency was 8.97ms, not a statement about the private scorer's latency.

The v2 FFA improvement is not a valid production promotion because its rear damage rose, while v1 FFA and v2/mixed cooperative squad placements fell, and v2 squad early deaths increased. These violate the preregistered directional and safety gates. In particular, the apparently conservative final approach still alters exposures and later tactical trajectories even without a recently observed threat; low-risk pickup geometry at one instant is insufficient to guarantee downstream safety. Do not selectively optimize for the v2 FFA population; the local simulator only approximates the official house squad and cannot verify the official ≥6.00 practice goal.

**No further holdout warranted for this candidate.** Preserve production `main` at `60b5438af4d45af989f63bffcbe0b03250a23ae4`, leave the tournament entry untouched, and do not repeat this mechanism without a genuinely new causal diagnosis. The benchmark artifact's two table-column labels say "Cube-arrival" because the aggregator header was reused; its value=1 payload and seeded matchup results are for **safe_loot_arrival**, as confirmed by workflow environment and job logs. This naming cosmetic has no effect on the measured data.
