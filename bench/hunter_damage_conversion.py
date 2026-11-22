"""Diagnostic-only, original instrumentation. Not a gameplay change or scorer."""
import argparse
from collections import Counter, defaultdict
import json
import statistics
import tools.sim as sim
from bot import Bot as Base

class Brain(Base):
    def __init__(self, hello):
        super().__init__(hello)
        self.hit_by_target = defaultdict(float)
        self.hit_by_weapon = defaultdict(float)
        self.hit_count = Counter()
        self.mode_counts = Counter()
        self.target_switches = 0
        self.targeted = Counter()
        self.stale_target_ticks = 0
        self.rear_hits = Counter()
        self.damage_taken = Counter()
        self.previous_target = None
        self.active_target_count = 0

    def enemy(self, obs, threats):
        target = super().enemy(obs, threats)
        tid = target["id"] if target else None
        if tid != self.previous_target and tid is not None and self.previous_target is not None:
            self.target_switches += 1
        self.previous_target = tid
        if target:
            self.active_target_count += 1
            self.targeted[str(tid)] += 1
            if obs["t"] - target["seen"] > 1.0:
                self.stale_target_ticks += 1
        return target

    def choose_goal(self, obs, threats, target):
        result = super().choose_goal(obs, threats, target)
        self.mode_counts[result[1]] += 1
        return result

    def act(self, obs):
        for ev in obs.get("events", []):
            if ev.get("type") == "hit":
                who = str(ev.get("target"))
                amt = float(ev.get("amount", 0))
                self.hit_by_target[who] += amt
                self.hit_by_weapon[ev.get("weapon", "unknown")] += amt
                self.hit_count[who] += 1
            elif ev.get("type") == "damaged":
                w = ev.get("weapon", "unknown")
                self.damage_taken[w] += float(ev.get("amount", 0))
                if ev.get("rear"):
                    self.rear_hits[w] += 1
        return super().act(obs)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--opp", required=True)
    p.add_argument("--seed", type=int, default=3672001)
    p.add_argument("-n", type=int, default=6)
    args = p.parse_args()
    outcomes = []
    for seed in range(args.seed, args.seed + args.n):
        match, hero_ids = sim.setup_match(seed, "squad", "diagnostic_adapter", args.opp)
        match.run()
        hero = match.mechs[hero_ids[0]]
        data = hero.bot
        actors = {k: v for k,v in data.hit_by_target.items() if int(k) in range(16)}
        total = sum(actors.values())
        peak = max(actors.values(), default=0)
        nonactors = sum(v for k,v in data.hit_by_target.items() if int(k) not in range(16))
        result = {
          "seed": seed, "pts": 16-hero.place, "kills": hero.kills,
          "death_t": hero.diag.get("death_t"), "rear_taken": hero.diag.get("rear_taken",0),
          "dealt": round(hero.diag.get("dealt",0),1),
          "mech_hit_damage": round(total,1), "object_hit_damage": round(nonactors,1),
          "unique_mech_targets_hit": len(actors), "top_target_damage": round(peak,1),
          "focus_fraction": round(peak/total,3) if total else 0,
          "switches": data.target_switches, "active_target_ticks": data.active_target_count,
          "stale_target_ticks": data.stale_target_ticks,
          "mode_counts": dict(data.mode_counts),
          "damage_taken": dict(data.damage_taken), "rear_hit_events": dict(data.rear_hits),
          "weapon_damage": dict(data.hit_by_weapon),
          "top_targets": sorted(((k,round(v,1)) for k,v in actors.items()),key=lambda q:-q[1])[:4],
          "final_weapon": [x.kind if x else None for x in hero.weapons],
        }
        print("DIAG "+json.dumps(result,sort_keys=True),flush=True)
        outcomes.append(result)
    print("SUMMARY "+json.dumps({
      "games": len(outcomes), "mean_points":statistics.mean(r["pts"] for r in outcomes),
      "mean_kills":statistics.mean(r["kills"] for r in outcomes),
      "mean_mech_damage":statistics.mean(r["mech_hit_damage"] for r in outcomes),
      "mean_damage_focus_fraction":statistics.mean(r["focus_fraction"] for r in outcomes),
      "mean_target_switches":statistics.mean(r["switches"] for r in outcomes),
      "mean_stale_target_pct":statistics.mean(r["stale_target_ticks"]/max(1,r["active_target_ticks"]) for r in outcomes),
      "mean_rear_taken":statistics.mean(r["rear_taken"] for r in outcomes),
    },sort_keys=True),flush=True)

if __name__ == "__main__":
    main()
