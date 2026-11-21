# Isolated lightning short-risk precharge guard — 22 November 2026

**PRE-REGISTERED; UNVALIDATED. DO NOT PROMOTE.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No organizer practice or tournament entry authorized.

## Causal mechanism
The official protocol specifies that charging a laser halves movement speed and lightning (45 m radius, 30° yaw cone) shorts a charged laser and disables it for 2 s. The baseline starts charging even while a freshly seen lightning-equipped opponent within 49 m is aiming into our position. This can incur slowed movement without earning laser damage. The opt-in guard avoids starting a **new** laser charge only in this fresh geometric short-risk scenario. It preserves all already-started charges, gun aim/fire, opponent selection, zone logic, combat movement, upgrades, and all other behavior. No claim that a noisy proxy precisely models opponent lightning.

## Prespecified screen
Exact control `MECH_TUNE={"laser_short_guard":0}` (baseline code behavior) vs candidate value `1`; independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New paired seeds squad 2130211–2130222 and one-hero FFA 2140211–2140222, each against v1/v2/mixed opponents: 144 matches total.

Record subgroup matched placement, 95% paired bootstrap confidence intervals, W/L/T, low finishes (≤2), early squad deaths <60 seconds, damage dealt, rear-hit damage, stuck time, zone exposure, and proxy action latency. Reject candidate on *any* negative subgroup mean placement, increase in low finishes, or FFA rear damage/zone exposure. Native 300-observation plus Docker sandbox conformance required. Passing screen only justifies new heldout seeds ≥64 FFA and ≥32 squad per opponent, end-circle review, and fresh conformance. Do not confuse proxy scores with official 48-game practice.

No external competitor research/code in repository. No main change, official entry, or history rewrite.