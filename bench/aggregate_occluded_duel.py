"""Strict paired-seed audit for wall-occluded duel-lane experiment.

The independent third-party simulator is a non-authoritative approximation.
Reject a variant if ANY subgroup placement, low-finish, rear or zone gate fails.
"""
from pathlib import Path
import os
import random
import re
import statistics

ROOT = Path("bench-artifacts")
VALUES = (0, 1, 2)
OPPONENTS = ("v1", "v2", "mixed")
MODES = ("squad", "ffa")
SEEDS = {"squad": 1810211, "ffa": 1820211}
COUNT = 12


def logfile(value, opponent, mode):
    return ROOT / f"occluded-duel-{value}-{opponent}" / f"{mode}-occluded-duel.txt"


def scores(value, opponent, mode):
    path = logfile(value, opponent, mode)
    raw = path.read_text(encoding="utf-8")
    pattern = (r"seed (\d+): hero pts \[(\d+)\]" if mode == "squad"
               else r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)")
    matches = re.findall(pattern, raw)
    found = {int(seed): int(pts) for seed, pts in matches}
    expected = set(range(SEEDS[mode], SEEDS[mode] + COUNT))
    if len(matches) != COUNT or set(found) != expected:
        raise ValueError(f"Missing/duplicate scores in {path}: {len(matches)}")
    if any(not 0 <= p <= 15 for p in found.values()):
        raise ValueError(f"Invalid points in {path}")
    return found


def diagnostics(value, opponent):
    raw = logfile(value, opponent, "ffa").read_text(encoding="utf-8")
    pat = (r"seed=(\d+) hero_slot=\d+ place=\d+ points=\d+ kills=\d+ "
           r"rear_taken=([0-9.]+) stuck_s=([0-9.]+) out_s=([0-9.]+) "
           r"max_act_ms=([0-9.]+)")
    matches = re.findall(pat, raw)
    found = {int(seed): tuple(float(x) for x in row)
             for seed, *row in matches}
    if len(matches) != COUNT or set(found) != set(
            range(SEEDS["ffa"], SEEDS["ffa"] + COUNT)):
        raise ValueError(f"Missing/duplicate FFA diagnostics: {value}, {opponent}")
    return found


def interval(deltas, salt):
    rng = random.Random(98121 + salt)
    n = len(deltas)
    res = sorted(statistics.mean(deltas[rng.randrange(n)] for _ in range(n))
                 for _ in range(4000))
    return res[99], res[3899]


def report():
    scoreset = {(v, o, m): scores(v, o, m) for v in VALUES
                for o in OPPONENTS for m in MODES}
    diag = {(v, o): diagnostics(v, o) for v in VALUES for o in OPPONENTS}
    out = [
        "# Wall-occluded duel lane — 216 independent simulated matches",
        "",
        "**NOT the organizer's official 48-game practice score.**",
        "Fixed baseline 60b5438, 12 fresh matched seeds per scenario.",
        "Policy 0: unchanged baseline; 1: seek exposed safe firing lane or disengage;",
        "2: seek lane, otherwise route toward enemy if >68m away.",
        "",
        "| Opponent | Mode | 0: control | 1: lane/hold | 2: lane/route |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for o in OPPONENTS:
        for mode in MODES:
            values = [statistics.mean(scoreset[v, o, mode].values())
                      for v in VALUES]
            out.append(f"| {o} | {mode} | " +
                       " | ".join(f"{x:.3f}" for x in values) + " |")
    out += [
        "", "## Prespecified paired directional gates",
        "",
        "A variant fails if ANY population/mode has negative mean placement,",
        "more early low finishes (points <=2), more FFA rear damage, or",
        "more FFA zone time. CIs are paired bootstrap, not proof of superiority.",
        "",
        "| Variant | Opp. | Mode | Delta [95% CI] W/L/T | low control→candidate | FFA rear delta | FFA out-zone delta |",
        "| --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    failures = {1: [], 2: []}
    for v in (1, 2):
        for oi, opponent in enumerate(OPPONENTS):
            for mi, mode in enumerate(MODES):
                old = scoreset[0, opponent, mode]
                new = scoreset[v, opponent, mode]
                ds = [new[s] - old[s] for s in sorted(old)]
                mean = statistics.mean(ds)
                lo, hi = interval(ds, v * 100 + oi * 10 + mi)
                wins = sum(x > 0 for x in ds)
                losses = sum(x < 0 for x in ds)
                ties = len(ds) - wins - losses
                low0 = sum(p <= 2 for p in old.values())
                low1 = sum(p <= 2 for p in new.values())
                if mean < 0 or low1 > low0:
                    failures[v].append(
                        f"{opponent}/{mode} placement={mean:+.3f}, low={low0}→{low1}")
                rd, zd = "—", "—"
                if mode == "ffa":
                    d0, d1 = diag[0, opponent], diag[v, opponent]
                    rd_mean = statistics.mean(d1[s][0] - d0[s][0] for s in d0)
                    zd_mean = statistics.mean(d1[s][2] - d0[s][2] for s in d0)
                    rd, zd = f"{rd_mean:+.1f}", f"{zd_mean:+.3f}"
                    if rd_mean > 0.000001:
                        failures[v].append(f"{opponent}/ffa rear={rd_mean:+.1f}")
                    if zd_mean > 0.000001:
                        failures[v].append(f"{opponent}/ffa zone={zd_mean:+.3f}")
                out.append(
                    f"| {v} | {opponent} | {mode} | {mean:+.3f} "
                    f"[{lo:+.3f},{hi:+.3f}] {wins}/{losses}/{ties} "
                    f"| {low0}→{low1} | {rd} | {zd} |")
    peak_ms = max(x[3] for diagnostics in diag.values() for x in diagnostics.values())
    out.extend(["", f"Peak proxy action latency: {peak_ms:.2f} ms.", ""])
    for v in (1, 2):
        if failures[v]:
            out.append(f"**Variant {v}: REJECT.** " + "; ".join(failures[v]))
        else:
            out.append(
                f"**Variant {v}: SCREEN ONLY.** No observed directional regression. "
                "Requires independent 64 FFA + 32 squad fresh matched seeds "
                "per opponent and native/Docker conformance plus endgame audit "
                "before production consideration.")
        out.append("")
    out.append("Production main untouched; no official tournament action.")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    result = report()
    print(result)
    Path("occluded-duel-results.md").write_text(result, encoding="utf-8")
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(result)
