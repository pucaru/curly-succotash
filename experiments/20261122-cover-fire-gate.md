# Defensible-cover firing vs false-cover fire suppression — 22 November 2026

**PRE-REGISTERED; UNVALIDATED. DO NOT PROMOTE.** Immutable production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

## Mechanism and isolation

The prior LOS-verified waypoint screen (experiment/cover-los-gate-20261122-0530) found that all-exposed points may be labelled `cover` under baseline. Rejecting such waypoints increased v1/v2 squad damage but caused v1 FFA zone exposure and v2 FFA rear damage. Here **the original cover waypoint, movement and combat-selection paths are left unchanged**. Only the existing low-HP `cover`-mode fire suppression is bypassed when **no observed enemy sightline is actually blocked from the chosen waypoint**. All firing still passes baseline target, range, aim, cooldown, and LOS requirements. All genuine cover behavior and all `flee`-mode quiet recovery remain as before. Control `MECH_TUNE={"cover_fire_gate":0}`, candidate `1`; no edits to main.

## Prespecified evaluation

Pinned independently implemented MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New 12 fresh paired seeds per mode×opponent: squad 2251301–2251312; one-hero FFA 2252301–2252312; v1/v2/mixed. 144 matches. All subgroup paired mean-placement, 95% paired bootstrap CIs, wins/losses/ties, low placements ≤2, deaths <60s, rear damage, zone exposure, stuck time, damage dealt, action latency. Any mean-placement regression or increase in low finishes, FFA rear damage or FFA out-of-zone, or early squad deaths rejects. Native and Docker 300-observation official kit conformance required. If promising, independent fresh >=32 squad and >=64 FFA seeds per opponent profile, adversarial/end-circle review and repeat conformance BEFORE any promotion proposal. The proxy cannot verify the official practice objective ≥6.00.

No official tournament entry, account authorization, competitor code/research in repo, or rewrite of submitted history.
