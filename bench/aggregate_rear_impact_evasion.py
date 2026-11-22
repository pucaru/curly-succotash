"""Independent paired-seed rear-impact-evasion FFA inference screen audit.

Validates complete 2 x 3 x 2 matrix, one hero in FFA, two policies,
12 new matched seeds per mode/opponent. Proxy results ARE NOT official.
"""
from pathlib import Path
import os
import random
import re
import statistics

ROOT = Path("bench-artifacts")
VALUES = (0, 1)
OPPONENTS = ("v1", "v2", "mixed")
MODES = ("squad", "ffa")
SEEDS = {"squad": 2611201, "ffa": 2612201}
COUNT = 12


def logfile(value, opponent, mode):
    return ROOT / f"rear-impact-evasion-{value}-{opponent}" / f"{mode}-rear-impact-evasion.txt"


def scores(value, opponent, mode):
    path = logfile(value, opponent, mode)
    raw = path.read_text(encoding="utf-8")
    patt = (r"seed (\d+): hero pts \[(\d+)\]" if mode == "squad"
            else r"seed=(\d+) hero_slot=\d+ place=\d+ points=(\d+)")
    matches = re.findall(patt, raw)
    found = {int(seed): int(points) for seed, points in matches}
    expected = set(range(SEEDS[mode], SEEDS[mode] + COUNT))
    if len(matches) != COUNT or set(found) != expected:
        raise ValueError(f"Incomplete, duplicate or unexpected seeds in {path}: {len(matches)} rows")
    if any(not 0 <= pts <= 15 for pts in found.values()):
        raise ValueError(f"Invalid placement in {path}")
    return found


def diagnostics(value, opponent):
    raw = logfile(value, opponent, "ffa").read_text(encoding="utf-8")
    pat = (r"seed=(\d+) hero_slot=\d+ place=\d+ points=\d+ kills=\d+ "
           r"rear_taken=([0-9.]+) stuck_s=([0-9.]+) out_s=([0-9.]+) "
           r"max_act_ms=([0-9.]+)")
    matches = re.findall(pat, raw)
    found = {int(seed): tuple(float(x) for x in row)
             for seed, *row in matches}
    if len(matches) != COUNT or set(found) != set(range(SEEDS["ffa"], SEEDS["ffa"] + COUNT)):
        raise ValueError(f"Missing/duplicate FFA diagnostic: {value}, {opponent}")
    return found



def squad_diagnostics(value, opponent):
    raw = logfile(value, opponent, "squad").read_text(encoding="utf-8")
    hero_lines = re.findall(r"^\s+hero \d+: (.+)$", raw, re.M)
    seeds = re.findall(r"^seed (\d+): hero pts", raw, re.M)
    if len(hero_lines) != COUNT or len(seeds) != COUNT:
        raise ValueError(f"Missing/duplicate squad diagnostics: {value}, {opponent}")
    found = {}
    for seed, line in zip(seeds, hero_lines):
        fields = dict(re.findall(r"(\w+)=([^\s]+)", line))
        death = fields.get("death_t", "None")
        found[int(seed)] = (float(death) if death not in ("None", "null") else 420.0,
                            float(fields.get("rear_taken", 0)),
                            float(fields.get("stuck_s", 0)),
                            float(fields.get("out_s", 0)),
                            float(fields.get("dealt", 0)))
    if set(found) != set(range(SEEDS["squad"], SEEDS["squad"] + COUNT)):
        raise ValueError("Unexpected squad seeds")
    return found

def interval(ds, salt):
    rng = random.Random(88321 + salt)
    n = len(ds)
    res = sorted(statistics.mean(ds[rng.randrange(n)] for _ in range(n))
                 for _ in range(4000))
    return res[99], res[3899]


