"""Small deterministic checks for protocol-safe decisions and important combat branches."""
import math
import unittest

from bot import Bot


def make_bot():
    return Bot({
        "type": "hello", "protocol": "mechfight/1", "slot": 3, "seed": 42,
        "map": {"dir": "/path-that-does-not-exist"},
        "config": {
            "match": {"mechs": 16}, "loot": {"pickup_radius": 4},
            "projectile": {"gravity": 22},
            "weapons": {
                "gun": {"speed": 252},
                "laser": {"charge": 0.75},
                "mortar": {"speed": 72}, "lightning": {"range": 45},
            },
        },
    })


def obs(t=1, with_laser=False):
    guns = [{
        "kind": "gun", "ammo": 12, "cooldown": 0, "reload": 0,
        "stats": {"speed": 252},
    }, None]
    if with_laser:
        guns[1] = {"kind": "laser", "cooldown": 0, "charge": 0.75,
                   "stats": {"charge": .75}}
    return {
        "type": "obs", "tick": int(t * 10), "t": t, "alive": 16,
        "self": {"id": 3, "pos": [0.0, 0.0, 0.0], "vel": [0, 0, 0],
                 "aim": [0, math.atan2(-2.5, 40)], "hp": 1400, "max_hp": 1400,
                 "energy": 100, "max_energy": 100, "grounded": True,
                 "cubes": 0, "in_zone": True, "weapons": guns,
                 "stats": {"walk_speed": 13, "muzzle_height": 7}},
        "mechs": [], "crates": [], "cubes": [], "pickups": [],
        "sounds": [], "projectiles": [], "events": [], "beams": [],
        "drops": [], "offer": None,
        "zone": {"center": [0, 0], "radius": 560,
                 "next_center": [20, 0], "next_radius": 380,
                 "shrink_start": 100, "shrink_end": 150, "dps": 20},
    }


class DecisionTests(unittest.TestCase):
    def test_never_crashes_when_map_is_missing(self):
        bot = make_bot()
        action = bot.act(obs())
        self.assertEqual(action["tick"], 10)
        self.assertEqual(len(action["move"]), 2)
        self.assertEqual(len(action["aim"]), 2)

    def test_upgrade_prefers_plating(self):
        bot = make_bot()
        data = obs()
        data["offer"] = {"id": 1, "expires": 5, "choices": [
            {"id": "gun_rate"}, {"id": "plating"}, {"id": "sensors"},
        ]}
        self.assertEqual(bot.act(data)["pick"], 1)

    def test_take_uncontested_laser(self):
        bot = make_bot()
        data = obs()
        data["pickups"] = [{"id": 8001, "pos": [1, 0, 0], "kind": "laser"}]
        self.assertEqual(bot.act(data).get("take"), 8001)

    def test_releases_fully_charged_aligned_laser(self):
        bot = make_bot()
        data = obs(with_laser=True)
        data["mechs"] = [{"kind": "mech", "id": 7, "pos": [40, 0, 0],
                          "vel": [0, 0, 0], "hp": 1400, "max_hp": 1400,
                          "aim": [math.pi, 0], "weapons": ["gun"]}]
        result = bot.act(data)
        self.assertEqual(result["fire"][1], False)
        self.assertAlmostEqual(result["aim"][0], 0, places=3)

    def test_zone_emergency(self):
        bot = make_bot()
        data = obs(t=132)
        data["self"]["pos"] = [-480, 0, 0]
        data["self"]["in_zone"] = False
        action = bot.act(data)
        self.assertGreater(action["move"][0], 0)

    def test_far_laser_beats_random_scouting(self):
        bot = make_bot()
        data = obs(t=5)
        data["pickups"] = [{"id": 8111, "kind": "laser", "pos": [145, 0, 0]}]
        bot.update(data)
        goal, mode, urgent = bot.choose_goal(data, [], None)
        self.assertEqual(mode, "weapon")
        self.assertGreater(goal[0], 130)

    def test_aim_toward_recent_gun_sound(self):
        bot = make_bot()
        data = obs(t=6)
        data["sounds"] = [{"kind": "gun", "bearing": math.pi / 2,
                            "dist": "mid", "age": 0}]
        action = bot.act(data)
        self.assertAlmostEqual(action["aim"][0], math.pi / 2, places=3)

    def test_detect_independent_death_early(self):
        bot = make_bot()
        first = obs(t=4)
        bot.act(first)
        second = obs(t=5)
        second["alive"] = 15
        bot.act(second)
        self.assertTrue(bot.ffa)


if __name__ == "__main__":
    unittest.main()
