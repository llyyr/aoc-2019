class Matrix(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Matrix(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return other and abs(self.x - other.x) < 1e-5 and abs(self.y - other.y) < 1e-5

    def __hash__(self):
        return hash((self.x, self.y))

directions = [Matrix(0, -1), Matrix(1, 0), Matrix(0, 1), Matrix(-1, 0)]
lines = open('24.in').read().strip().splitlines()

def part1(lines=lines):
    seen = set()
    while True:
        grid = ''.join(lines)
        if grid in seen:
            a, b = 0, 1
            for y in range(5):
                for x in range(5):
                    if lines[y][x] == '#':
                        a += b
                    b *= 2
            print(a)
            break
        seen.add(grid)
        #print('\n'.join(lines), end='\n\n')
        nl = []
        for y in range(5):
            s = ''
            for x in range(5):
                p = Matrix(x, y)
                count = 0
                for d in directions:
                    np = p + d
                    if np.x >= 0 and np.y >= 0 and np.x < 5 and np.y < 5 and lines[np.y][np.x] == '#':
                        count += 1
                if lines[p.y][p.x] == '#':
                    s += '#' if count == 1 else '.'
                else:
                    s += '#' if count == 1 or count == 2 else '.'
            nl.append(s)
        lines = nl
part1()

def part2():
    blank = ['.' * 5] * 5
    lvls = [blank[:], blank[:], lines, blank[:], blank[:]]
    for minutes in range(200):
        new_lvls = [blank[:], blank[:]]
        bugs = 0
        for lvl in range(1, len(lvls)-1):
            nl = []
            for y in range(5):
                s = ''
                for x in range(5):
                    if x==2 and y == 2:
                        s += '.'
                        continue
                    p = Matrix(x,y)
                    count = 0
                    for d in directions:
                        np = p+d
                        if np.x < 0:
                            if lvls[lvl-1][2][1] == '#':
                                count += 1
                        elif np.x >= 5:
                            if lvls[lvl-1][2][3] == '#':
                                count += 1
                        elif np.y < 0:
                            if lvls[lvl-1][1][2] == '#':
                                count += 1
                        elif np.y >= 5:
                            if lvls[lvl-1][3][2] == '#':
                                count += 1
                        elif np.y == 2 and np.x == 2:
                            if x == 1:
                                for ny in range(5):
                                    if lvls[lvl+1][ny][0] == '#':
                                        count += 1
                            elif x == 3:
                                for ny in range(5):
                                    if lvls[lvl+1][ny][4] == '#':
                                        count += 1
                            elif y == 1:
                                for nx in range(5):
                                    if lvls[lvl+1][0][nx] == '#':
                                        count += 1
                            elif y == 3:
                                for nx in range(5):
                                    if lvls[lvl+1][4][nx] == '#':
                                        count += 1
                            else:
                                assert False
                        else:
                            if lvls[lvl][np.y][np.x] == '#':
                                count += 1
                    if lvls[lvl][p.y][p.x] == '#':
                        s += '#' if count == 1 else '.'
                    else:
                        s += '#' if count == 1 or count == 2 else '.'
                bugs += s.count('#')
                nl.append(s)
            new_lvls.append(nl)
        new_lvls.append(blank[:])
        new_lvls.append(blank[:])
        lvls = new_lvls
    print(bugs)

part2()
