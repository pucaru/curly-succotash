"""Controlled checks for damage-triggered movement and laser restraint."""
import unittest
from unittest.mock import patch

from bot import TUNE
from test_bot import make_bot, obs


def enemy():
    return {"kind": "mech", "id": 7, "pos": [65, 0, 0],
            "vel": [0, 0, 0], "hp": 1400, "max_hp": 1400,
            "aim": [3.14159, 0], "weapons": ["gun"], "charging": False}


class UnderFireTests(unittest.TestCase):
    def test_evasive_boost_only_with_option_enabled(self):
        data = obs(t=20)
        data["self"]["hp"] = 1200
        data["self"]["energy"] = 90
        data["mechs"] = [enemy()]
        data["events"] = [{"type": "damaged", "amount": 60,
                           "weapon": "gun", "bearing": 0.0, "by": 7}]
        with patch.dict(TUNE, {"panic_boost": False}):
            original = make_bot().act(data)
        with patch.dict(TUNE, {"panic_boost": True}):
            experimental = make_bot().act(data)
        self.assertFalse(original["boost"])
        self.assertTrue(experimental["boost"])
        self.assertEqual(original["move"], experimental["move"])

    def test_retreat_laser_charge_is_optional(self):
        data = obs(t=25, with_laser=True)
        data["self"]["hp"] = 850
        data["self"]["weapons"][1]["charge"] = 0.2
        tr = enemy()
        tr["pos"] = [40, 0, 0]
        with patch.dict(TUNE, {"escape_no_laser_charge": False}):
            a = {}
            make_bot().aim_and_fire(data, tr, "flee", [], a)
        with patch.dict(TUNE, {"escape_no_laser_charge": True}):
            b = {}
            make_bot().aim_and_fire(data, tr, "flee", [], b)
        self.assertTrue(a["fire"][1])
        self.assertFalse(b["fire"][1])
        self.assertEqual(a["fire"][0], b["fire"][0])


if __name__ == "__main__":
    unittest.main()
