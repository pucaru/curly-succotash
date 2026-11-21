"""Deterministic tests for cover validity and opt-in fire preservation."""
import unittest
from bot import Bot, TUNE


class Geometry:
    def __init__(self, blocked):
        self.blocked = blocked
    def free(self, x, y):
        return True
    def clear(self, x0, y0, x1, y1, inflated=True):
        return True if abs(x0) < 0.001 and abs(y0) < 0.001 else not self.blocked


def make_bot(blocked):
    bot = Bot({"slot":0,"seed":1,"map":{"dir":"/absent-map-for-test"},
               "config":{"match":{"mechs":16},"loot":{"pickup_radius":4}}})
    bot.map = Geometry(blocked)
    return bot


def observation():
    return {"t":20.0,"tick":201,"alive":16,
            "self":{"pos":[0.0,0.0,0.0],"energy":100,"grounded":True,
                    "weapons":[{"kind":"gun","ammo":12},None],
                    "hp":500.0,"max_hp":1400.0,"cubes":0,
                    "stats":{"walk_speed":13}},
            "zone":{"center":[0,0],"radius":560,"next_center":[0,0],
                    "next_radius":380,"shrink_end":160},
            "mechs":[],"events":[],"pickups":[],"offer":None}


class CoverFireTests(unittest.TestCase):
    def test_exposed_waypoint_classified_false_but_still_reachable(self):
        bot=make_bot(False)
        tr={"id":4,"pos":[42.0,0.0,0.0]}
        cover=bot.find_cover(observation(),[(tr,42.0,0.0)])
        self.assertIsNotNone(cover)
        self.assertFalse(bot.cover_is_real)

    def test_blocked_enemy_sightline_classified_genuine(self):
        bot=make_bot(True)
        tr={"id":4,"pos":[42.0,0.0,0.0]}
        cover=bot.find_cover(observation(),[(tr,42.0,0.0)])
        self.assertIsNotNone(cover)
        self.assertTrue(bot.cover_is_real)

    def test_opt_in_preserves_fire_only_for_fake_cover(self):
        bot=make_bot(False)
        target={"id":4,"pos":[80.0,0.0,0.0],"hp":1400.0}
        bot.update=lambda obs:None
        bot.threats=lambda p,t:[(target,80.0,0.0)]
        bot.enemy=lambda obs,threats:target
        bot.choose_goal=lambda obs,threats,target:((8.0,0.0),"cover",False)
        bot.steer=lambda obs,goal,mode,urgent,threats:([0.0,0.0],False,False)
        bot.dodge=lambda obs,move:move
        bot.aim_and_fire=lambda obs,target,mode,threats,a:a.update({"fire":[True,True]})
        bot.cover_is_real=False
        old=TUNE.get("cover_fire_gate")
        try:
            TUNE["cover_fire_gate"]=0
            self.assertEqual(bot.act(observation())["fire"],[False,False])
            TUNE["cover_fire_gate"]=1
            self.assertEqual(bot.act(observation())["fire"],[True,True])
            bot.cover_is_real=True
            self.assertEqual(bot.act(observation())["fire"],[False,False])
        finally:
            if old is None:TUNE.pop("cover_fire_gate",None)
            else:TUNE["cover_fire_gate"]=old
