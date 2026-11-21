"""Paired placement and safety audit for line-of-sight holding position experiments.

The simulator is an independent approximation, not the official engine.
Require all 9 matrix cells, exact seed sets, and unique per-seed entries.
"""
from pathlib import Path
import os
import re
import statistics

ROOT = Path("bench-artifacts")
VALUES = (0, 55, 125)
OPPONENTS = ("v1", "v2", "mixed")
MODES = ("squad", "ffa")
SQUAD_START = 973911
FFA_START = 983911
COUNT = 24


def logfile(value, opponent, mode):
    return ROOT / f"zone-los-cover-{value}-{opponent}" / f"{mode}-zone-los-cover.txt"


def read_scores(value, opponent, mode):
    path = logfile(value, opponent, mode)
    raw = path.read_text(encoding="utf-8")
    pattern = (r"seed (\d+): hero pts \[(\d+)\]" if mode == "squad"
               else r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)")
    pairs = re.findall(pattern, raw)
    scores = {int(seed): int(pts) for seed, pts in pairs}
    start = SQUAD_START if mode == "squad" else FFA_START
    expected = set(range(start, start + COUNT))
    if len(pairs) != COUNT or set(scores) != expected:
        raise ValueError(
            f"Wrong, duplicate or missing seeds in {path}: {len(pairs)} rows / {len(scores)} unique"
        )
    if any(not 0 <= x <= 15 for x in scores.values()):
        raise ValueError(f"Placement out of range in {path}")
    return scores


def ffa_diagnostics(value, opponent):
    raw = logfile(value, opponent, "ffa").read_text(encoding="utf-8")
    ptn = (r"seed=(\d+) hero_slot=\d+ place=\d+ points=\d+ kills=\d+ "
           r"rear_taken=([0-9.]+) stuck_s=([0-9.]+) out_s=([0-9.]+) "
           r"max_act_ms=([0-9.]+)")
    pairs = re.findall(ptn, raw)
    found = {int(s): tuple(float(x) for x in (rear, stuck, outside, latency))
             for s, rear, stuck, outside, latency in pairs}
    expected = set(range(FFA_START, FFA_START + COUNT))
    if len(pairs) != COUNT or set(found) != expected:
        raise ValueError(f"FFA diagnostic rows incomplete or duplicated: {value} {opponent}")
    return found


def summarize():
    result = {(v, o, m): read_scores(v, o, m)
              for v in VALUES for o in OPPONENTS for m in MODES}
    diag = {(v, o): ffa_diagnostics(v, o)
            for v in VALUES for o in OPPONENTS}
    lines = [
        "# LOS-aware safe-zone hold — independent paired-seed audit", "",
        "Proxy simulator only; scores are not official. Control 0 preserves production behavior.",
        "Three LOS penalty weights, three populations, two modes, 24 fresh matched seeds per cell = 432 matches.",
        "",
        "| Opponents | 0 squad | 0 FFA | 55 squad | 55 FFA | 125 squad | 125 FFA |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for opponent in OPPONENTS:
        vals = [statistics.mean(result[v, opponent, mode].values())
                for v in VALUES for mode in MODES]
        lines.append("| " + opponent + " | " +
                     " | ".join(f"{v:.3f}" for v in vals) + " |")
    lines += [
        "", "## Matched-seed deltas relative to 0",
        "Positive placement delta is better. Negative rear-damage and outside-zone time deltas are better.",
        "",
        "| Variant | Opponents | Squad delta (W/L/T) | FFA delta (W/L/T) | Early FFA deaths (0-2) | FFA rear damage Δ | FFA outside-zone seconds Δ |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for v in (55, 125):
        regressed = False
        for opp in OPPONENTS:
            bymode = {}
            for mode in MODES:
                control, cand = result[0, opp, mode], result[v, opp, mode]
                ds = [cand[s] - control[s] for s in sorted(control)]
                avg = statistics.mean(ds)
                bymode[mode] = (f"{avg:+.3f} "
                                f"({sum(x > 0 for x in ds)}/{sum(x < 0 for x in ds)}/"
                                f"{sum(x == 0 for x in ds)})")
                if avg < 0:
                    regressed = True
            early_control = sum(p <= 2 for p in result[0, opp, "ffa"].values())
            early_cand = sum(p <= 2 for p in result[v, opp, "ffa"].values())
            if early_cand > early_control:
                regressed = True
            drear = statistics.mean(
                diag[v, opp][s][0] - diag[0, opp][s][0]
                for s in diag[v, opp]
            )
            dout = statistics.mean(
                diag[v, opp][s][2] - diag[0, opp][s][2]
                for s in diag[v, opp]
            )
            if dout > 0:
                regressed = True
            lines.append(
                f"| {v} | {opp} | {bymode['squad']} | {bymode['ffa']} | "
                f"{early_control} → {early_cand} | {drear:+.1f} | {dout:+.2f} |"
            )
        if regressed:
            lines.append(f"\n**{v} rejected for promotion:** at least one population/mode mean, "
                         "FFA early-death count or mean outside-zone time regressed.")
        else:
            lines.append(f"\n**{v} holdout candidate only:** needs a new larger matched-seed "
                         "sample, final-circle inspection, conformance and runtime checks.")
    maxlat = max(row[3] for group in diag.values() for row in group.values())
    lines += ["", f"Peak observed FFA action time in simulator: {maxlat:.2f} ms. "
              "Simulator timing is not a substitute for the official 50ms conformance check.",
              "Do not alter main or submit an official tournament entry automatically."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report = summarize()
    print(report)
    Path("zone-los-cover-results.md").write_text(report, encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as dest:
            dest.write(report)
