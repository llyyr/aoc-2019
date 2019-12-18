from collections import defaultdict, namedtuple
from queue import Queue as Q
import heapq as hq

f = open('18.in').read().strip().splitlines()

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
keys = set()
doors = set()
mp = []
key_loc = [0]*27
door_loc = [0]*26


y=0
for line in f:
    x=0
    mp.append(line)
    for c in line:
        if c >= 'a' and c <='z':
            key_loc[ord(c)-ord('a')] = Matrix(x,y)
            keys.add(c)
        if c >= 'A' and c <='Z':
            door_loc[ord(c)-ord('A')] = Matrix(x,y)
            doors.add(c)
        if c == '@':
            start=Matrix(x,y)
        x+=1
    y+=1

dist={}

xsize=len(mp[0])
ysize=len(mp)

SEEN = set()

req_keys = {}
def dfs(cur, doors):
    global mp
    global SEEN
    if cur in SEEN:
        return
    SEEN.add(cur)

    for d in directions:
        p = cur+d
        c = mp[p.y][p.x]
        if c != '#':
            new_doors=set(doors)
            if c >= 'a' and c <= 'z':
                req_keys[c] = doors
            if c >= 'A' and c <= 'Z':
                new_doors.add(chr(ord(c)+ord(' ')))
            dfs(p, new_doors)

dfs(start,set())

req_mask = {}
for k, v in req_keys.items():
    mask = 0
    for c in v:
        mask |= (2**(ord(c)-ord('a')))
    req_mask[ord(k)-ord('a')] = mask

final_mask = (2**len(req_mask))-1

graph = {}


for y in range(ysize):
    for x in range(xsize):
        p = Matrix(x, y)
        c = mp[y][x]
        if c != '#':
            nearby = []
            for d in directions:
                new_pos = p + d
                if new_pos.x >= 0 and new_pos.x < xsize and new_pos.y >= 0 and new_pos.y < ysize:
                    new_cur = mp[new_pos.y][new_pos.x]
                    if new_cur != '#':
                        nearby.append(new_pos)
            graph[p] = nearby


key_dist = defaultdict(lambda :defaultdict(int))
def bfs(graph, start):
    dist = {}
    q = Q()
    q.put(start)
    dist[start] = 0
    while not q.empty():
        current = q.get()
        steps = dist[current]
        for nearby in graph.get(current, []):
            if nearby not in dist:
                dist[nearby] = steps + 1
                q.put(nearby)
    return dist

for c in range(len(req_keys)):
    kdist = bfs(graph, key_loc[c])
    for t in range(len(req_keys)):
        key_dist[c][t] = kdist[key_loc[t]]
    key_dist[c][26] = kdist[start]
    key_dist[26][c] = kdist[start]

key_loc[26] = start

q = []
def put(loc, keys, d):
    global q, dist
    node = (loc, keys)
    if node not in dist or d < dist[node]:
        dist[node] = d
        hq.heappush(q, (d, node))


def part1():
    put(26, 0, 0)
    while q:
        (cur_dist, (cur, keys)) = hq.heappop(q)
        if keys == final_mask:
            print(cur_dist)
            break

        if cur_dist == dist[(cur,keys)]:
            for i in range(len(req_mask)):
                if (req_mask[i] & keys) == req_mask[i]:
                    put(i, keys|(2**i), cur_dist+key_dist[cur][i])

part1()


def part2():
    key_quad = {}
    for i in range(len(req_keys)):
        p = key_loc[i]
        if p.x < start.x and p.y < start.y:
            key_quad[i] = 0
        elif p.x > start.x and p.y < start.y:
            key_quad[i] = 1
        elif p.x < start.x and p.y > start.y:
            key_quad[i] = 2
        elif p.x > start.x and p.y > start.y:
            key_quad[i] = 3
        else:
            assert False

    put((26, 26, 26, 26), 0, 0)
    while q:
        (cur_dist, (cur, keys)) = hq.heappop(q)
        if keys == final_mask:
            print(cur_dist - 8)
            break

        if cur_dist == dist[(cur,keys)]:
            for i in range(len(req_mask)):
                if (req_mask[i] & keys) == req_mask[i]:
                    v = key_quad[i]
                    old_pos = cur[v]
                    new_cur=list(cur)
                    new_cur[v] = i
                    new_cur=tuple(new_cur)
                    new_dist = cur_dist+key_dist[cur[v]][i]
                    put(new_cur, keys|(2**i), cur_dist+key_dist[old_pos][i])

part2()
