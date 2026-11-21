"""Placement-oriented Mech Royale bot. Uses only the official protocol and Python stdlib."""
import math
import random
import json
import os

import mechfight as mf
from arena import Arena, Navigator

TAU = 2.0 * math.pi
RANK = {"gun": 0, "mortar": 1, "lightning": 2, "laser": 3}
UPGRADES = ("plating", "armor", "nanites", "laser_damage", "gun_rate",
            "gun_damage", "laser_charge", "gyros", "gun_velocity",
            "lightning_efficiency", "mortar_reload", "servos", "reactor",
            "capacitor", "gun_mag", "sensors", "jets")
DEFENSE_RADIUS = 180.0
# Tunable constants allow reproducible A/B runs in the local simulator.
# Production uses the defaults; no network or model inference is required.
TUNE = {
    "focus": 120.0,
    "attacker": 180.0,
    "finish": 110.0,
    "cover_hp": 0.47,
    "hurt_cover_hp": 0.75,
    "duel_range": 140.0,
    "duel_hp": 0.44,
    "avoid_range": 145.0,
    "laser_value": 300.0,
    "laser_search_radius": 270.0,
    "lightning_spacing": 0,
}
try:
    TUNE.update(json.loads(os.environ.get("MECH_TUNE", "{}") or "{}"))
except (TypeError, ValueError):
    pass


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def unit(dx, dy):
    h = math.hypot(dx, dy)
    return (dx / h, dy / h) if h > 1e-6 else (0.0, 0.0)


def wrap(a):
    return (a + math.pi) % TAU - math.pi


def clamp(a, lo, hi):
    return max(lo, min(hi, a))


