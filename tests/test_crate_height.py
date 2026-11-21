"""Crate impact height must differ from humanoid target height."""
import math
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class CrateHeightTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("crate_target_height", 4.5)
    def tearDown(self):
        TUNE["crate_target_height"] = self.old
    def test_actual_crate_observation_aims_at_configured_height(self):
        for h in (1.4,2.0,4.5):
            with self.subTest(h=h):
                TUNE["crate_target_height"] = h
                bot=make_bot()
                d=obs(t=8)
                d["crates"]=[{"id":1004,"pos":[40.0,0.0,0.0],"hp":300}]
                a={}
                bot.aim_and_fire(d,None,"scout",[],a)
                self.assertAlmostEqual(a["aim"][0],0.0,places=4)
                expected=math.atan2(h-7.0,40.0)
                self.assertAlmostEqual(a["aim"][1],expected,places=3)
    def test_mech_target_keeps_original_center_height(self):
        TUNE["crate_target_height"]=1.4
        bot=make_bot()
        d=obs(t=8)
        e={"kind":"mech","id":7,"pos":[40.0,0.0,0.0],
           "vel":[0.0,0.0,0.0],"hp":1400,"max_hp":1400,
           "aim":[3.14,0.0],"weapons":["gun"],"charging":False}
        a={}
        bot.aim_and_fire(d,e,"duel",[],a)
        self.assertAlmostEqual(a["aim"][1],math.atan2(4.5-7.0,40.0),places=3)

if __name__ == "__main__":
    unittest.main()
