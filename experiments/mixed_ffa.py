"""One candidate versus fifteen distinct opponent instances in FFA.

An independent local approximation, not the official scoring engine.
Uses only published simulator interfaces; no competitor strategy is copied.
"""
import argparse
import concurrent.futures
import random
import statistics
from tools.sim import Sim, load_hello, import_bot


def play(job):
    seed, mix = job
    rng = random.Random(seed ^ 0x23B87C9D)
    hero_slot = rng.randrange(16)
    if mix == "balanced":
        opponents = ["tools.baseline.brain_v1"] * 7 + ["tools.baseline.brain_v2"] * 8
    elif mix == "strong":
        opponents = ["tools.baseline.brain_v1"] * 3 + ["tools.baseline.brain_v2"] * 12
    else:
        raise ValueError("unknown opponent composition")
    rng.shuffle(opponents)
    next_opponent = iter(opponents)
    bots = [import_bot("survivor_adapter") if i == hero_slot else
            import_bot(next(next_opponent)) for i in range(16)]
    sim = Sim(load_hello(), bots, [None] * 16, seed)
    placements = sim.run()
    hero = next(m for m in sim.mechs if m.id == hero_slot)
    place = next(place for mid, place, *_ in placements if mid == hero_slot)
    return dict(seed=seed, slot=hero_slot, points=16 - place, place=place,
                kills=hero.kills, death=hero.diag.get("death_by"),
                zone_damage=hero.diag.get("zone_dmg", 0),
                max_ms=max(hero.act_ms or [0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mix", choices=["balanced", "strong"], required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("-n", type=int, default=16)
    parser.add_argument("-j", type=int, default=4)
    args = parser.parse_args()
    jobs = [(args.seed + i, args.mix) for i in range(args.n)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.j) as pool:
        data = list(pool.map(play, jobs))
    pts = [x["points"] for x in data]
    for d in sorted(data, key=lambda x: x["seed"]):
        print(f'seed {d["seed"]}: slot={d["slot"]} place={d["place"]} '
              f'points={d["points"]} kills={d["kills"]} '
              f'death={d["death"]} zone_damage={d["zone_damage"]:.1f} '
              f'max_act_ms={d["max_ms"]:.2f}', flush=True)
    print(f'MIXED_FFA mix={args.mix} n={len(data)} mean={statistics.mean(pts):.4f} '
          f'median={statistics.median(pts):.2f} '
          f'bottom4={sum(p <= 3 for p in pts)} top4={sum(p >= 12 for p in pts)} '
          f'min={min(pts)} max={max(pts)}', flush=True)


if __name__ == "__main__":
    main()
