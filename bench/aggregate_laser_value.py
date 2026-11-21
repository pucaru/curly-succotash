"""Audit matched-seed Mech Royale laser-loot-value trials (local simulator only)."""
from pathlib import Path
import os
import re
import statistics

ROOT = Path("bench-artifacts")
VALUES = (180, 300, 420)
OPPONENTS = ("v1", "v2", "mixed")
MODES = ("squad", "ffa")
SQUAD_START = 581121
FFA_START = 681121
COUNT = 24

def read_scores(value, opponent, mode):
    path = ROOT / f"laser-value-{value}-{opponent}" / f"{mode}-laser-value.txt"
    raw = path.read_text(encoding="utf-8")
    pattern = (r"seed (\d+): hero pts \[(\d+)\]" if mode == "squad"
               else r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)")
    pairs = re.findall(pattern, raw)
    scores = {int(seed): int(points) for seed, points in pairs}
    start = SQUAD_START if mode == "squad" else FFA_START
    expected = set(range(start, start + COUNT))
    if len(pairs) != COUNT or set(scores) != expected:
        raise ValueError(f"Missing, duplicated, or wrong seed in {path}: {len(pairs)} records / {len(scores)} unique")
    if any(not (0 <= p <= 15) for p in scores.values()):
        raise ValueError(f"Out-of-range placement points in {path}")
    return scores

def summarize():
    results = {(v, o, m): read_scores(v, o, m)
               for v in VALUES for o in OPPONENTS for m in MODES}
    lines = [
        "# Independent laser-loot priority: paired placement summary", "",
        "Proxy-only simulator results, NOT official scoring. Each cell contains 24 fresh matched seeds.",
        "Baseline 300 uses production behavior; 180 and 420 vary only the loot value.", "",
        "| Opponents | 180 squad | 180 FFA | 300 squad | 300 FFA | 420 squad | 420 FFA |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for opp in OPPONENTS:
        vals = [statistics.mean(results[v, opp, m].values()) for v in VALUES for m in MODES]
        lines.append(f"| {opp} | " + " | ".join(f"{n:.3f}" for n in vals) + " |")
    lines += ["", "## Paired deltas vs 300 (wins/losses/ties; early deaths <= 2)", "",
              "| Variant | Opponents | Squad delta (W/L/T) | FFA delta (W/L/T) | FFA early deaths control => variant |",
              "| --- | --- | ---: | ---: | ---: |"]
    for v in (180, 420):
        regressed = False
        for opp in OPPONENTS:
            by_mode = {}
            for mode in MODES:
                baseline, variant = results[300, opp, mode], results[v, opp, mode]
                differences = [variant[seed] - baseline[seed] for seed in sorted(baseline)]
                delta = statistics.mean(differences)
                by_mode[mode] = f"{delta:+.3f} ({sum(x > 0 for x in differences)}/{sum(x < 0 for x in differences)}/{sum(x == 0 for x in differences)})"
                regressed |= delta < 0
            early_base = sum(p <= 2 for p in results[300, opp, "ffa"].values())
            early_new = sum(p <= 2 for p in results[v, opp, "ffa"].values())
            lines.append(f"| {v} | {opp} | {by_mode['squad']} | {by_mode['ffa']} | {early_base} => {early_new} |")
            if early_new > early_base:
                regressed = True
        if regressed:
            lines.append(f"\n**Value {v}: REJECT provisional promotion.** One or more opponent/mode means or FFA early-death counts regressed.")
        else:
            lines.append(f"\n**Value {v}: holdout candidate only.** Requires new 64-seed FFA and 32-seed cooperative-squad validation, final-circle diagnostics and Docker conformance.")
    lines += ["", "Do not automatically alter main or make official tournament submissions."]
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    report = summarize()
    print(report)
    Path("laser-value-results.md").write_text(report, encoding="utf-8")
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(report)
