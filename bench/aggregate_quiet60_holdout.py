"""Audited 32-squad + 64-FFA holdout per opponent and quiet opening variant.
Independent approximation only; NOT the organizer's official match engine.
"""
from pathlib import Path
import os
import random
import re
import statistics

ROOT = Path("bench-artifacts")
VARIANTS = (0, 60)
OPPONENTS = ("v1", "v2", "mixed")
COUNTS = {"squad": 32, "ffa": 64}
STARTS = {"squad": 1317211, "ffa": 1327211}


def log_path(value, opponent, mode):
    return ROOT / f"quiet60-holdout-{value}-{opponent}" / f"{mode}-quiet60-holdout.txt"


def scores(value, opponent, mode):
    path = log_path(value, opponent, mode)
    raw = path.read_text(encoding="utf-8")
    pattern = (r"seed (\d+): hero pts \[(\d+)\]" if mode == "squad"
               else r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)")
    pairs = re.findall(pattern, raw)
    found = {int(s): int(p) for s, p in pairs}
    expect = set(range(STARTS[mode], STARTS[mode] + COUNTS[mode]))
    if len(pairs) != COUNTS[mode] or set(found) != expect:
        raise ValueError(f"Unpaired, extra, duplicate, or missing seeds in {path}: "
                         f"{len(pairs)} rows, {len(found)} unique")
    if not all(0 <= p <= 15 for p in found.values()):
        raise ValueError(f"Invalid placement points in {path}")
    return found


def diagnostics(value, opponent):
    raw = log_path(value, opponent, "ffa").read_text(encoding="utf-8")
    pat = (r"seed=(\d+) hero_slot=\d+ place=\d+ points=\d+ kills=\d+ "
           r"rear_taken=([0-9.]+) stuck_s=([0-9.]+) out_s=([0-9.]+) "
           r"max_act_ms=([0-9.]+)")
    pairs = re.findall(pat, raw)
    found = {int(seed): tuple(float(q) for q in vals)
             for seed, *vals in pairs}
    if len(pairs) != COUNTS["ffa"] or set(found) != set(
            range(STARTS["ffa"], STARTS["ffa"] + COUNTS["ffa"])):
        raise ValueError(f"FFA diagnostics incomplete: {value} {opponent}")
    return found


def bootstrap_ci(values, group_seed):
    rng = random.Random(group_seed)
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n
                   for _ in range(4000))
    return means[100], means[3900]


def main():
    pts = {(v, o, mode): scores(v, o, mode)
           for v in VARIANTS for o in OPPONENTS
           for mode in COUNTS}
    diag = {(v, o): diagnostics(v, o) for v in VARIANTS for o in OPPONENTS}
    lines = [
        "# Quiet opening 60s — independent fresh-seed holdout", "",
        "576 games; 32 squad and 64 one-hero FFA fresh paired seeds per opponent/variant.",
        "Scores are from a pinned independent approximation, not the official practice scorer.",
        "",
        "| Opponents | Control squad | Control FFA | Quiet-60 squad | Quiet-60 FFA |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    reject = False
    for o in OPPONENTS:
        means = [statistics.mean(pts[v, o, mode].values())
                 for v in VARIANTS for mode in ("squad","ffa")]
        lines.append("| " + o + " | " + " | ".join(f"{x:.3f}" for x in means) + " |")
    lines += ["", "## Paired outcomes and uncertainty", "",
              "Percentile bootstrap 95% CI for the matched-seed *mean* delta (4,000 resamples);",
              "negative rear damage, zone time or early deaths is preferable.",
              "",
              "| Opponents | Mode | Δ mean (95% CI) | W/L/T | Low placement (≤2) | Rear damage Δ | Out-of-zone seconds Δ |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for i, o in enumerate(OPPONENTS):
        for mode in ("squad","ffa"):
            a, b = pts[0, o, mode], pts[60, o, mode]
            d = [b[s]-a[s] for s in sorted(a)]
            mean = statistics.mean(d)
            low, high = bootstrap_ci(d, 84111 + i*2 + int(mode=="ffa"))
            if mean < 0:
                reject = True
            w, l = sum(x>0 for x in d), sum(x<0 for x in d)
            tie = len(d)-w-l
            before = sum(x<=2 for x in a.values())
            after = sum(x<=2 for x in b.values())
            if mode=="ffa":
                if after>before:
                    reject=True
                darr = diag[0,o];dbrr = diag[60,o]
                drear = statistics.mean(dbrr[s][0]-darr[s][0] for s in darr)
                dout = statistics.mean(dbrr[s][2]-darr[s][2] for s in darr)
                if dout>0:
                    reject=True
                detail=f"{drear:+.1f} | {dout:+.2f}"
            else:
                detail="— | —"
            lines.append(
                f"| {o} | {mode} | {mean:+.3f} [{low:+.3f}, {high:+.3f}] | "
                f"{w}/{l}/{tie} | {before} → {after} | {detail} |")
    maxlat=max(row[3] for group in diag.values() for row in group.values())
    lines+=["",f"Peak action latency in this proxy: {maxlat:.2f}ms (not a Docker timing guarantee).",""]
    if reject:
        lines.append("**Holdout failed promotion gates:** at least one group lost mean placement, "
                     "increased early FFA deaths, or spent more time in the zone. "
                     "Preserve original production; no tournament submission.")
    else:
        lines.append("**Holdout passes prespecified directional gates ONLY.** "
                     "Still requires end-circle review, independent validity checks and "
                     "native/Docker conformance on any proposed production revision. "
                     "Do not auto-promote or officially submit.")
    report="\n".join(lines)+"\n"
    print(report)
    Path("quiet60-holdout-results.md").write_text(report,encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
