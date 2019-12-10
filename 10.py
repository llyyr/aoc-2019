import math

with open('10.in', 'r') as f:
    grid = list(map(str, (l.strip() for l in f)))

rows = len(grid)
columns = len(grid[0])

outs = [0] * 4

for i in range(rows):
    for j in range(columns):
        if grid[i][j] == '.':
            continue

        seen = set()

        for x in range(rows):
            for y in range(columns):
                if grid[x][y] == '#' and (x != i or y != j):
                    dx, dy = x - i, y - j
                    g = abs(math.gcd(dx, dy))
                    dx //= g
                    dy //= g
                    seen.add((-dx, dy))
        if len(seen) > outs[0]:
            outs = [len(seen), i, j, seen]

ans, i, j, seen = outs
print(ans)

targets = []

for (dx, dy) in seen:
    key = math.degrees(math.atan2(dx, dy))
    key -= 360 if key > 90 else 0
    targets.append((key, (dx, dy)))

targets = sorted(targets, reverse=True)
target = targets[199][1]
x = i - target[0]
y = j + target[1]
print(x + y * 100)
