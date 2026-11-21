"""Regression tests for hold-position movement under nearby threats."""
import random
import unittest
from unittest.mock import patch

import bot


class HoldRepulsionTests(unittest.TestCase):
    def setUp(self):
        self.agent = object.__new__(bot.Bot)
        self.agent.map = None
        self.agent.nav = None
        self.agent.rng = random.Random(3)
        self.agent.strafe_until = 0.0
        self.agent.strafe_dir = 1
        self.agent.sound_contacts = []
        self.agent.last_hit = -100
        self.agent.last_bearing = None
        self.agent.last_sound_time = -100
        self.agent.prev_pos = None
        self.agent.stuck = 0
        self.agent.unstuck_until = -100
        self.agent.unstuck_yaw = 0
        self.obs = {"t": 50.0, "self": {"pos": [0.0, 0.0, 0.0],
                                          "energy": 70.0, "grounded": True,
                                          "weapons": [{"kind": "gun"}, None]}}
        self.near = [({"pos": [60.0, 0.0, 0.0]}, 60.0, 0.2)]

    def move(self, radius, threats=None):
        with patch.dict(bot.TUNE, {"hold_evasion_radius": radius}):
            move, boost, jump = self.agent.steer(
                self.obs, (0.0, 0.0), "hold", False,
                self.near if threats is None else threats)
        self.assertFalse(boost)
        self.assertFalse(jump)
        return move

    def test_original_hold_stops_even_with_close_track(self):
        self.assertEqual(self.move(0), [0.0, 0.0])

    def test_nearby_enemy_keeps_evading_after_arrival(self):
        self.assertLess(self.move(130.0)[0], -0.9)

    def test_escaped_track_range_stops_at_hold(self):
        self.assertEqual(self.move(40.0), [0.0, 0.0])

    def test_unthreatened_hold_does_not_wander(self):
        self.assertEqual(self.move(130.0, []), [0.0, 0.0])

    def test_damage_bearing_starts_evasion_without_track(self):
        self.agent.last_hit = self.obs["t"] - 1.0
        self.agent.last_bearing = 0.0
        self.assertLess(self.move(130.0, [])[0], -0.9)


if __name__ == "__main__":
    unittest.main()
