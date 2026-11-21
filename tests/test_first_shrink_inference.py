"""Regression checks for first-zone-phase-based FFA classification."""
import unittest
from unittest.mock import patch
from bot import Bot, TUNE


def fresh_bot():
    return Bot({"config": {"match": {"mechs": 16}},
                "slot": 0, "seed": 42, "map": {"dir": "/nonexistent-zone-test"}})


def obs(t, alive, shrink_start):
    return {"t": t, "alive": alive, "self": {"pos": [0, 0, 0]},
            "zone": {"shrink_start": shrink_start},
            "mechs": [], "events": [], "pickups": [], "crates": [],
            "cubes": [], "sounds": []}


class FirstShrinkClassification(unittest.TestCase):
    def test_default_preserves_baseline_late_flip(self):
        with patch.dict(TUNE, {"pre_shrink_ffa_only": 0}):
            b = fresh_bot()
            b.update(obs(0, 16, 70))
            b.update(obs(91, 14, 180))
            self.assertTrue(b.ffa)

    def test_strict_excludes_two_deaths_after_first_shrink(self):
        with patch.dict(TUNE, {"pre_shrink_ffa_only": 1}):
            b = fresh_bot()
            b.update(obs(0, 16, 70))
            b.update(obs(91, 14, 180))
            self.assertEqual(b.first_shrink, 70)
            self.assertFalse(b.ffa)

    def test_strict_still_detects_early_ffa(self):
        with patch.dict(TUNE, {"pre_shrink_ffa_only": 1}):
            b = fresh_bot()
            b.update(obs(0, 16, 70))
            b.update(obs(30, 15, 70))
            self.assertTrue(b.ffa)

    def test_strict_detects_two_pre_shrink_deaths(self):
        with patch.dict(TUNE, {"pre_shrink_ffa_only": 1}):
            b = fresh_bot()
            b.update(obs(0, 16, 70))
            b.update(obs(58, 14, 70))
            self.assertTrue(b.ffa)


if __name__ == "__main__":
    unittest.main()
