# Threat-aware lightning spacing — 22 November 2026, 06:32 SGT

**EXPERIMENT ONLY; not validated; do not promote.** Production immutable baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

## New causal mechanism
Earlier isolated-lightning spacing increased v2 FFA placement on 12 paired seeds by +1.750 but increased v2/mixed FFA rear damage and reduced mixed FFA placement. The likely failure mechanism is retreating away from one selected target while entering a second shooter's firing lane. This isolated experiment preserves the prior useful near-lightning separation **only when no second fresh enemy is within 165m and no damage was recently received from a substantially different direction**. It selects a zone-safe, reachable point with multiple directional fallbacks. Non-lightning combat, targeting, upgrades, farming, loot, and all default behavior are unchanged. `MECH_TUNE={"lightning_flank_veto":0}` exactly restores the immutable production policy.

## Prespecified gates
Pinned independently implemented MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. 144 total games (12 FRESH paired seeds for each of cooperative squad/one-entrant FFA, v1/v2/mixed, candidate/control), squad 2253301–2253312, FFA 2254301–2254312. Require complete paired results, 95% bootstrap intervals, low finishes (≤2), FFA rear damage, zone exposure, squad early deaths <60s, stuck time, damage dealt, action latency and native+Docker 300-observation conformance.

Reject on any subgroup negative mean placement, increased low finishes, FFA rear damage or zone exposure, or early squad deaths. Even if screen passes, do not promote without fresh ≥64 FFA and ≥32 squad seeds per opponent profile and endgame/adversarial review. Official 48-game practice score NOT measured; local proxy score does not establish official ≥6.00. No tournament submission or Git history rewrite. No public-competitor research/code in repo.

## Outcome
Await independent Actions screen and conformance. No results or improvement claimed.
