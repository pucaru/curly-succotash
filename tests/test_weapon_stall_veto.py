"""Time-box a non-progressing weapon pursuit without changing ordinary looting."""
import unittest
from unittest.mock import patch
from bot import TUNE
from test_bot import make_bot, obs

class WeaponPursuitTests(unittest.TestCase):
    def situation(self, t=1, x=0):
        data = obs(t=t)
        data["self"]["pos"][0] = x
        data["pickups"] = [{"id": 8111, "kind": "laser", "pos": [120, 0, 0]}]
        return data

    def test_control_never_bans_unreachable_laser(self):
        b = make_bot()
        with patch.dict(TUNE, {"weapon_stall_veto": 0}):
            b.act(self.situation(1))
            b.act(self.situation(10))
        self.assertNotIn(8111, b.bad_pickups)

    def test_candidate_bans_laser_after_eight_seconds_without_progress(self):
        b = make_bot()
        with patch.dict(TUNE, {"weapon_stall_veto": 1}):
            b.act(self.situation(1))
            b.act(self.situation(4))
            b.act(self.situation(10))
        self.assertIn(8111, b.bad_pickups)
        self.assertGreaterEqual(b.bad_pickups[8111], 34)

    def test_candidate_keeps_reachable_laser_when_making_progress(self):
        b = make_bot()
        with patch.dict(TUNE, {"weapon_stall_veto": 1}):
            b.act(self.situation(1, 0))
            b.act(self.situation(4, 22))
            b.act(self.situation(10, 45))
        self.assertNotIn(8111, b.bad_pickups)

    def test_expiry_allows_retry(self):
        b = make_bot()
        with patch.dict(TUNE, {"weapon_stall_veto": 1}):
            b.act(self.situation(1))
            b.act(self.situation(10))
            self.assertIn(8111, b.bad_pickups)
            b.act(self.situation(36))
        self.assertNotIn(8111, b.bad_pickups)

if __name__ == "__main__":
    unittest.main()
