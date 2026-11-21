"""Stealth opening must not disable defensive fire at real enemies."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class QuietFarmingTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("quiet_farm_until", 0.0)
    def tearDown(self):
        TUNE["quiet_farm_until"] = self.old
    def scenario(self, t=10):
        bot = make_bot()
        d = obs(t=t)
        d["crates"] = [{"id":1003,"pos":[40.0,0.0,0.0],"hp":300}]
        return bot, d
    def test_early_silent_opening_skips_crate_aim(self):
        TUNE["quiet_farm_until"] = 60.0
        bot, d = self.scenario()
        a={}
        bot.aim_and_fire(d,None,"scout",[],a)
        self.assertAlmostEqual(a["aim"][0],0.32,places=3)
        self.assertNotIn("fire",a)
    def test_default_farms_crates_as_before(self):
        TUNE["quiet_farm_until"] = 0.0
        bot, d = self.scenario()
        a={}
        bot.aim_and_fire(d,None,"scout",[],a)
        self.assertAlmostEqual(a["aim"][0],0.0,places=3)
        self.assertEqual(len(a["fire"]),2)
    def test_ffa_detected_or_recent_hit_allows_farming(self):
        TUNE["quiet_farm_until"] = 135.0
        bot, d = self.scenario()
        bot.ffa = True
        a={}
        bot.aim_and_fire(d,None,"scout",[],a)
        self.assertAlmostEqual(a["aim"][0],0.0,places=3)
        bot2, d2 = self.scenario()
        bot2.last_hit = 8.0
        a2={}
        bot2.aim_and_fire(d2,None,"scout",[],a2)
        self.assertAlmostEqual(a2["aim"][0],0.0,places=3)

if __name__ == "__main__":
    unittest.main()
