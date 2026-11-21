"""Preemptive cover is gated on hostile aim, real cover, and production defaults."""
import math
import unittest

from bot import TUNE
from test_bot import make_bot, obs


class CoverMap:
    def free(self, x, y):
        return True

    def clear(self, x0, y0, x1, y1, inflated=True):
        # The shooter sees our current position but a nearby northward offset
        # hides behind a geometric obstruction.
        return not (x0 > 60 and y1 >= 7.5)


class PreemptCoverTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("preempt_cover_range", 0.0)

    def tearDown(self):
        TUNE["preempt_cover_range"] = self.old

    def scenario(self, shooter_yaw=math.pi):
        b = make_bot()
        b.map = CoverMap()
        d = obs(t=15)
        hostile = {"id": 9, "pos": [80, 0, 0], "aim": [shooter_yaw, 0],
                   "hp": 1400, "max_hp": 1400, "weapons": ["gun"]}
        return b, d, [(hostile, 80, 0)]

    def test_off_preserves_ordinary_goal(self):
        b, d, threats = self.scenario()
        TUNE["preempt_cover_range"] = 0
        goal, mode, _ = b.choose_goal(d, threats, None)
        self.assertNotEqual(mode, "cover")

    def test_aimed_enemy_enables_blocked_cover(self):
        b, d, threats = self.scenario()
        TUNE["preempt_cover_range"] = 110
        goal, mode, urgent = b.choose_goal(d, threats, None)
        self.assertEqual(mode, "cover")
        self.assertGreaterEqual(goal[1], 7.5)
        self.assertFalse(urgent)

    def test_enemy_looking_away_does_not_force_cover(self):
        b, d, threats = self.scenario(shooter_yaw=0.0)
        TUNE["preempt_cover_range"] = 110
        _, mode, _ = b.choose_goal(d, threats, None)
        self.assertNotEqual(mode, "cover")

    def test_out_of_range_does_not_force_cover(self):
        b, d, threats = self.scenario()
        TUNE["preempt_cover_range"] = 65
        _, mode, _ = b.choose_goal(d, threats, None)
        self.assertNotEqual(mode, "cover")


if __name__ == "__main__":
    unittest.main()
