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

## Partial holdout audit (21 November, 22:31 SGT)

Four fully completed matrix cells (`0/60 × v1/mixed`) were independently extracted from the GitHub Actions logs using exact paired seed sets: 32 squad and 64 single-entrant FFA seeds in each cell. **This candidate already fails the preregistered safety/placement gate, even before the slower v2 jobs finish.** Treat the 60-second suppression as rejected for production; do not cherry-pick the mixed-population improvement.

| Opponents | Squad paired Δ (W/L/T) | FFA 0→60 mean | FFA paired Δ (W/L/T) | Early FFA ≤2 points | FFA rear damage Δ | FFA out-of-zone Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 | +0.125 (5/1/26) | 7.484→7.313 | **−0.172** (8/13/43) | **5→7** | −49.9 | −0.006 s |
| mixed | +0.156 (7/3/22) | 6.234→6.797 | +0.563 (16/10/38) | 11→8 | −147.3 | **+0.181 s** |

Paired 4,000-resample percentile bootstrap 95% mean-delta confidence intervals: v1 squad [+0.000,+0.281], v1 FFA [−0.703,+0.344], mixed squad [−0.063,+0.375], mixed FFA [−0.063,+1.266]. Intervals include zero in most groups; no evidence of a reliable FFA gain. The v1 FFA mean and early-death count fail the directional gate, while mixed zone exposure increases. Results are from the independent approximation, not the official 48-match scorer. Do not alter production. The remaining v2 cells are still running; once finished, verify the full aggregate, bootstrap confidence intervals, and record final outcomes. The larger holdout reverses the earlier small-screen v1 FFA gain (+0.333), demonstrating the screening instability. No official submission.

## Final 576-game holdout (21 November 2026, completed)
**Completed CI:** [holdout run 44913277052](https://github.com/pucaru/curly-succotash/actions/runs/44913277052), all six compare cells and aggregate **success**. [Native 300-observation + Docker conformance 44913276997](https://github.com/pucaru/curly-succotash/actions/runs/44913276997) **success**. The CI aggregate independently checked all six matched cells (32 squad and 64 one-hero FFA seeds each) with 4,000-resample paired bootstrap CIs.

| Opponents | Squad 0→60 | FFA 0→60 | Squad Δ (95% CI; W/L/T) | FFA Δ (95% CI; W/L/T) | FFA low placements ≤2 | Rear damage Δ | Outside-zone time Δ |
| --- | ---: | ---: | --- | --- | ---: | ---: | ---: |
| v1 | 0.219→0.344 | 7.484→7.312 | +0.125 [+0.000,+0.281]; 5/1/26 | **−0.172 [−0.703,+0.359]**; 8/13/43 | **5→7** | −49.9 | −0.01s |
| v2 | 0.094→0.094 | 5.578→5.250 | +0.000 [−0.125,+0.156]; 1/2/29 | **−0.328 [−1.141,+0.500]**; 20/20/24 | **15→17** | −56.7 | **+0.23s** |
| mixed | 0.562→0.719 | 6.234→6.797 | +0.156 [−0.062,+0.375]; 7/3/22 | +0.562 [−0.047,+1.250]; 16/10/38 | 11→8 | −147.3 | **+0.18s** |

CI output archived in [quiet60-holdout-summary artifact](https://github.com/pucaru/curly-succotash/actions/runs/44913277052/artifacts/14710923996). Observed peak action latency 8.21ms in the approximation; no claim about private match execution time.

**Final decision: REJECT.** The v1/v2 FFA placement losses, increased v1/v2 early low placements, and increased v2/mixed zone exposure each violate independent preregistered safety gates. The mixed FFA uplift is insufficient and not statistically established at the paired 95% level; do not select by population after looking at outcomes. Preserve main 60b5438, leave official practice score unknown, and do not re-run this unchanged mechanism.
