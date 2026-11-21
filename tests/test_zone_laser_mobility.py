"""Urgent safe-zone mobility versus charging a laser (isolate policy toggle)."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs


def laser_enemy_obs(t, urgent):
    data = obs(t=t, with_laser=True)
    if urgent:
        data["self"]["pos"] = [-480.0, 0.0, 0.0]
    data["self"]["weapons"][1]["charge"] = 0.4
    x = data["self"]["pos"][0]
    data["mechs"] = [{"kind": "mech", "id": 7, "pos": [x + 42, 0, 0],
                      "vel": [0, 0, 0], "hp": 1200, "max_hp": 1400,
                      "aim": [3.14, 0], "weapons": ["gun"]}]
    return data


class ZoneLaserMobilityTests(unittest.TestCase):
    def test_switch_suppresses_only_during_urgent_travel(self):
        old = TUNE["zone_laser_mobility"]
        try:
            for flag in (0, 1):
                TUNE["zone_laser_mobility"] = flag
                endangered = make_bot().act(laser_enemy_obs(132, True))
                safe = make_bot().act(laser_enemy_obs(10, False))
                self.assertEqual(endangered["fire"][1], not bool(flag))
                self.assertTrue(safe["fire"][1])
        finally:
            TUNE["zone_laser_mobility"] = old

    def test_candidate_does_not_suppress_primary_gun(self):
        old = TUNE["zone_laser_mobility"]
        try:
            TUNE["zone_laser_mobility"] = 1
            action = make_bot().act(laser_enemy_obs(132, True))
            self.assertEqual(len(action["fire"]), 2)
            self.assertFalse(action["fire"][1])
        finally:
            TUNE["zone_laser_mobility"] = old


if __name__ == "__main__":
    unittest.main()
