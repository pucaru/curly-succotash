"""Rear-impact break independent of the standard duel movement."""
import math
import unittest
from unittest.mock import patch
from bot import TUNE
from test_bot import make_bot, obs

class RearImpactTests(unittest.TestCase):
    def scenario(self, rear=True, source=9):
        bot = make_bot()
        data = obs(t=10)
        data["self"]["hp"] = 1120
        data["mechs"] = [{
            "kind": "mech", "id": 7, "pos": [40, 0, 0],
            "vel": [0, 0, 0], "hp": 1100, "max_hp": 1400,
            "weapons": ["gun"], "aim": [math.pi, 0]
        }]
        data["events"] = [{"type": "damaged", "amount": 250,
                           "weapon": "gun", "bearing": math.pi,
                           "rear": rear, "by": source}]
        return bot, data

    def choice(self, bot, data):
        bot.update(data)
        threats = bot.threats(data["self"]["pos"], data["t"])
        enemy = bot.enemy(data, threats)
        return bot.choose_goal(data, threats, enemy)

    def test_baseline_unchanged(self):
        bot, data = self.scenario()
        with patch.dict(TUNE, {"rear_impact_evade": 0}):
            self.assertEqual(self.choice(bot, data)[1], "duel")

    def test_distinct_rear_attacker_evades_perpendicular(self):
        bot, data = self.scenario()
        with patch.dict(TUNE, {"rear_impact_evade": 1}):
            goal, mode, urgent = self.choice(bot, data)
        self.assertEqual(mode, "rear_evade")
        self.assertFalse(urgent)
        self.assertGreater(abs(goal[1]), 20.0)
        self.assertLess(abs(goal[0]), 1)

    def test_no_rear_hit_no_change(self):
        bot, data = self.scenario(rear=False)
        with patch.dict(TUNE, {"rear_impact_evade": 1}):
            self.assertEqual(self.choice(bot, data)[1], "duel")

    def test_selected_attacker_does_not_trigger(self):
        bot, data = self.scenario(source=7)
        with patch.dict(TUNE, {"rear_impact_evade": 1}):
            self.assertEqual(self.choice(bot, data)[1], "duel")

    def test_evasion_retains_fire_and_boost(self):
        bot, data = self.scenario()
        with patch.dict(TUNE, {"rear_impact_evade": 1}):
            result = bot.act(data)
        self.assertTrue(result["fire"][0])
        self.assertTrue(result["boost"])

if __name__ == "__main__":
    unittest.main()
