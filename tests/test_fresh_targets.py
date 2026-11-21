"""Target memory regression tests: evasive tracks survive longer than firing locks."""
import unittest
from unittest.mock import patch

import bot


class TargetMemoryTests(unittest.TestCase):
    def setUp(self):
        self.agent = object.__new__(bot.Bot)
        self.agent.ffa = False
        self.agent.attacker = None
        self.agent.attacker_until = -100.0
        self.agent.last_enemy_id = None
        self.agent.target_last = -100.0
        self.target = {
            "id": 7, "pos": [50.0, 0.0, 0.0], "hp": 1000,
            "max_hp": 1400, "seen": 0.0,
        }
        self.obs = {"t": 10.0, "self": {"hp": 1400, "max_hp": 1400}}

    def test_stale_enemy_not_selected_under_short_lock(self):
        with patch.dict(bot.TUNE, {"target_memory_s": 0.8}):
            self.assertIsNone(self.agent.enemy(self.obs, [(self.target, 50.0, 1.2)]))

    def test_fresh_enemy_is_still_selected(self):
        with patch.dict(bot.TUNE, {"target_memory_s": 0.8}):
            self.assertEqual(self.agent.enemy(self.obs, [(self.target, 50.0, 0.2)]), self.target)

    def test_current_baseline_preserves_previous_target_window(self):
        with patch.dict(bot.TUNE, {"target_memory_s": 5.2}):
            self.assertEqual(self.agent.enemy(self.obs, [(self.target, 50.0, 4.5)]), self.target)

    def test_stale_track_still_available_for_evasion(self):
        self.agent.tracks = {7: self.target}
        self.assertEqual(len(self.agent.threats((0.0, 0.0), 6.0)), 1)


if __name__ == "__main__":
    unittest.main()
