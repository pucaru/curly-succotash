"""One-entry free-for-all benchmark using the independent Mech Royale simulator.

Run from its root after copying this file into its tools/ directory.
Unlike the simulator's built-in FFA, this puts only ONE tested bot in
each lobby, alongside fifteen opponents that all fight each other.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import random
import statistics

import sim


def one_match(job):
    seed, opponent_specs = job
    hello = sim.load_hello()
    hero_type = sim.import_bot("survivor_adapter")
    opponent_types = [sim.import_bot(name) for name in opponent_specs]
    rng = random.Random(seed)
    hero_slot = rng.randrange(16)
    opponents = [opponent_types[i % len(opponent_types)] for i in range(15)]
    rng.shuffle(opponents)
    bots = opponents[:]
    bots.insert(hero_slot, hero_type)
    assert len(bots) == 16 and bots[hero_slot] is hero_type
    match = sim.Sim(hello, bots, [None] * 16, seed)
    result = match.run(verbose=True)
    mine = match.mechs[hero_slot]
    assert mine.place is not None, "Hero missing final placement"
    assert len(result) == 16, "Incomplete match"
    return {
        "seed": seed, "slot": hero_slot, "place": mine.place,
        "points": 16 - mine.place, "kills": mine.kills,
        "max_ms": max(mine.act_ms, default=0),
        "diag": mine.diag,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("-n", type=int, default=24)
    ap.add_argument("-j", type=int, default=4)
    ap.add_argument("--opp", required=True,
                    help="Comma-separated independent simulator opponent modules")
    args = ap.parse_args()
    opponent_specs = tuple(s.strip() for s in args.opp.split(",") if s.strip())
    if not opponent_specs or args.n < 1:
        ap.error("Specify at least one opponent and a positive match count")
    jobs = [(args.seed + i, opponent_specs) for i in range(args.n)]
    if args.j == 1:
        results = [one_match(job) for job in jobs]
    else:
        with ProcessPoolExecutor(max_workers=args.j) as pool:
            results = list(pool.map(one_match, jobs))
    results.sort(key=lambda r: r["seed"])
    for entry in results:
        diag = entry["diag"]
        print("seed=%d hero_slot=%d place=%d points=%d kills=%d rear_taken=%.1f "
              "stuck_s=%.1f out_s=%.1f max_act_ms=%.2f" % (
                  entry["seed"], entry["slot"], entry["place"], entry["points"],
                  entry["kills"], diag.get("rear_taken", 0.0),
                  diag.get("stuck_s", 0.0), diag.get("out_s", 0.0),
                  entry["max_ms"]), flush=True)
    pts = [entry["points"] for entry in results]
    rear = [entry["diag"].get("rear_taken", 0.0) for entry in results]
    print("one-hero FFA: mean pts %.3f, median pts %.1f, "
          "mean rear_taken %.1f, worst pts %d, n=%d" % (
              statistics.mean(pts), statistics.median(pts), statistics.mean(rear),
              min(pts), len(pts)), flush=True)


if __name__ == "__main__":
    main()
