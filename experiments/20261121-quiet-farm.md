# Quiet opening: suppress opportunistic loud crate and drone farming (21 November 2026)

**Status:** Low-cost early screen launched. No improvement claimed.
Production base `60b5438af4d45af989f63bffcbe0b03250a23ae4`; isolated branch only, default config unchanged. No competitor research, copying, public-research section or history rewrite.

## Mechanism
The official rules specify that gunshots carry audible cues up to 320m while footsteps carry only 40m, potentially revealing the mech to a coordinated squad before it has gear or cover. Our current policy fires at crates/drones opportunistically whenever no enemy is nearby, even if doing so advertises its location and interrupts HP regeneration. This experiment changes only *unthreatened non-mech farming*: suppress crate/drone aim before the cutoff, but still attack real enemy targets normally, resume farming immediately when independent FFA is detected or after taking damage, and return to normal behavior after the cutoff.

Control `MECH_TUNE.quiet_farm_until=0` exactly preserves production. Variants 60 seconds and 135 seconds. The trade-off is loss of early cubes, defensive upgrades and weapon drops; silence is only plausibly valuable if nearby opponents actually respond to sound.

## Cost-controlled screening
Pin MIT-licensed independent simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. The simulated squad is an approximation, not the official shared-vision house bots.

Twelve **new** paired squad seeds 1110211–1110222 and twelve single-entrant FFA seeds 1120211–1120222, for control/60/135 × v1/v2/mixed: nine jobs, 216 total matches. Unit/native and Docker conformance required. This is a **small screening sample only**, not evidence sufficient for promotion. Exact-seed auditor checks placements, matched wins/losses/ties, early deaths, rear damage, zone exposure and max runtime.

Strict safety gate: reject clear regressions. Positive candidates must be retested on **new** larger paired holdout samples (at least 64 FFA and 32 squad seeds per opponent type) before contemplating promotion. Do not make official submissions without explicit user approval.


## Screening results and independent validation decision

[All 9 cells and 216 fresh paired simulator games completed](https://github.com/pucaru/curly-succotash/actions/runs/44912563320), with [native/unit/Docker conformance success](https://github.com/pucaru/curly-succotash/actions/runs/44912563218). Max proxy action time 11.47ms.

| Opponents | Control squad | Control FFA | Quiet 60s squad | Quiet 60s FFA | Quiet 135s squad | Quiet 135s FFA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | 1.000 | 6.917 | 0.667 | 7.250 | 0.417 | 7.250 |
| v2 | 0.000 | 5.917 | 0.083 | 6.917 | 0.083 | 7.500 |
| mixed | 0.750 | 6.083 | 0.833 | 7.250 | 0.750 | 7.250 |

**Quiet 60s:** FFA +0.333/+1.000/+1.167 points (v1/v2/mixed), but cooperative v1 -0.333 (paired W/L/T 1/2/9), and v2 FFA out-of-zone exposure +0.34s. This does **not** pass preregistered promotion rules. The v1 squad paired mean delta has a rough 95% t interval [-1.115, +0.448], so the 12-seed screen alone cannot establish a stable penalty; conversely, FFA positives also need confirmation.

**Quiet 135s:** FFA +0.333/+1.583/+1.167, but v1 squad -0.583; v2 rear damage +220.7 and outside-zone exposure +0.14s. **Reject for promotion**; no holdout justified for this more extreme setting.

A deliberately diagnostic, independent 576-game holdout of quiet 60s vs unchanged control is launched on [experiment/quiet60-holdout-20261121-2230](https://github.com/pucaru/curly-succotash/tree/experiment/quiet60-holdout-20261121-2230) with 32 new squad +64 new FFA seeds per opponent per variant. That is not promotion. If the holdout fails any robustness gate, preserve original gameplay. No official submission or rewrite.
