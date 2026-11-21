# Quiet 60-second opening — independent fresh-seed robustness holdout (21 November 2026)

**Status:** launched. No verified production improvement or official practice result yet.
Parent experiment commit: `5711d871c51034777048d324f88f19ab36fb5676` (`quiet_farm_until` defaults 0 so production behavior is preserved). Separate branch with *no* change to the bot logic. The selected candidate is `MECH_TUNE.quiet_farm_until=60`.

## Why additional testing rather than promotion
The 12-seed first screen ([run 44912563320](https://github.com/pucaru/curly-succotash/actions/runs/44912563320)) found positive FFA deltas in v1 (+0.333), v2 (+1.000) and mixed (+1.167). However v1 squad fell -0.333, and v2 FFA out-of-zone time rose 0.34s. These are small, noisy samples (v1 squad only 1 win/2 losses/9 ties) that did **not** pass promotion gates. Repeating the same seeds would be invalid; the independent holdout investigates whether apparent gains and risks persist.

## Preregistered holdout
Pinned independent MIT proxy engine `VivekRnx/bob-the-builder-2026@b76c216d8a7829e14409a42058eea93e46e9ccdb`.
Six cells: `quiet_farm_until=0 vs 60` × v1/v2/mixed opponents. Each 32 **new** squad seeds 1317211–1317242 and 64 **new** single-hero FFA seeds 1327211–1327274. Exactly **576** games. One test bot in FFA against varied independent opponents, 15 coordinated practice proxy bots in squad. As with all tests, this approximation is not the official scorer, and it simplifies sound-driven hunting.

The aggregator fails on missing/duplicate/wrong seed coverage, computes matched W/L/T, 4,000-resample paired bootstrap 95% confidence intervals, early deaths, rear damage, outside-zone exposure, and action latency. Reject on negative group mean, increased FFA early deaths or zone exposure. A passing holdout is *not* authorization to modify `main`: end-circle audit, actual conformance on candidate's production-default values and user approval of any official submission remain required.

Do not resurrect the removed public-research material, record competitor code or rewrite submitted history.
