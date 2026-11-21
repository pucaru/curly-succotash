"""Static line-of-sight-aware hold decision, preserving the default path."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class FakeMap:
    def __init__(self):
        self.rays = 0
    def free(self, x, y):
        return True
    def clear(self, x0, y0, x1, y1, inflated=True):
        self.rays += 1
        return x1 > 0.0

class ZoneLineOfSightTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("zone_los_penalty", 0.0)
    def tearDown(self):
        TUNE["zone_los_penalty"] = self.old
    def scenario(self):
        bot = make_bot()
        bot.map = FakeMap()
        data = obs(t=12)
        data["self"]["pos"] = [50.0, 0.0, 0.0]
        data["zone"]["next_center"] = [0.0, 0.0]
        data["zone"]["next_radius"] = 70.0
        data["mechs"] = [{
            "kind":"mech", "id":7,"pos":[180.0,0.0,0.0],
            "vel":[0.0,0.0,0.0], "hp":1400, "max_hp":1400,
            "aim":[3.14,0.0], "weapons":["gun"],"charging":False}]
        bot.update(data)
        return bot, data
    def test_zero_weight_keeps_nearest_side_without_raycast(self):
        TUNE["zone_los_penalty"] = 0.0
        bot, data = self.scenario()
        pt = bot.zone_target(data)
        self.assertGreater(pt[0], 0.0)
        self.assertEqual(bot.map.rays, 0)
    def test_positive_weight_changes_exposed_hold_location(self):
        TUNE["zone_los_penalty"] = 125.0
        bot, data = self.scenario()
        pt = bot.zone_target(data)
        self.assertLessEqual(pt[0], 0.0)
        self.assertGreater(bot.map.rays, 0)

if __name__ == "__main__":
    unittest.main()
