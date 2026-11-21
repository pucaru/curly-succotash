"""Regression checks: selected-target duel movement vs nearest unrelated threat."""
import unittest
from unittest.mock import patch
from bot import Bot, TUNE


def bot():
    return Bot({"config": {"match": {"mechs": 16}}, "slot": 0,
                "seed": 3, "map": {"dir": "/no-map-duel-test"}})


def observation():
    return {"t": 4.0, "self": {"pos": [0, 0, 0], "energy": 100,
             "weapons": [{"kind": "gun"}, None]}, "zone": {}}


class DuelAnchorTests(unittest.TestCase):
    def test_selected_target_used_instead_of_nearest(self):
        hero = bot()
        hero.strafe_until = 100
        nearer = {"pos": [0, 30, 0]}
        selected = {"pos": [80, 0, 0]}
        threats = [(nearer, 30, 0), (selected, 80, 0)]
        with patch.dict(TUNE, {"duel_target_tracking": 1}):
            move, _, _ = hero.steer(observation(), (0, 0), "duel",
                                     False, threats, selected)
        self.assertAlmostEqual(move[0], 0.0, places=3)
        self.assertLess(move[1], -0.98)

    def test_control_preserves_nearest_threat_behavior(self):
        hero = bot()
        hero.strafe_until = 100
        nearer = {"pos": [0, 30, 0]}
        selected = {"pos": [80, 0, 0]}
        with patch.dict(TUNE, {"duel_target_tracking": 0}):
            move, _, _ = hero.steer(observation(), (0, 0), "duel",
                                    False, [(nearer, 30, 0), (selected, 80, 0)], selected)
        self.assertGreater(move[0], 0.5)
        self.assertLess(move[1], -0.3)

    def test_no_target_falls_back_to_previous_behavior(self):
        hero = bot()
        hero.strafe_until = 100
        nearer = {"pos": [0, 30, 0]}
        with patch.dict(TUNE, {"duel_target_tracking": 1}):
            move, _, _ = hero.steer(observation(), (0, 0), "duel",
                                    False, [(nearer, 30, 0)], None)
        self.assertGreater(move[0], 0.5)


if __name__ == "__main__":
    unittest.main()
