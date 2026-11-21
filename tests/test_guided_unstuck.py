"""Regression test for the optional terrain-guided recovery heading."""
import math
import unittest
from bot import TUNE
from test_bot import make_bot, obs


class OneOpenCorridor:
    def free(self, x, y):
        return True

    def walk_score(self, x, y, angle, distance=16):
        return 22 if math.cos(angle) > 0.99 else 4


class GuidedUnstuckTests(unittest.TestCase):
    def test_recovery_selects_known_open_corridor(self):
        bot = make_bot()
        bot.map = OneOpenCorridor()
        bot.nav = None
        bot.prev_pos = [0.0, 0.0, 0.0]
        bot.stuck = 16
        original = TUNE.get("guided_unstuck")
        try:
            TUNE["guided_unstuck"] = True
            move, boost, jump = bot.steer(
                obs(t=1), (100, 0), "zone", True, [])
            self.assertLess(abs(bot.unstuck_yaw), 1e-5)
            self.assertGreater(move[0], 0.99)
            self.assertTrue(jump)
        finally:
            if original is None:
                TUNE.pop("guided_unstuck", None)
            else:
                TUNE["guided_unstuck"] = original


if __name__ == "__main__":
    unittest.main()
