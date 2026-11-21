# Killed-mech ghost-track eviction — isolated experiment (2026-11-22)

**Status: screening pending.** Fixed production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No change to production main or prior submitted history; official practice score unknown.

## Causal bug and minimal correction

The protocol's `kill` event provides the authoritative ID of the mech we just eliminated. Existing `Bot.update()` only increments a kill counter. The dead mech remains in `self.tracks` for up to 13 seconds and may remain a combat candidate for up to 5.2 seconds, because `enemy()` permits recent-memory targets. In a solo versus coordinated hunter squad, that can waste a decisive second or more on a non-existent opponent instead of switching to a live attacker, potentially magnifying rear damage. This is not a parameter-tuning hypothesis: the observation includes an explicit state change that current policy discards.

Candidate `MECH_TUNE={"kill_track_purge":1}`: on confirmed own kill, delete the matching tracked mech ID and clear `last_enemy_id` if it was focused. `0` exactly preserves the original policy. No other target scoring, vision, firing, movement, or FFA logic changes. Unit test verifies both toggles.

## Independent prespecified gates

Pinned MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Fresh 12 paired seeds across squad and one-entrant FFA versus v1/v2/mixed, 2 toggle settings: 144 games total. Squad seeds 1850211–1850222 and FFA 1860211–1860222.

Require nonnegative mean placement in **each** of six mode/population groups, no increase in low placements (≤2 points), no increase in mean FFA rear damage or outside-zone seconds. Report matched-seed placement deltas, bootstrap confidence intervals, W/L/T, action latency. Native 300-observation and Docker sandbox conformance must pass.

Screen passing alone is not enough: ≥64 FFA and ≥32 squad new paired held-out seeds per population and final-circle diagnostics before production consideration. Do not submit, merge automatically, or include any external public competitor research.

## Completed screening audit — 2026-11-22

**REJECTED. No large holdout, production promotion or official submission.** [All 144 proxy games and aggregate run 44931180918](https://github.com/pucaru/curly-succotash/actions/runs/44931180918) succeeded at evaluated code commit `ca9d9a84b1fda34e2a1fe6947566a3d58b6b48ea`; [300-observation native and Docker conformance run 44931178780](https://github.com/pucaru/curly-succotash/actions/runs/44931178780) also succeeded.

| Opponents | Squad control→candidate | FFA control→candidate | Paired FFA delta [95% bootstrap CI], W/L/T | FFA rear delta | FFA out-zone delta |
| --- | --- | --- | --- | ---: | ---: |
| v1 | 0.333→0.333 | 8.917→8.250 | **-0.667 [-2.083,+0.167]**, 1/2/9 | **+92.8** | +0.000s |
| v2 | 0.333→0.333 | 5.667→5.917 | +0.250 [-0.500,+1.083], 3/3/6 | -3.6 | +0.000s |
| mixed | 0.167→0.583 | 7.500→8.000 | +0.500 [-0.083,+1.250], 4/1/7 | **+177.7** | +0.000s |

Squad paired deltas: v1 +0.000 [0,0] W/L/T 0/0/12, v2 +0.000 [-0.250,+0.250] W/L/T 1/1/10, mixed +0.417 [+0.083,+0.833] W/L/T 4/0/8. Low placements ≤2: all squad cells 12→12, FFA v1 0→0, v2 2→2, mixed 1→1. Max proxy action latency 9.97ms. Any single subgroup negative placement or FFA increased rear damage fails a hard gate; this variant fails three gates despite positive mixed-squad results.

**Squad diagnosis** from the 12 per-seed engine diagnostics per cell:

| Opponents | Death before 60s, control→candidate | Mean death time | Rear damage | Stuck time | Outside-zone time |
| --- | --- | --- | --- | --- | --- |
| v1 | 5→5 | 98.35→97.52s | 178.7→289.8 | 4.60→4.58s | 5.71→5.71s |
| v2 | 7→6 | 83.26→86.95s | 335.1→366.8 | 7.10→12.23s | 5.44→5.58s |
| mixed | 4→2 | 97.93→112.82s | 272.6→220.5 | 3.22→7.72s | 3.34→5.76s |

The proxy mixed-squad gain is real in the sample but accompanied by more sticking and zone exposure, and fails independent v1 FFA safety. Simple ghost deletion is therefore not robust enough. No further rerun of this exact hypothesis without a fresh causal explanation. All numbers are independent approximate simulations, not an official tournament/48-match score. Production main/history untouched.
