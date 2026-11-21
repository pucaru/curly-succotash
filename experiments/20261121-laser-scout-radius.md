# Laser scouting distance: pre-registered A/B sweep — 21 November 2026

Status: exploratory / **not a promotion**. Production main is `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

## Hypothesis

The current `TUNE["laser_search_radius"] = 270.0` causes the bot to travel a long distance for a laser, potentially increasing exposure to the coordinated practice squad. A shorter radius could preserve early survival while a longer one could increase laser acquisition and late-match survival in free-for-alls. Changing the radius alone leaves combat, steering, and protocol behavior identical.

## Precommitted comparison

- Variants: **200.0**, **270.0 control**, **340.0**, injected as `MECH_TUNE` at runtime; the bot source and its 270.0 production default are unchanged.
- Evaluator: one tested hero against **15** independently fighting opponents for FFA; cooperative squad benchmark versus 15 coordinated house-style opponents. No eight-copy hero FFA shortcut.
- Independent MIT simulator pinned to `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`; it is **not** the official organizer engine.
- Paired **24 squad seeds beginning 2101121** and **24 one-hero FFA seeds beginning 2201121** for each of three opponent populations: v1, v2, mixed v1/v2.
- Outcomes: mean placement points (`16-place`) and worst-case/diagnostic data. Nine jobs, 432 simulation matches total.
- Gate: no change to production on first sweep. Require an additional untouched 64-seed one-hero FFA and 32-seed cooperative squad holdout (distinct starting seeds) if any candidate improves FFA while preserving squad and stronger-opponent results. Reject inconsistent/regressive changes.

The official Mech Royale competition scores placement, not kills; finals are free-for-all with new private seeds. Simulator scores are only a proxy.

Workflow: `.github/workflows/laser-scout-radius.yml`.
Never rewrite submitted commits, change main, restore deleted public research, or make an official tournament submission as part of this branch.