def face(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


def lerp(a, b, f):
    return a + (b - a) * f


class Bot:
    name = "curly-survivor"

    def __init__(self, hello):
        self.cfg = hello["config"]
        self.slot = hello["slot"]
        self.rng = random.Random(hello.get("seed", 0))
        self.map = None
        self.nav = None
        try:
            self.map = Arena(hello["map"]["dir"])
            self.nav = Navigator(self.map)
        except Exception as exc:
            mf.log("navigation map unavailable:", repr(exc))
        self.tracks = {}
        self.loot = {}
        self.cube_memory = {}
        self.crate_memory = {}
        self.bad_pickups = {}
        self.last_hit = -100.0
        self.last_shot = -100.0
        self.last_bearing = None
        self.attacker = None
        self.attacker_until = -100.0
        self.last_visible_mech = -100.0
        self.prev_alive = int(self.cfg.get("match", {}).get("mechs", 16))
        self.kills = 0
        self.other_deaths = 0
        self.ffa = False
        self.last_time = 0.0
        self.strafe_dir = 1
        self.strafe_until = 0.0
        self.prev_pos = None
        self.stuck = 0
        self.unstuck_until = -100.0
        self.unstuck_yaw = 0.0
        self.hold = None
        self.hold_until = -100.0
        self.cover = None
        self.cover_until = -100.0
        self.last_enemy_id = None
        self.last_danger = 0.0
        self.target_last = -100.0
        self.scout_goal = None
        self.scout_until = -100.0
        self.explored = set()
        self.sound_contacts = []
        self.last_sound_yaw = None
        self.last_sound_time = -100.0
        self.last_sound_kind = None

    def update(self, obs):
        t = obs["t"]
        me = obs["self"]
        own_pos = me["pos"]
        kills_now = 0
        for ev in obs.get("events", []):
            typ = ev.get("type")
            if typ == "damaged":
                self.last_hit = t
                if ev.get("bearing") is not None:
                    self.last_bearing = ev["bearing"]
                if ev.get("by") is not None:
                    self.attacker = ev["by"]
                    self.attacker_until = t + 9.0
            elif typ == "hit":
                self.last_shot = t
            elif typ == "kill":
                kills_now += 1
            elif typ in ("took", "take_failed"):
                self.loot.pop(ev.get("id"), None)
                if typ == "take_failed" and ev.get("reason") in ("gone", "have"):
                    self.bad_pickups[ev.get("id")] = t + 20
        self.kills += kills_now
        dropped = max(0, self.prev_alive - int(obs.get("alive", self.prev_alive)))
        self.other_deaths += max(0, dropped - kills_now)
        self.prev_alive = int(obs.get("alive", self.prev_alive))
        if ((t < 50 and self.other_deaths >= 1) or
                (t >= 50 and self.other_deaths >= 2)):
            self.ffa = True
        for ent in obs.get("mechs", []):
            if ent.get("kind") != "mech":
                continue
            ident = ent["id"]
            self.tracks[ident] = {
                "id": ident, "pos": ent["pos"], "vel": ent.get("vel", (0, 0, 0)),
                "aim": ent.get("aim", (0, 0)), "hp": ent.get("hp", 1400),
                "max_hp": ent.get("max_hp", 1400),
                "cubes": ent.get("cubes", 0),
                "weapons": ent.get("weapons", []),
                "charging": ent.get("charging", False), "seen": t,
            }
            self.last_visible_mech = t
        for ident, tr in list(self.tracks.items()):
            if t - tr["seen"] > 13.0:
                del self.tracks[ident]
        for item, kind in ((obs.get("pickups", []), "weapon"),
                           (obs.get("cubes", []), "cube"),
                           (obs.get("crates", []), "crate")):
            dst = {"weapon": self.loot, "cube": self.cube_memory,
                   "crate": self.crate_memory}[kind]
            for p in item:
                dst[p["id"]] = (p, t)
        for dst, ttl in ((self.loot, 55), (self.cube_memory, 13),
                         (self.crate_memory, 18)):
            for ident, (p, seen) in list(dst.items()):
                if t - seen > ttl or (
                        t - seen > 1.4 and
                        distance(own_pos, p["pos"]) < 8):
                    del dst[ident]
        for ident, until in list(self.bad_pickups.items()):
            if until < t:
                del self.bad_pickups[ident]
        self.explored.add((round(own_pos[0] / 25), round(own_pos[1] / 25)))
        self.sound_contacts = [q for q in self.sound_contacts if t - q["seen"] < 4.0]
        for heard in obs.get("sounds", []):
            kind = heard.get("kind", "")
            if kind not in ("gun", "mortar", "laser", "laser_charge",
                            "lightning", "step", "boost", "jet"):
                continue
            age = heard.get("age", 0.0)
            if age > 1.2:
                continue
            bearing = heard.get("bearing", 0.0)
            band = heard.get("dist", "mid")
            radius = {"near": 43, "mid": 112, "far": 212}.get(band, 115)
            px = own_pos[0] + radius * math.cos(bearing)
            py = own_pos[1] + radius * math.sin(bearing)
            self.sound_contacts.append({"pos": (px, py),
                                        "seen": t - age, "bearing": bearing,
                                        "kind": kind, "band": band})
            if (t - age >= self.last_sound_time and
                    kind in ("gun", "mortar", "laser", "laser_charge", "lightning")):
                self.last_sound_yaw = bearing
                self.last_sound_time = t - age
                self.last_sound_kind = kind
        self.sound_contacts = self.sound_contacts[-18:]
        self.last_time = t

    def threats(self, pos, t, radius=220):
        arr = []
        for tr in self.tracks.values():
            age = t - tr["seen"]
            dist = distance(pos, tr["pos"])
            if dist < radius and age <= 9:
                arr.append((tr, dist, age))
        arr.sort(key=lambda x: x[1])
        return arr

    def enemy(self, obs, threats):
        t, me = obs["t"], obs["self"]
        hpfrac = me["hp"] / max(1, me["max_hp"])
        candidates = []
        for tr, d, age in threats:
            if age > 5.2 or d > 190:
                continue
            hpfrac_enemy = tr["hp"] / max(1, tr["max_hp"])
            actively_hit = tr["id"] == self.attacker and t < self.attacker_until
            if self.ffa and not actively_hit and d > 62 and hpfrac_enemy > 0.32:
                continue
            # In practice the house squad does not fight itself, so removing an attacker matters.
            score = d * 0.42 + tr["hp"] * 0.045 + age * 16
            if actively_hit:
                score -= TUNE["attacker"]
            if tr["id"] == self.last_enemy_id and age < 1.75:
                score -= TUNE["focus"]
            if hpfrac_enemy < 0.46:
                score -= TUNE["finish"] * (1.0 - hpfrac_enemy)
            if hpfrac < 0.3 and not actively_hit and d > 30:
                score += 140
            candidates.append((score, tr, d))
        if not candidates:
            return None
        _, tr, d = min(candidates, key=lambda c: c[0])
        self.last_enemy_id = tr["id"]
        self.target_last = t
        return tr

    def zone_target(self, obs):
        z = obs["zone"]
        p = obs["self"]["pos"]
        t = obs["t"]
        xc, yc = z["next_center"]
        r = z["next_radius"]
        # The final phase's radius approaches zero, so track the moving centre tightly.
        if r <= 35:
            return (xc, yc)
        if self.hold is not None and t < self.hold_until:
            if distance(self.hold, (xc, yc)) < r * 0.72:
                return self.hold
        # Sample a ring of reachable sites instead of always walking into the same centre.
        radius = min(r * 0.52, 88.0)
        best, bestscore = (xc, yc), float("-inf")
        candidates = [(xc, yc)]
        for dist in (radius, radius * 0.55):
            for i in range(16):
                a = TAU * i / 16
                candidates.append((xc + dist * math.cos(a),
                                   yc + dist * math.sin(a)))
        dangers = self.threats(p, t, 330)
        for point in candidates:
            if self.map is not None and not self.map.free(*point):
                continue
            travel = distance(p, point)
            score = -travel * 0.30
            score -= abs(distance(point, (xc, yc)) - radius) * 0.045
            if self.map is not None:
                # Simple cover proxy: nearby barriers shield at least one direction.
                hidden = 0
                for j in range(8):
                    a = j * TAU / 8
                    if not self.map.free(point[0] + math.cos(a) * 8,
                                         point[1] + math.sin(a) * 8):
                        hidden += 1
                score += hidden * 11.0
            for tr, d, age in dangers:
                pd = distance(tr["pos"], point)
                if pd < 160:
                    score -= (160 - pd) * (0.30 if not self.ffa else 0.75)
            if score > bestscore:
                bestscore = score
                best = point
        self.hold = best
        self.hold_until = t + 4.0
        return best

    def safety(self, obs, point, margin=9):
        z = obs["zone"]
        p = obs["self"]["pos"]
        t = obs["t"]
        cur = z["center"]
        if distance(point, cur) > z["radius"] - margin:
            return False
        speed = max(7.5, obs["self"].get("stats", {}).get("walk_speed", 13.0))
        travel = distance(p, point) / speed * 1.5
        if t + travel + 8 >= z["shrink_end"]:
            if distance(point, z["next_center"]) > max(2, z["next_radius"] - margin):
                return False
        return True

    def find_cover(self, obs, threats):
        me, t = obs["self"], obs["t"]
        if self.map is None or not threats:
            return None
        pos = me["pos"]
        if (self.cover is not None and t < self.cover_until and
                self.safety(obs, self.cover)):
            return self.cover
        best = None
        bestcost = float("inf")
        # Prefer cover close enough to reach before another laser volley.
        for radius in (8, 16, 25, 37):
            for i in range(16):
                a = i * TAU / 16
                px, py = pos[0] + radius * math.cos(a), pos[1] + radius * math.sin(a)
                if not self.map.free(px, py) or not self.safety(obs, (px, py), 5):
                    continue
                if not self.map.clear(pos[0], pos[1], px, py):
                    continue
                danger, covered = 0.0, 0
                for tr, _, age in threats[:4]:
                    if age > 6:
                        continue
                    dist = math.hypot(tr["pos"][0] - px, tr["pos"][1] - py)
                    exposed = self.map.clear(tr["pos"][0], tr["pos"][1], px, py,
                                             inflated=False)
                    if exposed:
                        danger += max(0, 160 - dist) * 0.65 + 45
                    else:
                        covered += 1
                    if dist < 20:
                        danger += (20 - dist) * 4
                cost = radius * 1.1 + danger - covered * 19
                if cost < bestcost:
                    bestcost, best = cost, (px, py)
        if best is not None:
            self.cover = best
            self.cover_until = t + 0.75
        return best

    def choose_goal(self, obs, threats, target):
        me, z, t = obs["self"], obs["zone"], obs["t"]
        p = me["pos"]
        hp = me["hp"] / max(1.0, me["max_hp"])
        nearest = threats[0][1] if threats else 9999
        close = sum(1 for _, d, a in threats if d < 100 and a < 3)
        center = self.zone_target(obs)
        dcur = distance(p, z["center"])
        dnext = distance(p, z["next_center"])
        rnext = z["next_radius"]
        speed = max(8, me["stats"].get("walk_speed", 13))
        timeleft = z["shrink_end"] - t
        need = max(0, dnext - max(4, rnext * 0.50))
        urgent = (not me["in_zone"] or
                  dcur > z["radius"] - 8 or
                  (t > z["shrink_start"] - 16 and
                   need / max(3, speed * 0.7) + 10 > timeleft) or
                  (t > z["shrink_start"] and dnext > rnext - 7))
        if urgent:
            return (z["next_center"][0], z["next_center"][1]), "zone", True
        taking_fire = t - self.last_hit < 7.5
        outnumbered = close >= 2 and nearest < 110
        unseen_incoming = (not threats and
                           ((taking_fire and self.last_bearing is not None) or
                            (t - self.last_sound_time < 1.7 and
                             self.last_sound_kind == "laser_charge")))
        if unseen_incoming and hp < 0.92:
            bearing = (self.last_bearing if t - self.last_hit < 6
                       else self.last_sound_yaw)
            if bearing is not None:
                rx, ry = math.cos(bearing), math.sin(bearing)
                faux = {"pos": [p[0] + rx * 58, p[1] + ry * 58, p[2]],
                        "aim": [wrap(bearing + math.pi), 0], "charging": False}
                cover = self.find_cover(obs, [(faux, 58.0, 0.0)])
                if cover is not None:
                    return cover, "cover", False
                retreat = (p[0] - 40 * rx, p[1] - 40 * ry)
                if self.safety(obs, retreat):
                    return retreat, "flee", False
        disadvantage = (hp < TUNE["cover_hp"] or
                        (taking_fire and hp < TUNE["hurt_cover_hp"]) or
                        (hp < 0.78 and outnumbered))
        if target is None and self.ffa and nearest < 90 and close:
            disadvantage = True
        if (disadvantage or (taking_fire and outnumbered and hp < 0.85)):
            cover = self.find_cover(obs, threats)
            if cover is not None:
                return cover, "cover", False
            if threats and nearest < 70:
                flee = threats[0][0]["pos"]
                vx, vy = unit(p[0] - flee[0], p[1] - flee[1])
                goal = (p[0] + vx * 35, p[1] + vy * 35)
                if self.safety(obs, goal):
                    return goal, "flee", False
        # Reach loot safely before the opponents converge; prioritize a laser.
        weapons = [w["kind"] if w else None for w in me["weapons"]]
        have_laser = "laser" in weapons
        have_secondary = weapons[1] is not None
        local_threat = nearest < TUNE["avoid_range"] and (
            not self.ffa or nearest < 160)
        if (t - self.last_sound_time < 2.2 and
                any(q["band"] == "near" and t - q["seen"] < 2
                    for q in self.sound_contacts)):
            local_threat = True
        choices = []
        for ident, (pck, seen) in self.loot.items():
            if ident in self.bad_pickups:
                continue
            kind = pck.get("kind", "")
            if kind in weapons or kind not in RANK:
                continue
            d = distance(p, pck["pos"])
            if (abs(p[2] - pck["pos"][2]) > 4.5 or
                    d > (TUNE["laser_search_radius"] if kind == "laser" else 145)): 
                continue
            if not self.safety(obs, pck["pos"], 7):
                continue
            if any(distance(tr["pos"], pck["pos"]) < 40
                   for tr, _, a in threats if a < 4):
                continue
            if local_threat and d > 55 and (
                    kind != "laser" or hp < 0.72 or
                    t - self.last_hit < 4.5 or nearest < 70):
                continue
            value = {"laser": TUNE["laser_value"],
                     "lightning": 145, "mortar": 95}.get(kind, 0)
            if have_secondary:
                value -= 115
                if have_laser and kind != "lightning":
                    value -= 100
            if have_secondary and me["weapons"][1]["kind"] == "laser" and kind != "laser":
                value = -1
            score = value - d * (0.37 if kind == "laser" else 0.73) - (t - seen) * 0.30
            if score > 0:
                choices.append((score, (pck["pos"][0], pck["pos"][1]), "weapon"))
        if not local_threat:
            for ident, (cube, seen) in self.cube_memory.items():
                d = distance(p, cube["pos"])
                if d > 75 or not self.safety(obs, cube["pos"], 6):
                    continue
                if any(distance(tr["pos"], cube["pos"]) < 35
                       for tr, _, age in threats if age < 4):
                    continue
                value = 84 + (40 if me["cubes"] < 3 else 0)
                choices.append((value - d * 0.9 - (t - seen), cube["pos"][:2], "cube"))
            for drop in obs.get("drops", []):
                d = distance(p, drop["pos"])
                if d > 170 or drop["lands_in"] > 14:
                    continue
                if not self.safety(obs, drop["pos"], 7):
                    continue
                if any(distance(tr["pos"], drop["pos"]) < 80
                       for tr, _, age in threats if age < 6):
                    continue
                val = 230 + (me["max_hp"] - me["hp"]) * 0.10 - d * 1.0
                choices.append((val, drop["pos"][:2], "drop"))
        # Early unarmed scouting. Persist the goal instead of changing targets at every step.
        if (not have_secondary and t < 64 and not local_threat and
                self.scout_goal is not None and t < self.scout_until and
                self.safety(obs, self.scout_goal)):
            if distance(p, self.scout_goal) > 8:
                choices.append((93 - distance(p, self.scout_goal) * 0.09,
                                self.scout_goal, "scout"))
        if not have_secondary and t < 64 and not local_threat:
            for d in (55, 90, 130):
                for i in range(12):
                    a = i * TAU / 12 + self.slot * 0.3
                    goal = (p[0] + math.cos(a) * d, p[1] + math.sin(a) * d)
                    if self.map is not None and not self.map.free(*goal):
                        continue
                    if not self.safety(obs, goal, 12):
                        continue
                    explored_distance = min(
                        (math.hypot(goal[0] - kx * 25, goal[1] - ky * 25)
                         for kx, ky in self.explored),
                        default=125)
                    score = 89 - d * 0.05 + min(120, explored_distance) * .19
                    if self.hold is not None and distance(goal, self.hold) < 8:
                        score += 2
                    if choices and max(c[0] for c in choices) > score:
                        continue
                    choices.append((score, goal, "scout"))
            # Time-limited exploration stays within the next circle.
        if choices and (not local_threat or target is None):
            score, place, mode = max(choices, key=lambda c: c[0])
            if score > 30:
                if mode == "scout":
                    self.scout_goal = tuple(place)
                    self.scout_until = t + 9
                return place, mode, False
        # Test-only policy: keep a ranged firing lane when a recent, armed
        # lightning opponent is inside its close-range threat envelope.
        # No change to baseline behavior unless lightning_spacing=1.
        if target is not None and TUNE["lightning_spacing"]:
            td = distance(p, target["pos"])
            if (t - target["seen"] < 2.0 and td < 58 and hp > 0.25 and
                    "lightning" in target.get("weapons", ())):
                rx, ry = unit(p[0] - target["pos"][0],
                              p[1] - target["pos"][1])
                for extension in (34.0, 23.0, 14.0):
                    retreat = (p[0] + rx * extension, p[1] + ry * extension)
                    if self.safety(obs, retreat, 7) and (
                            self.map is None or self.map.free(*retreat)):
                        return retreat, "spacing", False
        if target is not None and not self.ffa:
            d = distance(p, target["pos"])
            hp_enemy = target["hp"] / max(1, target["max_hp"])
            # Fight one hunter when safe; retreat if it can draw other squad members.
            if d < TUNE["duel_range"] and hp > TUNE["duel_hp"] and close < 2:
                return (p[0], p[1]), "duel", False
            if d > 115 and d < 200 and hp > 0.60 and hp_enemy < 0.42 and close < 2:
                return (target["pos"][0], target["pos"][1]), "finish", False
        return center, "hold", False

    def steer(self, obs, goal, mode, urgent, threats):
        me, t, p = obs["self"], obs["t"], obs["self"]["pos"]
        x, y = p[:2]
        energy = me.get("energy", 0)
        if mode == "duel" and threats:
            tr, d, _ = threats[0]
            vx, vy = unit(x - tr["pos"][0], y - tr["pos"][1])
            sideways = (-vy * self.strafe_dir, vx * self.strafe_dir)
            desire = 52 if any(w and w["kind"] == "lightning" for w in me["weapons"]) else 75
            if d > desire + 14:
                dx, dy = -vx * 0.4 + sideways[0] * 0.9, -vy * 0.4 + sideways[1] * 0.9
            elif d < desire - 19:
                dx, dy = vx * 0.55 + sideways[0] * 0.8, vy * 0.55 + sideways[1] * 0.8
            else:
                dx, dy = sideways
        else:
            gx, gy = goal
            if self.nav is not None:
                try:
                    gx, gy = self.nav.route(x, y, gx, gy, t, steps=125)
                except Exception:
                    pass
            dx, dy = gx - x, gy - y
        if t > self.strafe_until:
            self.strafe_dir *= -1
            self.strafe_until = t + self.rng.uniform(0.7, 1.4)
        if mode in ("hold", "scout", "weapon", "cube", "drop") and not urgent:
            # Gently repel known enemies but do not run out of the circle to do it.
            ax, ay = 0.0, 0.0
            for tr, d, age in threats:
                if d < DEFENSE_RADIUS and age < 4:
                    weight = (DEFENSE_RADIUS - d) / DEFENSE_RADIUS
                    ux, uy = unit(x - tr["pos"][0], y - tr["pos"][1])
                    ax += ux * weight
                    ay += uy * weight
            for audible in self.sound_contacts[-10:]:
                age = t - audible["seen"]
                if age > 3.5:
                    continue
                q = audible["pos"]
                estimated = distance((x, y), q)
                if estimated > 205:
                    continue
                ux, uy = unit(x - q[0], y - q[1])
                amount = (205 - estimated) / 205 * (1 - age / 4)
                if self.ffa:
                    amount *= 0.55
                ax += ux * amount * 0.9
                ay += uy * amount * 0.9
            if t - self.last_hit < 6 and self.last_bearing is not None:
                ax -= math.cos(self.last_bearing) * 0.9
                ay -= math.sin(self.last_bearing) * 0.9
            ddx, ddy = unit(dx, dy)
            dx, dy = ddx + 1.3 * ax, ddy + 1.3 * ay
        dx, dy = unit(dx, dy)
        if self.map is not None and not self.map.free(x + dx * 9, y + dy * 9):
            alternatives = []
            yaw = math.atan2(dy, dx)
            for k, aoff in enumerate((0, 0.42, -0.42, 0.8, -0.8, 1.25, -1.25,
                                      1.65, -1.65, math.pi)):
                a = yaw + aoff
                clear = self.map.walk_score(x, y, a)
                score = clear - abs(aoff) * 2.0
                alternatives.append((score, math.cos(a), math.sin(a)))
            _, dx, dy = max(alternatives)
        if self.prev_pos is not None:
            moved = distance(p, self.prev_pos)
            moving = mode != "duel" and distance(p, goal) > 13
            if moving and moved < 0.35:
                self.stuck += 1
            else:
                self.stuck = max(0, self.stuck - 2)
            if self.stuck >= 17:
                self.unstuck_until = t + 1.4
                self.unstuck_yaw = math.atan2(dy, dx) + self.rng.choice((-1.0, 1.0))
                self.stuck = 0
        self.prev_pos = p[:]
        boost = (urgent or mode in ("cover", "flee", "finish") or
                 (mode == "spacing" and energy > 58 and
                  any(d < 47 and a < 2 and "lightning" in tr.get("weapons", ())
                      for tr, d, a in threats)) or
                 (mode == "zone" and distance(p, goal) > 38) or
                 (mode == "weapon" and me["weapons"][1] is None and
                  distance(p, goal) > 15)) and energy > 28
        jump = False
        if t < self.unstuck_until:
            dx, dy = math.cos(self.unstuck_yaw), math.sin(self.unstuck_yaw)
            jump = me.get("grounded", True)
            boost = energy > 17
        if distance(p, goal) < 6 and mode not in ("flee", "duel", "cover"):
            dx, dy, boost = 0.0, 0.0, False
        if mode == "hold" and distance(p, goal) < 19 and not urgent:
            dx, dy = 0.0, 0.0
            boost = False
        # Always preserve enough energy for an emergency jet escape.
        if energy < 30:
            boost = False
        return [round(dx, 5), round(dy, 5)], boost, jump

    def dodge(self, obs, move):
        me, p = obs["self"], obs["self"]["pos"]
        sx, sy = 0.0, 0.0
        for shell in obs.get("projectiles", []):
            q, v = shell["pos"], shell["vel"]
            if distance(p, q) > 140:
                continue
            if shell["kind"] == "mortar":
                g = self.cfg.get("projectile", {}).get("gravity", 22)
                vz = v[2]
                alt = self.map.ground(*q[:2]) if self.map else p[2]
                radicand = max(0, vz * vz + 2 * g * max(0, q[2] - alt))
                hit_s = max(0.0, (vz + math.sqrt(radicand)) / g)
                if hit_s < 2:
                    px, py = q[0] + v[0] * hit_s, q[1] + v[1] * hit_s
                    if math.hypot(px - p[0], py - p[1]) < 21:
                        ux, uy = unit(p[0] - px, p[1] - py)
                        sx += ux * 5
                        sy += uy * 5
            else:
                rvx, rvy = v[0] - me["vel"][0], v[1] - me["vel"][1]
                dx, dy = p[0] - q[0], p[1] - q[1]
                vv = rvx * rvx + rvy * rvy
                if vv < 0.01:
                    continue
                at = clamp((dx * rvx + dy * rvy) / vv, 0, 0.85)
                near = math.hypot(dx - rvx * at, dy - rvy * at)
                if near < 5.0:
                    ux, uy = unit(-rvy, rvx)
                    side = 1 if ux * dx + uy * dy > 0 else -1
                    sx += side * ux * 4
                    sy += side * uy * 4
        for tr, d, age in self.threats(p, obs["t"], 130):
            if (tr["charging"] and age < 1.0 and
                    abs(wrap(face(tr["pos"], p) - tr["aim"][0])) < 0.24 and
                    d < 130):
                ux, uy = unit(p[0] - tr["pos"][0], p[1] - tr["pos"][1])
                sx += -uy * self.strafe_dir * 1.6
                sy += ux * self.strafe_dir * 1.6
        if sx or sy:
            return list(unit(move[0] + sx, move[1] + sy))
        return move

    def projectile_lead(self, p, v, shooter, shooter_v, speed):
        dx = p[0] + v[0] * 0.055 - shooter[0] - shooter_v[0] * 0.055
        dy = p[1] + v[1] * 0.055 - shooter[1] - shooter_v[1] * 0.055
        dz = p[2] + v[2] * 0.055 - shooter[2] - shooter_v[2] * 0.055
        ax, ay, az = (v[0] - shooter_v[0] * 0.03,
                      v[1] - shooter_v[1] * 0.03,
                      v[2] - shooter_v[2] * 0.03)
        qa = ax * ax + ay * ay + az * az - speed * speed
        qb = 2 * (dx * ax + dy * ay + dz * az)
        qc = dx * dx + dy * dy + dz * dz
        tm = math.sqrt(qc) / max(1, speed)
        if abs(qa) > 1e-5:
            disc = qb * qb - 4 * qa * qc
            if disc >= 0:
                root = math.sqrt(disc)
                candidates = [z for z in ((-qb - root) / (2 * qa),
                                           (-qb + root) / (2 * qa)) if z > 0]
                if candidates:
                    tm = min(candidates)
        return [p[i] + v[i] * clamp(tm + 0.06, 0, 1.2) for i in range(3)]

    def aim_and_fire(self, obs, target, mode, threats, action):
        me, p = obs["self"], obs["self"]["pos"]
        st = me.get("stats", {})
        muzzle = p[2] + st.get("muzzle_height", 7.0)
        guns = me["weapons"]
        w0, w1 = guns[0], guns[1]
        active = None
        if target is not None:
            active = target
        elif not threats and mode not in ("cover", "flee", "hold"):
            # Only farm when unthreatened. Shooting interrupts HP regeneration.
            actors = list(obs.get("crates", [])) + [
                v for v in obs.get("mechs", []) if v.get("kind") == "npc"
            ]
            candidates = []
            for a in actors:
                d = distance(a["pos"], p)
                if d > 100:
                    continue
                if a.get("kind") == "npc" and me["hp"] < me["max_hp"] * 0.75:
                    continue
                candidates.append((d, a))
            if candidates:
                active = min(candidates, key=lambda c: c[0])[1]
        if active is None:
            if self.last_bearing is not None and obs["t"] - self.last_hit < 8.0:
                action["aim"] = [self.last_bearing, 0.0]
            elif self.last_sound_yaw is not None and obs["t"] - self.last_sound_time < 4:
                action["aim"] = [self.last_sound_yaw, 0.0]
            else:
                action["aim"] = [wrap(me["aim"][0] + 0.32), 0.0]
            return
        ep = active["pos"]
        center_z = 4.5 if active.get("kind", "mech") == "mech" else (
            1.75 if active.get("kind") == "npc" else 1.4)
        scale = 1.0 + 0.05 * active.get("cubes", 0)
        cent = [ep[0], ep[1], ep[2] + center_z * scale]
        d = distance(p, ep)
        if d < 0.1:
            return
        visible = True
        if self.map is not None:
            visible = self.map.clear(p[0], p[1], ep[0], ep[1], inflated=False)
        vel = active.get("vel", (0, 0, 0))
        speed = self.cfg.get("weapons", {}).get("gun", {}).get("speed", 252)
        if w0 and w0.get("kind") == "gun":
            speed = w0.get("stats", {}).get("speed", speed)
        gunpt = self.projectile_lead(cent, vel, (p[0], p[1], muzzle),
                                     me["vel"], speed)
        laserpt = [cent[i] + vel[i] * 0.06 for i in range(3)]
        gunyaw = face(p, gunpt)
        gunpitch = math.atan2(gunpt[2] - muzzle, distance(p, gunpt))
        laseryaw = face(p, laserpt)
        laserpitch = math.atan2(laserpt[2] - muzzle, distance(p, laserpt))
        use_laser_aim = w1 and w1["kind"] == "laser" and (
            w1.get("charge", 0) > 0.53)
        aimyaw, aimpitch = ((laseryaw, laserpitch) if use_laser_aim else
                            (gunyaw, gunpitch))
        fire = [False, False]
        secondary = w1.get("kind", "") if w1 else ""
        if secondary == "mortar":
            if 32 < d < 225 and w1.get("cooldown", 1) < 0.12:
                v = w1.get("stats", {}).get("speed", 72)
                g = self.cfg.get("projectile", {}).get("gravity", 22)
                dh = cent[2] - muzzle
                disc = v ** 4 - g * (g * d * d + 2 * dh * v * v)
                if disc >= 0:
                    low = math.atan2(v * v - math.sqrt(disc), g * d)
                    # Prefer the low arc when visible and high arc when shooting over cover.
                    pitch = low if visible else math.atan2(v * v + math.sqrt(disc), g * d)
                    if pitch < 1.44:
                        aimyaw, aimpitch = laseryaw, pitch
                        if (abs(wrap(me["aim"][0] - aimyaw)) < 0.055 and
                                abs(me["aim"][1] - aimpitch) < 0.075):
                            fire[1] = True
        elif secondary == "laser":
            charge = w1.get("charge", 0)
            charge_s = w1.get("stats", {}).get("charge",
                        self.cfg.get("weapons", {}).get("laser", {}).get("charge", 0.75))
            aligned = (abs(wrap(me["aim"][0] - laseryaw)) < clamp(2.1 / d, .014, .095) and
                       abs(me["aim"][1] - laserpitch) < clamp(3.2 / d, .03, .13))
            if d < 275 and (visible or charge > 0.2):
                if charge <= 0.001:
                    fire[1] = w1.get("cooldown", 0) <= 0.11
                elif charge < charge_s - 0.10 or not aligned:
                    fire[1] = True
                else:
                    # Releasing a charged laser is a separate action from charging.
                    fire[1] = False
            elif charge > 0.001:
                fire[1] = charge < charge_s + 1.6
        elif secondary == "lightning":
            rng = w1.get("stats", {}).get("range", 45)
            if (d < rng - 1 and visible and me["energy"] >= 4 and
                    abs(wrap(me["aim"][0] - laseryaw)) < 0.20 and
                    w1.get("cooldown", 0) <= 0.12):
                fire[1] = True
        if w0 and w0["kind"] == "gun":
            if (visible and d < 220 and w0.get("cooldown", 0) <= 0.11 and
                    w0.get("ammo", 0) > 0 and
                    abs(wrap(me["aim"][0] - gunyaw)) < clamp(2.3 / d, 0.015, .10) and
                    abs(me["aim"][1] - gunpitch) < clamp(3.4 / d, .032, .13)):
                fire[0] = True
            if w0.get("ammo", 0) <= 0 or (
                    w0.get("ammo", 0) <= 3 and d > 115 and
                    w0.get("reload", 0) <= 0):
                action["reload"] = True
        action["aim"] = [wrap(aimyaw), clamp(aimpitch, -1.45, 1.45)]
        action["fire"] = fire

    def act(self, obs):
        self.update(obs)
        me, p, t = obs["self"], obs["self"]["pos"], obs["t"]
        threats = self.threats(p, t)
        target = self.enemy(obs, threats)
        goal, mode, urgent = self.choose_goal(obs, threats, target)
        a = {"tick": obs["tick"]}
        if obs.get("offer"):
            choices = obs["offer"].get("choices", [])
            if choices:
                a["pick"] = min(range(len(choices)),
                    key=lambda i: UPGRADES.index(choices[i]["id"])
                    if choices[i]["id"] in UPGRADES else 100)
        for item in obs.get("pickups", []):
            if item["id"] in self.bad_pickups:
                continue
            if distance(p, item["pos"]) < self.cfg["loot"].get("pickup_radius", 4.0) - 0.1 and (
                    abs(p[2] - item["pos"][2]) < 4):
                held = me["weapons"]
                kinds = [w["kind"] if w else None for w in held]
                kind = item["kind"]
                if kind in kinds or kind == "gun":
                    continue
                if held[1] is None:
                    a["take"] = item["id"]
                    break
                current = held[1]["kind"]
                if (RANK.get(kind, 0) > RANK.get(current, 0) and
                        not (current == "laser" and held[1].get("charge", 0) > .01)):
                    a["take"], a["drop"] = item["id"], 1
                    break
        move, boost, jump = self.steer(obs, goal, mode, urgent, threats)
        a["move"] = self.dodge(obs, move)
        a["boost"] = boost or (
            me["energy"] > 43 and me["grounded"] and
            t - self.last_sound_time < 1.1 and
            self.last_sound_kind == "laser_charge")
        a["jump"] = jump
        self.aim_and_fire(obs, target, mode, threats, a)
        # If hiding to regenerate, avoid dealing damage.
        if mode in ("cover", "flee") and not urgent:
            # Quiet recovery is more valuable than chip damage across an obstacle.
            if target is None or (distance(p, target["pos"]) > 65 and
                                  me["hp"] < me["max_hp"] * 0.72):
                a["fire"] = [False, False]
        if obs["tick"] % 12 == 0:
            mf.draw.label("%s | HP %.0f | cubes %d | %s" %
                          (mode, me["hp"], me["cubes"],
                           "FFA" if self.ffa else "squad"))
            mf.draw.point([goal[0], goal[1], p[2]], "#66ccee", 5)
        return a


if __name__ == "__main__":
    mf.run(Bot)
