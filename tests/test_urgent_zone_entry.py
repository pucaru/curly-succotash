"""Independent urgent-zone-entry behavioral guardrails."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class UrgentZoneEntryTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("urgent_zone_entry_margin", 0.0)
    def tearDown(self):
        TUNE["urgent_zone_entry_margin"] = self.old
    def make_case(self, rnext=380):
        bot = make_bot()
        data = obs(t=132)
        data["self"]["pos"] = [-480.0, 0.0, 0.0]
        data["self"]["in_zone"] = False
        data["zone"]["center"] = [0.0, 0.0]
        data["zone"]["radius"] = 430.0
        data["zone"]["next_center"] = [0.0, 0.0]
        data["zone"]["next_radius"] = rnext
        return bot, data
    def test_entry_waypoint_shortens_large_circle_emergency(self):
        TUNE["urgent_zone_entry_margin"] = 24.0
        bot, data = self.make_case()
        goal, mode, urgent = bot.choose_goal(data, [], None)
        self.assertEqual(mode, "zone")
        self.assertTrue(urgent)
        self.assertAlmostEqual(goal[0], -356, places=3)
    def test_final_circle_still_targets_center(self):
        TUNE["urgent_zone_entry_margin"] = 64.0
        bot, data = self.make_case(rnext=25.0)
        goal, mode, urgent = bot.choose_goal(data, [], None)
        self.assertEqual(goal, (0.0, 0.0))
    def test_zero_margin_preserves_production_emergency(self):
        TUNE["urgent_zone_entry_margin"] = 0.0
        bot, data = self.make_case()
        goal, mode, urgent = bot.choose_goal(data, [], None)
        self.assertEqual(goal, (0.0, 0.0))

if __name__ == "__main__":
    unittest.main()
