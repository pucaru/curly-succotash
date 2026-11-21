# FFA-only holding-point threat evasion — 2026-11-21

**Status: independent holdout in progress. Do not promote.** Production `main` remains at `60b5438af4d45af989f63bffcbe0b03250a23ae4`.

This separate branch tests a precise follow-up to the rejected global holding-point evasion: only enable the 200 m threat-repulsion bypass after the bot independently infers it is in a free-for-all (`self.ffa`); leave coordinated practice behavior as close as possible to baseline. The original policy remains the default when `MECH_TUNE.ffa_hold_evasion_radius=0`. Tests assert that practice mode does not evade at its reached holding point.

Commit trail: behavior `d0b8139a516e3d7353139d658454cb23c3dade76`; unit tests `99be3af1985ecb6f05d387f35e6b3bbec42a7f62`; one-entry evaluator `1a302c55c52f000ccedd9f2d7331cc71af832fc8`; independent holdout workflow `610aaf1e99b84b1cc2860aa4f6e5b39f117587c4`.

Fixed MIT-licensed independent simulator at `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`. Three opponent profiles: v1, v2 and mixed (8 v1, 7 v2). Each candidate and control uses the same new 24-squad seeds beginning 551231 and 32 independent single-entry free-for-all seeds beginning 661231. Each mean is placement score `16 - place`, **not official** hidden/practice score.

| Opponents | Baseline squad | 200 m FFA-gated squad | Baseline one-hero FFA | 200 m FFA-gated one-hero FFA | FFA Δ |
| --- | ---: | ---: | ---: | ---: | ---: |
| v1 | 0.42 | 0.42 | 8.344 | 8.312 | -0.032 |
| mixed | 0.96 | 0.92 | 7.531 | 7.562 | +0.031 |
| v2 | pending | pending | pending | pending | pending |

Paired placements: v1 0 improved, 1 worsened, 31 unchanged; mixed 4 improved, 4 worsened, 24 unchanged. No meaningful advantage so far. Mixed cooperative placement fell. Preserve `main` and the cleaned submission history; do not promote without confirming the remaining v2 run and strong positive evidence from all profiles.

Benchmark: https://github.com/pucaru/curly-succotash/actions/runs/44892481979
Native/Docker conformance: https://github.com/pucaru/curly-succotash/actions/runs/44892481928

The benchmark overrides TUNE in its environment. Default-configuration Docker conformance is a separate protocol check; it does not certify the unpromoted 200 m policy's official placement.
