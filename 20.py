from queue import Queue as Q


class Matrix(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Matrix(self.x + other.x, self.y+other.y)

    def __eq__(self, other):
        return other and abs(self.x - other.x) < 1e-5 and abs(self.y - other.y) < 1e-5

    def __hash__(self):
        return hash((self.x, self.y))


directions = [Matrix(0, -1), Matrix(1, 0), Matrix(0, 1), Matrix(-1, 0)]
lines = open('20.in').read().split('\n')
ysize = len(lines) - 4
xsize = len(lines[2]) - 2

g, portals, diff = {}, {}, {}
for y in range(ysize):
    for x in range(xsize):
        if lines[y + 2][x + 2] != '.':
            continue
        p = Matrix(x, y)
        nearby = []
        for d in directions:
            new_pos = p + d
            if new_pos.x + 2 < len(lines[new_pos.y + 2]):
                c = lines[new_pos.y + 2][new_pos.x + 2]
                if c >= 'A' and c <= 'Z':
                    new_pos = p + d + d
                    cc = lines[new_pos.y + 2][new_pos.x + 2]
                    if d.x < 0 or d.y < 0:
                        c, cc = cc, c
                    new_pos = p + d + d + d
                    inner = 0 if new_pos.x < 0 or new_pos.y < 0 or new_pos.x >= xsize or new_pos.y >= ysize else 1
                    i = c + cc
                    if i == 'AA':
                        start = p
                    elif i == 'ZZ':
                        goal = p
                    else:
                        if i not in portals:
                            portals[i] = [None, None]
                        assert portals[i][0 if inner else 1] is None
                        portals[i][0 if inner else 1] = p
            if new_pos.x >= 0 and new_pos.y >= 0 and new_pos.x < xsize and new_pos.y < ysize and lines[new_pos.y + 2][new_pos.x + 2] == '.':
                nearby.append(new_pos)
        g[p] = nearby

for _, pos in portals.items():
    diff[(pos[0], pos[1])] = 1
    diff[(pos[1], pos[0])] = -1
    g[pos[0]].append(pos[1])
    g[pos[1]].append(pos[0])


dist = {}
q = Q()
q.put(start)
dist[start] = 0
while not q.empty():
    cur = q.get()
    steps = dist[cur]
    for nearby in g.get(cur, []):
        if nearby not in dist:
            dist[nearby] = steps + 1
            q.put(nearby)
print(dist[goal])


dist = {}
q = Q()
q.put((start, 0))
dist[(start, 0)] = 0
while not q.empty():
    (cur, lvl) = q.get()
    steps = dist[(cur, lvl)]
    if cur == goal and lvl == 0:
        print(steps)
        break
    for nearby in g.get(cur, []):
        new_lvl = lvl
        if (cur, nearby) in diff:
            new_lvl = lvl + diff[(cur, nearby)]
        if new_lvl >= 0:
            new_pos = (nearby, new_lvl)
            if new_pos not in dist:
                dist[new_pos] = steps + 1
                q.put(new_pos)

