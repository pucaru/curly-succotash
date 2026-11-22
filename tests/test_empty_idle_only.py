"""Isolated empty-magazine-only reload tests: zero-ammo recovery, never partial."""
import unittest
from bot import Bot, TUNE

def hello():
    return {"slot": 1, "seed": 17, "map": {"dir": "/nonexistent"},
            "config": {"match": {"mechs": 16}, "loot": {"pickup_radius": 4},
                       "weapons": {"gun": {"speed": 252}}}}

def obs(ammo=7, reload_s=0, t=12.0):
    return {"tick": int(t * 10), "t": t, "alive": 16,
            "self": {"id": 1, "pos": [0,0,0], "vel": [0,0,0], "aim": [0,0],
                     "hp": 1400, "max_hp": 1400, "energy": 80, "grounded": True,
                     "cubes": 0, "in_zone": True,
                     "weapons": [{"kind": "gun", "ammo": ammo, "reload": reload_s,
                                  "cooldown": 0, "stats": {"speed":252,"mag":12}}, None],
                     "stats": {"walk_speed": 13, "muzzle_height": 7}},
            "mechs": [], "crates": [], "cubes": [], "pickups": [], "drops": [],
            "projectiles": [], "sounds": [], "events": [], "offer": None,
            "zone": {"center": [0,0], "radius": 560, "next_center": [0,0],
                     "next_radius": 380, "shrink_start":100, "shrink_end":150,"dps":20}}

class EmptyOnlyTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("empty_idle_reload", 0)
    def tearDown(self):
        TUNE["empty_idle_reload"] = self.old
    def test_off_keeps_empty_until_target(self):
        TUNE["empty_idle_reload"] = 0
        self.assertFalse(Bot(hello()).act(obs(ammo=0)).get("reload", False))
    def test_on_reloads_empty(self):
        TUNE["empty_idle_reload"] = 1
        self.assertTrue(Bot(hello()).act(obs(ammo=0)).get("reload", False))
    def test_no_partial_reload(self):
        TUNE["empty_idle_reload"] = 1
        for n in (1, 3, 7, 11, 12):
            self.assertFalse(Bot(hello()).act(obs(ammo=n)).get("reload", False))
    def test_no_restart_while_reloading(self):
        TUNE["empty_idle_reload"] = 1
        self.assertFalse(Bot(hello()).act(obs(ammo=0, reload_s=1.0)).get("reload", False))
    def test_empty_when_recent_damage(self):
        TUNE["empty_idle_reload"] = 1
        o = obs(ammo=0)
        o["events"] = [{"type":"damaged","amount":20,"bearing":1.2,"by":None}]
        self.assertTrue(Bot(hello()).act(o).get("reload", False))
    def test_empty_when_near_sound(self):
        TUNE["empty_idle_reload"] = 1
        o = obs(ammo=0)
        o["sounds"] = [{"kind":"gun","bearing":0.3,"dist":"near","age":0.1}]
        self.assertTrue(Bot(hello()).act(o).get("reload", False))

if __name__ == "__main__":
    unittest.main()
