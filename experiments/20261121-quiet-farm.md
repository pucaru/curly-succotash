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
