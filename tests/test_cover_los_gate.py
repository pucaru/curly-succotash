"""Check the opt-in factual LOS gate for defensive waypoints."""
import unittest
from bot import Bot, TUNE


class FakeMap:
    def __init__(self, blocks_attackers):
        self.blocks_attackers = blocks_attackers
    def free(self, x, y):
        return True
    def clear(self, x0, y0, x1, y1, inflated=True):
        # Hero -> nearby waypoint is navigable. Threat -> waypoint is
        # either universally exposed or protected by a hard barrier.
        if abs(x0) < 0.001 and abs(y0) < 0.001:
            return True
        return not self.blocks_attackers


def setup(blocks_attackers):
    bot = Bot({"config":{"match":{"mechs":16}}, "slot":0,
               "seed":7,"map":{"dir":"/nonexistent-test-map"}})
    bot.map = FakeMap(blocks_attackers)
    obs = {"t":20,"self":{"pos":[0.0,0.0,0.0],"stats":{"walk_speed":13}},
           "zone":{"center":[0,0],"radius":560,"next_center":[0,0],
                   "next_radius":380,"shrink_end":160}}
    threat = {"id":4,"pos":[42.0,0.0,0.0]}
    return bot, obs, [(threat,42.0,0.0)]


class CoverValidityTests(unittest.TestCase):
    def test_exposed_waypoint_is_rejected_with_gate(self):
        bot, obs, threats = setup(False)
        old = TUNE.get("cover_los_gate")
        try:
            TUNE["cover_los_gate"] = 1
            self.assertIsNone(bot.find_cover(obs, threats))
        finally:
            if old is None: TUNE.pop("cover_los_gate", None)
            else: TUNE["cover_los_gate"] = old

    def test_exposed_waypoint_retained_in_original_control(self):
        bot, obs, threats = setup(False)
        old = TUNE.get("cover_los_gate")
        try:
            TUNE["cover_los_gate"] = 0
            self.assertIsNotNone(bot.find_cover(obs, threats))
        finally:
            if old is None: TUNE.pop("cover_los_gate", None)
            else: TUNE["cover_los_gate"] = old

    def test_barrier_protected_cover_kept_with_gate(self):
        bot, obs, threats = setup(True)
        old = TUNE.get("cover_los_gate")
        try:
            TUNE["cover_los_gate"] = 1
            self.assertIsNotNone(bot.find_cover(obs, threats))
        finally:
            if old is None: TUNE.pop("cover_los_gate", None)
            else: TUNE["cover_los_gate"] = old
