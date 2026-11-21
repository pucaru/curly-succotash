"""Selective squad-first targeting: retaliation and finishing are never suppressed."""
import unittest
from bot import TUNE
from test_bot import make_bot, obs

class SelectiveEngageTests(unittest.TestCase):
    def setUp(self):
        self.old = TUNE.get("squad_unprovoked_range", 190.0)
    def tearDown(self):
        TUNE["squad_unprovoked_range"] = self.old
    def make_case(self, range_m=150.0, hp=1400):
        bot = make_bot()
        d=obs(t=10)
        d["mechs"]=[{"kind":"mech","id":7,"pos":[range_m,0,0],
            "vel":[0,0,0],"hp":hp,"max_hp":1400,
            "aim":[3.14,0],"weapons":["gun"]}]
        bot.update(d)
        return bot,d
    def get_target(self,bot,d):
        return bot.enemy(d,bot.threats(d["self"]["pos"],d["t"]))
    def test_default_selects_distant_enemy(self):
        TUNE["squad_unprovoked_range"] = 190
        bot,d=self.make_case()
        self.assertEqual(self.get_target(bot,d)["id"],7)
    def test_close_range_blocks_distant_unprovoked_enemy(self):
        TUNE["squad_unprovoked_range"] = 85
        bot,d=self.make_case()
        self.assertIsNone(self.get_target(bot,d))
        b2,d2=self.make_case(70)
        self.assertEqual(self.get_target(b2,d2)["id"],7)
    def test_attacker_and_weak_enemy_can_still_be_targeted(self):
        TUNE["squad_unprovoked_range"] = 85
        bot,d=self.make_case()
        bot.attacker=7
        bot.attacker_until=18
        self.assertEqual(self.get_target(bot,d)["id"],7)
        bot2,d2=self.make_case(hp=500)
        self.assertEqual(self.get_target(bot2,d2)["id"],7)
    def test_ffa_target_policy_unmodified(self):
        TUNE["squad_unprovoked_range"] = 85
        bot,d=self.make_case(hp=350)
        bot.ffa=True
        self.assertEqual(self.get_target(bot,d)["id"],7)

if __name__ == "__main__":
    unittest.main()
