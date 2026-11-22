"""Cube auto-pickup requires reaching within cubes.pickup_radius."""
import unittest
from bot import Bot, TUNE

def hello(radius=3.5):
    return {"slot": 3, "seed": 42, "map": {"dir": "/missing"},
            "config": {"match": {"mechs": 16}, "loot": {"pickup_radius": 4},
                       "cubes": {"pickup_radius": radius}, "projectile": {"gravity": 22},
                       "weapons": {"gun": {"speed": 252}, "laser": {"charge": .75}}}}

def obs(x=0.0, cube=5.2, t=5):
    return {"tick": int(t * 10), "t": t, "alive": 16,
            "self": {"id": 3, "pos": [x, 0, 0], "vel": [0, 0, 0],
                     "aim": [0, 0], "hp": 1400, "max_hp": 1400,
                     "energy": 100, "max_energy": 100, "grounded": True,
                     "cubes": 0, "in_zone": True,
                     "weapons": [{"kind": "gun", "ammo": 12, "cooldown": 0,
                                  "reload": 0, "stats": {"speed": 252}}, None],
                     "stats": {"walk_speed": 13, "muzzle_height": 7}},
            "mechs": [], "crates": [],
            "cubes": [{"id": 5001, "pos": [cube, 0, 0]}],
            "pickups": [], "sounds": [], "projectiles": [],
            "events": [], "beams": [], "drops": [], "offer": None,
            "zone": {"center": [0, 0], "radius": 560,
                     "next_center": [20, 0], "next_radius": 380,
                     "shrink_start": 100, "shrink_end": 150, "dps": 20}}

class CubeArrivalTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("cube_approach_fix")
    def tearDown(self):
        if self.old is None:
            TUNE.pop("cube_approach_fix", None)
        else:
            TUNE["cube_approach_fix"] = self.old
    def test_mode_is_cube(self):
        b = Bot(hello()); d = obs(); b.update(d)
        self.assertEqual(b.choose_goal(d, [], None)[1], "cube")
    def test_control_stops_outside_cube_radius(self):
        TUNE["cube_approach_fix"] = 0
        self.assertEqual(Bot(hello()).act(obs())["move"], [0.0, 0.0])
    def test_candidate_enters_cube_pickup_radius(self):
        TUNE["cube_approach_fix"] = 1
        self.assertGreater(Bot(hello()).act(obs())["move"][0], 0.9)
    def test_tracks_configured_cube_radius(self):
        TUNE["cube_approach_fix"] = 1
        self.assertGreater(Bot(hello(radius=5.0)).act(obs(cube=6.2))["move"][0], 0.9)
    def test_weapon_stop_behavior_unchanged(self):
        TUNE["cube_approach_fix"] = 1
        b = Bot(hello()); d = obs(); b.update(d)
        movement, _, _ = b.steer(d, (5.2, 0), "weapon", False, [])
        self.assertEqual(movement, [0.0, 0.0])
