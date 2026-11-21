"""Regression checks for FFA-only holding-point repulsion."""
import random
import unittest
from unittest.mock import patch

import bot


class FfaHoldEvasionTests(unittest.TestCase):
    def setUp(self):
        self.agent = object.__new__(bot.Bot)
        self.agent.map = self.agent.nav = None
        self.agent.rng = random.Random(7)
        self.agent.strafe_until = 0.0
        self.agent.strafe_dir = 1
        self.agent.sound_contacts = []
        self.agent.last_hit = -100.0
        self.agent.last_bearing = None
        self.agent.last_sound_time = -100.0
        self.agent.prev_pos = None
        self.agent.stuck = 0
        self.agent.unstuck_until = -100.0
        self.agent.unstuck_yaw = 0.0
        self.agent.ffa = False
        self.obs = {"t": 50.0, "self": {"pos": [0.0, 0.0, 0.0],
                                          "energy": 70.0, "grounded": True,
                                          "weapons": [{"kind": "gun"}, None]}}
        self.near = [({"pos": [60.0, 0.0, 0.0]}, 60.0, 0.2)]

    def move(self, mode_ffa, threshold, threats=None):
        self.agent.ffa = mode_ffa
        with patch.dict(bot.TUNE, {"ffa_hold_evasion_radius": threshold}):
            move, boost, jump = self.agent.steer(
                self.obs, (0.0, 0.0), "hold", False,
                self.near if threats is None else threats)
        self.assertFalse(boost)
        self.assertFalse(jump)
        return move

    def test_original_baseline_stops_on_target(self):
        self.assertEqual(self.move(True, 0), [0.0, 0.0])

    def test_squad_holding_point_never_evades_from_new_gate(self):
        self.assertEqual(self.move(False, 200), [0.0, 0.0])

    def test_ffa_holding_point_moves_away_from_nearby_enemy(self):
        self.assertLess(self.move(True, 200)[0], -0.9)

    def test_ffa_stops_when_no_incoming_threat(self):
        self.assertEqual(self.move(True, 200, []), [0.0, 0.0])

    def test_recent_damage_triggers_ffa_only(self):
        self.agent.last_hit = self.obs["t"] - 1.0
        self.agent.last_bearing = 0.0
        self.assertLess(self.move(True, 200, [])[0], -0.9)
        self.assertEqual(self.move(False, 200, []), [0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
