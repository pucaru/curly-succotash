"""Regressions for front-arc orientation while disengaging."""
import math
import unittest
from unittest.mock import patch
import bot


class DefensiveFacingTests(unittest.TestCase):
    def setUp(self):
        self.agent = object.__new__(bot.Bot)
        self.agent.last_bearing = None
        self.agent.last_hit = -100.0
        self.agent.last_sound_yaw = None
        self.agent.last_sound_time = -100.0
        self.obs = {
            "t": 50.0,
            "self": {"pos": [0.0, 0.0, 0.0],
                     "stats": {}, "weapons": [{"kind": "gun"}, None],
                     "aim": [0.0, 0.0]},
        }
        self.threats = [({"pos": [0.0, 60.0, 0.0]}, 60.0, 0.2)]

    def face(self, maxrange):
        action = {}
        with patch.dict(bot.TUNE, {"defensive_facing_range": maxrange}):
            self.agent.aim_and_fire(self.obs, None, "hold", self.threats, action)
        return action["aim"][0]

    def test_near_threat_facing_keeps_front_arc(self):
        self.assertAlmostEqual(self.face(95.0), math.pi / 2)

    def test_out_of_range_keeps_search_aim(self):
        self.assertAlmostEqual(self.face(45.0), 0.32)

    def test_recent_damage_bearing_takes_precedence(self):
        self.agent.last_bearing = -1.1
        self.agent.last_hit = 49.8
        self.assertAlmostEqual(self.face(100.0), -1.1)


if __name__ == "__main__":
    unittest.main()
