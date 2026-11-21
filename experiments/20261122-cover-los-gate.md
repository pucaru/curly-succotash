# LOS-verified defensive cover — 22 November 2026

**PRE-REGISTERED; NOT VALIDATED. DO NOT PROMOTE.** Production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4` is untouched. No official practice run or tournament submission is authorized.

## Distinct causal mechanism

Baseline `find_cover` ranks 64 accessible nearby waypoints even when **all** candidates remain fully exposed to every observed nearby enemy. It can return an entirely exposed position as `mode=cover` and subsequently suppress offensive fire for low-HP users, despite providing no ballistic protection. The experiment explicitly rejects candidate waypoints with zero blocked enemy lines of sight. Existing unreachable-site checks, navigation, scoring, targeting, zone management, attack and steering remain unchanged. No gameplay changes are active for control (`MECH_TUNE={"cover_los_gate":0}`). Candidate enables only `cover_los_gate=1`.

This is distinct from previously rejected zone LOS-cover experiments: it tests whether the **cover classification itself** is false, rather than changing zone holding-point selection.

## Pre-registered screening criteria

Use pinned independent MIT simulator `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. New independent 12 matched paired seeds each for squad (2241301–2241312) and one-hero FFA (2242301–2242312), for each of v1/v2/mixed, 144 matches across control/candidate; any directional subgroup placement loss, low-placement increase, FFA rear-damage increase, FFA zone-exposure increase, or early squad death increase rejects. Record paired CIs, all subgroup W/L/T, damage dealt, early deaths, rear hits, stuck and outside-zone times. Native + Docker 300-observation conformance required. Promotion additionally requires all six independently heldout cells with fresh >=32 squad and >=64 FFA seeds, plus endgame study and sandbox verification. Proxy never equals official 48-game practice.

No public competitor research, private evaluation claims, production promotion, history rewrite or official submission.
