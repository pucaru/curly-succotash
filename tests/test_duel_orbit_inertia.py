"""Predeclared causal checks for sustained lateral duel movement."""
import unittest
from unittest.mock import patch

from bot import TUNE
from test_bot import make_bot, obs


def enemy():
    return {"id": 7, "pos": [-55.0, 0.0, 0.0], "seen": 60,
            "aim": [0.0, 0.0], "weapons": ["gun"], "hp": 1400,
            "max_hp": 1400, "charging": False}


class DuelOrbitInertiaTests(unittest.TestCase):
    def test_long_orbit_when_enabled(self):
        bot = make_bot()
        data = obs(t=60, with_laser=True)
        tr = enemy()
        with patch.dict(TUNE, {"duel_orbit_commit": 1}):
            move, boost, jump = bot.steer(data, (0.0, 0.0), "duel", False,
                                          [(tr, 55.0, 0.0)])
        self.assertGreater(bot.strafe_until - data["t"], 2.7)
        self.assertFalse(jump)
        self.assertAlmostEqual(sum(v*v for v in move), 1.0, delta=0.001)

    def test_control_is_original_short_flip(self):
        bot = make_bot()
        data = obs(t=60, with_laser=True)
        with patch.dict(TUNE, {"duel_orbit_commit": 0}):
            bot.steer(data, (0.0, 0.0), "duel", False,
                      [(enemy(), 55.0, 0.0)])
        self.assertLessEqual(bot.strafe_until - data["t"], 1.40000001)

    def test_ffa_hold_uses_unchanged_timing(self):
        bot = make_bot()
        data = obs(t=60, with_laser=True)
        with patch.dict(TUNE, {"duel_orbit_commit": 1}):
            bot.steer(data, (0.0, 0.0), "hold", False,
                      [(enemy(), 55.0, 0.0)])
        self.assertLessEqual(bot.strafe_until - data["t"], 1.40000001)

    def test_unsafe_arc_vetoes_persistent_direction(self):
        bot = make_bot()
        data = obs(t=60, with_laser=True)
        data["zone"]["center"] = [0, 0]
        data["zone"]["radius"] = 14
        bot.strafe_until = 100
        bot.strafe_dir = 1
        with patch.dict(TUNE, {"duel_orbit_commit": 1}):
            bot.steer(data, (0.0, 0.0), "duel", False,
                      [(enemy(), 55.0, 0.0)])
        self.assertEqual(bot.strafe_dir, -1)


if __name__ == "__main__":
    unittest.main()
