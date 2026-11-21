"""Verify charging-window parameter changes the intended branch only."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs


class LaserReleaseWindowTests(unittest.TestCase):
    def test_aligned_partial_charge_release_window(self):
        bot = make_bot()
        sample = obs(t=6, with_laser=True)
        sample["self"]["weapons"][1]["charge"] = 0.60
        sample["mechs"] = [{
            "kind": "mech", "id": 7, "pos": [40, 0, 0],
            "vel": [0, 0, 0], "hp": 1400, "max_hp": 1400,
            "aim": [3.141592653589793, 0], "weapons": ["gun"]
        }]
        act = bot.act(sample)
        expected = 0.60 < 0.75 - TUNE["laser_release_margin"]
        self.assertEqual(act["fire"][1], expected)


if __name__ == "__main__":
    unittest.main()
