"""Terrain-aware, bounded-cost navigation for the Builders Mech Royale arena."""
from array import array
import heapq
import json
import math
import os
import sys

CELL = 4.0
DIRS = ((1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
        (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142))


class Arena:
    def __init__(self, directory):
        with open(os.path.join(directory, "v2", "world.json"), encoding="utf-8") as f:
            world = json.load(f)
        ter = world["terrain"]
        self.tx, self.ty = float(ter["minX"]), float(ter["minY"])
        self.tnx, self.tny = int(ter["nx"]), int(ter["ny"])
        self.ts = float(ter["step"])
        self.nx = max(1, math.ceil((self.tnx - 1) * self.ts / CELL) + 1)
        self.ny = max(1, math.ceil((self.tny - 1) * self.ts / CELL) + 1)
        self.n = self.nx * self.ny
        self.heights = array("h")
        with open(os.path.join(directory, "v2", ter["file"]), "rb") as f:
            self.heights.frombytes(f.read())
        if sys.byteorder == "big":
            self.heights.byteswap()
        if len(self.heights) < self.tnx * self.tny:
            raise ValueError("truncated arena terrain")
        self.raw = bytearray(self.n)
        for prism in world.get("prisms", []):
            ring = prism.get("ring", [])
            if len(ring) < 6:
                continue
            x = sum(ring[0::2]) / (len(ring) // 2)
            y = sum(ring[1::2]) / (len(ring) // 2)
            ground = self.ground(x, y)
            # Bridges high enough to walk beneath are not ground-level barriers.
            if prism.get("base", ground) > ground + 9.6:
                continue
            if prism.get("top", ground) < ground + 1.3:
                continue
            self.fill_ring(ring, 1)
            for hole in prism.get("holes", []) or []:
                self.fill_ring(hole, 0)
        # Inflate footprints to protect the 2.5 m mech cylinder from walls.
        self.blocked = bytearray(self.raw)
        for j in range(1, self.ny - 1):
            row = j * self.nx
            for i in range(1, self.nx - 1):
                idx = row + i
                if self.raw[idx]:
                    for dj in (-1, 0, 1):
                        ofs = idx + dj * self.nx
                        self.blocked[ofs - 1:ofs + 2] = b"\x01\x01\x01"
        self.alt = [self.ground(self.x(i), self.y(j))
                    for j in range(self.ny) for i in range(self.nx)]

    def fill_ring(self, flat, value):
        pts = list(zip(flat[0::2], flat[1::2]))
        if len(pts) < 3:
            return
        low = max(0, int((min(y for _, y in pts) - self.ty) / CELL) - 1)
        high = min(self.ny - 1, int((max(y for _, y in pts) - self.ty) / CELL) + 1)
        for j in range(low, high + 1):
            py = self.ty + j * CELL
            hits = []
            ax, ay = pts[-1]
            for bx, by in pts:
                if (ay <= py < by) or (by <= py < ay):
                    hits.append(ax + (py - ay) * (bx - ax) / (by - ay))
                ax, ay = bx, by
            hits.sort()
            for k in range(0, len(hits) - 1, 2):
                lo = max(0, math.ceil((hits[k] - self.tx) / CELL))
                hi = min(self.nx, math.floor((hits[k + 1] - self.tx) / CELL) + 1)
                if hi > lo:
                    a = j * self.nx + lo
                    self.raw[a:a + hi - lo] = bytes((value,)) * (hi - lo)

    def ground(self, x, y):
        fx = max(0.0, min(self.tnx - 1.001, (x - self.tx) / self.ts))
        fy = max(0.0, min(self.tny - 1.001, (y - self.ty) / self.ts))
        i, j = int(fx), int(fy)
        u, v = fx - i, fy - j
        a = j * self.tnx + i
        z = self.heights
        return 0.01 * ((1 - v) * ((1 - u) * z[a] + u * z[a + 1]) +
                       v * ((1 - u) * z[a + self.tnx] + u * z[a + self.tnx + 1]))

    def x(self, i):
        return self.tx + CELL * i

    def y(self, j):
        return self.ty + CELL * j

    def idx(self, x, y):
        i, j = round((x - self.tx) / CELL), round((y - self.ty) / CELL)
        return j * self.nx + i if 1 <= i < self.nx - 1 and 1 <= j < self.ny - 1 else -1

    def pos(self, idx):
        return self.x(idx % self.nx), self.y(idx // self.nx)

    def free(self, x, y):
        i = self.idx(x, y)
        return i >= 0 and not self.blocked[i]

    def nearest(self, x, y):
        i = self.idx(x, y)
        if i >= 0 and not self.blocked[i]:
            return i
        ii = max(1, min(self.nx - 2, round((x - self.tx) / CELL)))
        jj = max(1, min(self.ny - 2, round((y - self.ty) / CELL)))
        for rad in range(1, 17):
            best, bestd = -1, float("inf")
            for dj in range(-rad, rad + 1):
                for di in (-rad, rad):
                    a, b = ii + di, jj + dj
                    if 1 <= a < self.nx - 1 and 1 <= b < self.ny - 1:
                        k = b * self.nx + a
                        if not self.blocked[k]:
                            d = (self.x(a) - x) ** 2 + (self.y(b) - y) ** 2
                            if d < bestd:
                                best, bestd = k, d
            for di in range(-rad + 1, rad):
                for dj in (-rad, rad):
                    a, b = ii + di, jj + dj
                    if 1 <= a < self.nx - 1 and 1 <= b < self.ny - 1:
                        k = b * self.nx + a
                        if not self.blocked[k]:
                            d = (self.x(a) - x) ** 2 + (self.y(b) - y) ** 2
                            if d < bestd:
                                best, bestd = k, d
            if best >= 0:
                return best
        return -1

    def clear(self, x0, y0, x1, y1, inflated=True):
        dist = math.hypot(x1 - x0, y1 - y0)
        count = max(1, math.ceil(dist / (CELL * 0.75)))
        obs = self.blocked if inflated else self.raw
        # Do not reject a route because the initial point is near a wall.
        for k in range(1, count + 1):
            f = k / count
            at = self.idx(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)
            if at < 0 or obs[at]:
                return False
        return True

    def walk_score(self, x, y, angle, distance=16):
        ux, uy = math.cos(angle), math.sin(angle)
        for step in (4, 8, 12, 16, 22):
            if step > distance:
                break
            if not self.free(x + step * ux, y + step * uy):
                return step - 3
        return distance


class Navigator:
    """Incremental A*: no single decision blocks the 50 ms response budget."""

    def __init__(self, arena):
        self.arena = arena
        self.goal = None
        self.start = None
        self.open = []
        self.g = {}
        self.parent = {}
        self.best = -1
        self.best_h = float("inf")
        self.path = []
        self.finished = False
        self.created = -1.0

    def route(self, x, y, gx, gy, t, steps=225):
        m = self.arena
        if m.clear(x, y, gx, gy):
            return gx, gy
        start, goal = m.nearest(x, y), m.nearest(gx, gy)
        if start < 0 or goal < 0:
            return gx, gy
        if self.goal != goal or t - self.created > 5 or (self.start is not None and
                                                        math.hypot(x - m.pos(self.start)[0],
                                                                   y - m.pos(self.start)[1]) > 42):
            self.goal, self.start, self.created = goal, start, t
            self.open = [(0, start)]
            self.g = {start: 0.0}
            self.parent = {start: -1}
            self.best = start
            self.best_h = self.heuristic(start)
            self.path = []
            self.finished = False
        if not self.finished:
            self.expand(steps)
        endpoint = goal if self.finished else self.best
        if endpoint < 0 or endpoint not in self.parent:
            return gx, gy
        path = []
        u = endpoint
        while u >= 0 and len(path) < m.n:
            path.append(u)
            u = self.parent.get(u, -1)
        path.reverse()
        # String pull: take the farthest currently accessible step ahead.
        for u in reversed(path[1:]):
            px, py = m.pos(u)
            if math.hypot(px - x, py - y) > 48:
                continue
            if m.clear(x, y, px, py):
                return px, py
        return m.pos(path[min(1, len(path) - 1)])

    def heuristic(self, node):
        m = self.arena
        i, j = node % m.nx, node // m.nx
        gi, gj = self.goal % m.nx, self.goal // m.nx
        dx, dy = abs(i - gi), abs(j - gj)
        return CELL * (max(dx, dy) + 0.4142 * min(dx, dy))

    def expand(self, budget):
        m = self.arena
        for _ in range(budget):
            if not self.open:
                self.finished = True
                return
            f, u = heapq.heappop(self.open)
            h = self.heuristic(u)
            if f > self.g.get(u, float("inf")) + h + 0.01:
                continue
            if h < self.best_h:
                self.best, self.best_h = u, h
            if u == self.goal:
                self.finished = True
                self.best = u
                return
            ui, uj = u % m.nx, u // m.nx
            for di, dj, mult in DIRS:
                ni, nj = ui + di, uj + dj
                if ni < 1 or ni >= m.nx - 1 or nj < 1 or nj >= m.ny - 1:
                    continue
                v = nj * m.nx + ni
                if m.blocked[v] or abs(m.alt[v] - m.alt[u]) > 4.5:
                    continue
                if di and dj and (m.blocked[u + di] or m.blocked[u + dj * m.nx]):
                    continue
                ng = self.g[u] + CELL * mult
                if ng + 0.001 < self.g.get(v, float("inf")):
                    self.g[v] = ng
                    self.parent[v] = u
                    heapq.heappush(self.open, (ng + self.heuristic(v), v))
