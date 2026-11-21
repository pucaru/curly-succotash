# Killed-mech ghost-track eviction — isolated experiment (2026-11-22)

**Status: screening pending.** Fixed production baseline `60b5438af4d45af989f63bffcbe0b03250a23ae4`. No change to production main or prior submitted history; official practice score unknown.

## Causal bug and minimal correction

The protocol's `kill` event provides the authoritative ID of the mech we just eliminated. Existing `Bot.update()` only increments a kill counter. The dead mech remains in `self.tracks` for up to 13 seconds and may remain a combat candidate for up to 5.2 seconds, because `enemy()` permits recent-memory targets. In a solo versus coordinated hunter squad, that can waste a decisive second or more on a non-existent opponent instead of switching to a live attacker, potentially magnifying rear damage. This is not a parameter-tuning hypothesis: the observation includes an explicit state change that current policy discards.

Candidate `MECH_TUNE={"kill_track_purge":1}`: on confirmed own kill, delete the matching tracked mech ID and clear `last_enemy_id` if it was focused. `0` exactly preserves the original policy. No other target scoring, vision, firing, movement, or FFA logic changes. Unit test verifies both toggles.

## Independent prespecified gates

Pinned MIT proxy `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Fresh 12 paired seeds across squad and one-entrant FFA versus v1/v2/mixed, 2 toggle settings: 144 games total. Squad seeds 1850211–1850222 and FFA 1860211–1860222.

Require nonnegative mean placement in **each** of six mode/population groups, no increase in low placements (≤2 points), no increase in mean FFA rear damage or outside-zone seconds. Report matched-seed placement deltas, bootstrap confidence intervals, W/L/T, action latency. Native 300-observation and Docker sandbox conformance must pass.

Screen passing alone is not enough: ≥64 FFA and ≥32 squad new paired held-out seeds per population and final-circle diagnostics before production consideration. Do not submit, merge automatically, or include any external public competitor research.
