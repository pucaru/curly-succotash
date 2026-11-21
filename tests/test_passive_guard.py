"""Deterministic safety checks for passive threat facing without combat."""
import math
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class PassiveFacingTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("passive_guard_range", 0)
    def tearDown(self):
        TUNE["passive_guard_range"] = self.old
    def make_ffa_case(self, d):
        bot = make_bot()
        bot.ffa = True
        data = obs(t=12)
        data["mechs"] = [{"kind":"mech", "id":7, "pos":[0.0,d,0.0],
             "vel":[0,0,0], "hp":1400,"max_hp":1400,
             "aim":[0,0], "weapons":["gun"], "charging": False}]
        return bot, data
    def test_passive_facing_protects_rear_without_firing(self):
        TUNE["passive_guard_range"] = 120
        bot, data = self.make_ffa_case(80)
        action = bot.act(data)
        self.assertAlmostEqual(action["aim"][0], math.pi/2, places=3)
        self.assertEqual(action.get("fire", [False,False]), [False,False])
    def test_range_gate_retains_default_scan(self):
        TUNE["passive_guard_range"] = 120
        bot, data = self.make_ffa_case(160)
        action = bot.act(data)
        self.assertAlmostEqual(action["aim"][0], .32, places=3)

if __name__ == "__main__":
    unittest.main()
