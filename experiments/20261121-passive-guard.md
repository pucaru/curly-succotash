# Passive defensive facing — controlled placement experiment (21 November 2026)

**Status:** Screening launched; no outcome or promotion asserted.
Base production commit: `60b5438af4d45af989f63bffcbe0b03250a23ae4`. Isolated experiment: never alter main, prior submitted history or removed public-research section.

## Hypothesis
When declining combat in FFA, the bot resumes scanning while a known enemy remains close. Being hit outside its forward arc incurs 1.5× damage. Keep movement/combat unchanged and face a recent observed threat without firing (preserving regeneration).

Controlled variants: `MECH_TUNE={"passive_guard_range":0}` (production control), 120 m, 205 m.

## Prospective protocol
Use pinned independent MIT-licensed proxy engine `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb` (not the hidden official engine), 24 fresh squad seeds 933211–933234 and 24 one-hero FFA seeds 943211–943234 against v1, v2 and mixed bot populations. Exactly one tested bot in FFA. Paired same seeds per variant, nine jobs, 432 games.

Audit placement, matched-seed wins/losses/ties, early FFA deaths, rear damage, outside-zone seconds, and per-action latency. Reject any candidate with a negative mean placement delta in *any* opponent/mode or greater early deaths or zone exposure. Promising candidates require an independent 64 FFA + 32 squad fresh-seed holdout per opponent profile, final-circle checks and Docker/protocol conformance before any production decision.

No official submission or promotion without user authorization. No competitor-source research is stored here.
