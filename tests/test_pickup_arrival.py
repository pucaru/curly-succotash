"""Regression for the 6m stop versus <3.9m pickup distance mismatch."""
import unittest
from bot import Bot, TUNE

def hello(radius=4.0):
    return {"slot": 3, "seed": 42, "map": {"dir": "/missing"},
            "config": {"match": {"mechs": 16}, "loot": {"pickup_radius": radius},
                       "projectile": {"gravity": 22},
                       "weapons": {"gun": {"speed": 252}, "laser": {"charge": .75}}}}

def obs(x=0.0, target=5.2, t=5.0):
    return {"tick": int(t * 10), "t": t, "alive": 16,
            "self": {"id": 3, "pos": [x, 0, 0], "vel": [0, 0, 0],
                     "aim": [0, 0], "hp": 1400, "max_hp": 1400,
                     "energy": 100, "max_energy": 100, "grounded": True,
                     "cubes": 0, "in_zone": True,
                     "weapons": [{"kind": "gun", "ammo": 12, "cooldown": 0,
                                  "reload": 0, "stats": {"speed": 252}}, None],
                     "stats": {"walk_speed": 13, "muzzle_height": 7}},
            "mechs": [], "crates": [], "cubes": [],
            "pickups": [{"id": 8001, "kind": "laser", "pos": [target, 0, 0]}],
            "sounds": [], "projectiles": [], "events": [], "beams": [],
            "drops": [], "offer": None,
            "zone": {"center": [0, 0], "radius": 560,
                     "next_center": [20, 0], "next_radius": 380,
                     "shrink_start": 100, "shrink_end": 150, "dps": 20}}

class PickupTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("pickup_approach_fix")
    def tearDown(self):
        if self.old is None:
            TUNE.pop("pickup_approach_fix", None)
        else:
            TUNE["pickup_approach_fix"] = self.old
    def test_control_freezes_outside_take_radius(self):
        TUNE["pickup_approach_fix"] = 0
        a = Bot(hello()).act(obs())
        self.assertEqual(a["move"], [0.0, 0.0])
        self.assertNotIn("take", a)
    def test_candidate_moves_then_takes(self):
        TUNE["pickup_approach_fix"] = 1
        bot = Bot(hello())
        self.assertGreater(bot.act(obs())["move"][0], 0.9)
        self.assertEqual(bot.act(obs(x=2.0, t=5.1)).get("take"), 8001)
    def test_honors_configured_pickup_radius(self):
        TUNE["pickup_approach_fix"] = 1
        self.assertGreater(Bot(hello(radius=6)).act(obs(target=7))["move"][0], 0.9)
    def test_hold_still_stops(self):
        TUNE["pickup_approach_fix"] = 1
        b = Bot(hello()); data = obs(); b.update(data)
        movement, _, _ = b.steer(data, (5.2, 0), "hold", False, [])
        self.assertEqual(movement, [0.0, 0.0])
