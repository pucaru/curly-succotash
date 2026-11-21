"""Summarize controlled boost-reserve benchmarks. Never auto-promote game policies."""
from collections import defaultdict
from pathlib import Path
import os
import re
import statistics

ROOT = Path("bench-artifacts")
RESERVES = (18, 30, 42)
OPPONENTS = ("v1", "v2", "mixed")
MODES = ("squad", "ffa")


def read_scores(reserve, opp, mode):
    path = ROOT / f"boost-reserve-{reserve}-{opp}" / f"{mode}-boost-reserve.txt"
    text = path.read_text(encoding="utf-8")
    if mode == "squad":
        pairs = re.findall(r"seed (\d+): hero pts \[(\d+)\]", text)
    else:
        pairs = re.findall(r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)", text)
    scores = {int(seed): int(score) for seed, score in pairs}
    if len(scores) != 24 or len(pairs) != 24:
        raise ValueError(f"Unexpected {mode} records: {path}: {len(pairs)} lines, {len(scores)} unique seeds")
    expected = set(range(371121 if mode == "squad" else 471121,
                         (371121 if mode == "squad" else 471121) + 24))
    if set(scores) != expected:
        raise ValueError(f"Unmatched seeds in {path}")
    return scores


def summarize():
    scores = {(r, o, m): read_scores(r, o, m)
              for r in RESERVES for o in OPPONENTS for m in MODES}
    lines = [
        "# Boost reserve: matched placement results",
        "",
        "Local MIT-simulator proxy scores only; each mean is over 24 matches. "
        "The 30-energy configuration is the unmodified production control.",
        "",
        "| Opponent | 18 squad | 18 FFA | 30 squad | 30 FFA | 42 squad | 42 FFA |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    mean = lambda r, o, m: statistics.mean(scores[r, o, m].values())
    for o in OPPONENTS:
        row = [f"{mean(r,o,m):.3f}" for r in RESERVES for m in MODES]
        lines.append(f"| {o} | " + " | ".join(row) + " |")
    lines.extend(["", "## Paired deltas relative to reserve 30",
                  "", "| Reserve | Opponent | Squad delta (better/worse/ties) | FFA delta (better/worse/ties) |",
                  "| --- | --- | ---: | ---: |"])
    for r in (18, 42):
        all_ffa = []
        squad_regressed = False
        ffa_regressed = False
        for o in OPPONENTS:
            cells = []
            for m in MODES:
                base = scores[30, o, m]
                variant = scores[r, o, m]
                diff = [variant[seed] - base[seed] for seed in sorted(base)]
                avg = statistics.mean(diff)
                cells.append(f"{avg:+.3f} ({sum(x>0 for x in diff)}/{sum(x<0 for x in diff)}/{sum(x==0 for x in diff)})")
                if m == "ffa":
                    all_ffa.extend(diff)
                    ffa_regressed |= avg < 0
                else:
                    squad_regressed |= avg < 0
            lines.append(f"| {r} | {o} | {cells[0]} | {cells[1]} |")
        if squad_regressed or ffa_regressed:
            lines.extend(["", f"**Reserve {r}: REJECT provisional promotion.** "
                          "At least one opponent profile declined in FFA or squad."])
        else:
            lines.extend(["", f"**Reserve {r}: holdout candidate only.** "
                          "Nonnegative means across profiles are not sufficient "
                          "evidence: use new seeds and stress-test late-circle survival."])
    lines.extend(["", "No automatic changes to main or tournament submissions."])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report = summarize()
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(report)
    Path("boost-reserve-results.md").write_text(report, encoding="utf-8")
