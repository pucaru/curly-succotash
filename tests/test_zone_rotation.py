"""The experimental rotation guard should be opt-in and deterministic."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs


class RotationTests(unittest.TestCase):
    def test_buffer_makes_distant_zone_rotation_urgent(self):
        datum = obs(t=88)
        datum["zone"]["next_center"] = [210, 0]
        datum["zone"]["next_radius"] = 100
        original = TUNE.get("zone_rotation_buffer", None)
        try:
            TUNE["zone_rotation_buffer"] = 0
            base = make_bot()
            _, base_mode, base_urgent = base.choose_goal(datum, [], None)
            self.assertFalse(base_urgent)
            self.assertNotEqual(base_mode, "zone")

            TUNE["zone_rotation_buffer"] = 45
            candidate = make_bot()
            goal, cand_mode, cand_urgent = candidate.choose_goal(datum, [], None)
            self.assertTrue(cand_urgent)
            self.assertEqual(cand_mode, "zone")
            self.assertEqual(goal, (210, 0))
        finally:
            if original is None:
                TUNE.pop("zone_rotation_buffer", None)
            else:
                TUNE["zone_rotation_buffer"] = original


if __name__ == "__main__":
    unittest.main()
