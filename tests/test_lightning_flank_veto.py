"""Causal regression tests for the isolated lightning flank-veto policy."""
import unittest
from unittest.mock import patch
from bot import TUNE
from test_bot import make_bot, obs


def lightning_target(t):
    return {"id": 7, "kind": "mech", "pos": [-35.0, 0.0, 0.0],
            "vel": [0, 0, 0], "aim": [0, 0], "hp": 800,
            "max_hp": 1400, "weapons": ["gun", "lightning"],
            "seen": t}


class FlankVetoTests(unittest.TestCase):
    def test_isolated_lightning_makes_safe_distance(self):
        bot = make_bot()
        data = obs(t=70, with_laser=True)
        tr = lightning_target(70)
        with patch.dict(TUNE, {"lightning_flank_veto": 1}):
            goal, mode, urgent = bot.choose_goal(data, [(tr, 35, 0)], tr)
        self.assertEqual(mode, "spacing")
        self.assertGreater(goal[0], 10)
        self.assertFalse(urgent)

    def test_second_hunter_vetoes_escape_into_flank(self):
        bot = make_bot()
        data = obs(t=70, with_laser=True)
        tr = lightning_target(70)
        other = dict(lightning_target(70), id=8, pos=[55, 20, 0], weapons=["laser"])
        with patch.dict(TUNE, {"lightning_flank_veto": 1}):
            goal, mode, urgent = bot.choose_goal(
                data, [(tr, 35, 0), (other, 58, 0)], tr)
        self.assertNotEqual(mode, "spacing")

    def test_recent_hit_from_other_angle_vetoes_retreat(self):
        bot = make_bot()
        data = obs(t=70, with_laser=True)
        bot.last_hit = 69
        bot.last_bearing = 0.0
        tr = lightning_target(70)
        with patch.dict(TUNE, {"lightning_flank_veto": 1}):
            _, mode, _ = bot.choose_goal(data, [(tr, 35, 0)], tr)
        self.assertNotEqual(mode, "spacing")

    def test_toggle_zero_is_original_policy(self):
        bot = make_bot()
        data = obs(t=70, with_laser=True)
        tr = lightning_target(70)
        with patch.dict(TUNE, {"lightning_flank_veto": 0}):
            _, mode, _ = bot.choose_goal(data, [(tr, 35, 0)], tr)
        self.assertNotEqual(mode, "spacing")


if __name__ == "__main__":
    unittest.main()