def report():
    runs = {(v, o, m): scores(v, o, m) for v in VALUES
            for o in OPPONENTS for m in MODES}
    diag = {(v, o): diagnostics(v, o) for v in VALUES for o in OPPONENTS}
    squad_diag = {(v, o): squad_diagnostics(v, o) for v in VALUES for o in OPPONENTS}
    out = [
        "# Rear impact evasion paired screen — independent 144-game screen",
        "",
        "**NOT the official 48-match practice score.** Baseline 0 preserves original rear-impact-evasion toggle.",
        "12 fresh matched seeds per cooperative squad/one-hero FFA cell and opponent profile.",
        "",
        "| Opponents | Control squad | Control FFA | Rear-evade squad | Rear-evade FFA |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for o in OPPONENTS:
        a = [statistics.mean(runs[v, o, m].values()) for v in VALUES for m in MODES]
        out.append("| " + o + " | " + " | ".join(f"{x:.3f}" for x in a) + " |")
    out += [
        "", "## Paired matched-seed gates",
        "Positive placement delta better; negative rear-damage/out-of-zone better.",
        "",
        "| Opp. | Mode | Δ mean [bootstrap 95% CI] W/L/T | Low placements (≤2) control→candidate | FFA rear Δ | FFA out-zone Δ |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    invalid = []
    for k, opp in enumerate(OPPONENTS):
        for mode in MODES:
            base = runs[0, opp, mode]
            alt = runs[1, opp, mode]
            ds = [alt[s] - base[s] for s in sorted(base)]
            mean = statistics.mean(ds)
            lo, hi = interval(ds, 2 * k + (mode == "ffa"))
            wlts = tuple(sum(x > 0 for x in ds) for _ in [0])
            w, l, tie = sum(x > 0 for x in ds), sum(x < 0 for x in ds), sum(x == 0 for x in ds)
            low0 = sum(x <= 2 for x in base.values())
            low1 = sum(x <= 2 for x in alt.values())
            if mean < 0 or low1 > low0:
                invalid.append(f"{opp}/{mode}: mean {mean:+.3f}, low {low0}→{low1}")
            rrear, rout = "—", "—"
            if mode == "ffa":
                keys = sorted(diag[0, opp])
                rear = statistics.mean(diag[1, opp][s][0] - diag[0, opp][s][0] for s in keys)
                zone = statistics.mean(diag[1, opp][s][2] - diag[0, opp][s][2] for s in keys)
                rrear, rout = f"{rear:+.1f}", f"{zone:+.3f}"
                if rear > 0.000001:
                    invalid.append(f"{opp}/ffa: rear damage +{rear:.1f}")
                if zone > 0.000001:
                    invalid.append(f"{opp}/ffa: zone +{zone:.3f}s")
            out.append(f"| {opp} | {mode} | {mean:+.3f} [{lo:+.3f},{hi:+.3f}] {w}/{l}/{tie} | {low0}→{low1} | {rrear} | {rout} |")
    out += ["", "## Squad early death and structural safety", "", 
            "| Opp. | Deaths before 60s control→candidate | Death time avg | Rear dmg avg | Stuck avg | Out zone avg | Damage dealt avg |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for opp in OPPONENTS:
        old, new = squad_diag[0, opp], squad_diag[1, opp]
        keys = sorted(old)
        def fmt(idx, suffix=""):
            return f"{statistics.mean(old[s][idx] for s in keys):.2f}→{statistics.mean(new[s][idx] for s in keys):.2f}{suffix}"
        early = f"{sum(old[s][0]<60 for s in keys)}→{sum(new[s][0]<60 for s in keys)}"
        out.append(f"| {opp} | {early} | {fmt(0,'s')} | {fmt(1)} | {fmt(2,'s')} | {fmt(3,'s')} | {fmt(4)} |")
    maxlat = max(x[3] for d in diag.values() for x in d.values())
    out += [
        "", f"Peak proxy FFA action latency: {maxlat:.2f}ms (not a Docker timing guarantee).",
        "",
        ("**REJECT for promotion.** Gate failures: " + "; ".join(invalid))
        if invalid else ("**Only an exploratory holdout candidate.** No measured screen safety/placement "
                         "regression; require fresh ≥64 FFA and ≥32 squad per opponent, "
                         "endgame review and native+Docker protocol conformance before any production proposal."),
        "",
        "Do not update main or submit an official tournament entry.",
    ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    markdown = report()
    print(markdown)
    Path("rear-impact-evasion-results.md").write_text(markdown, encoding="utf-8")
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(markdown)
