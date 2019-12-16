from collections import deque, defaultdict


class IntCode(object):
    arity = {
        1: (0, 0, 1),
        2: (0, 0, 1),
        3: (1,),
        4: (0,),
        5: (0, 0),
        6: (0, 0),
        7: (0, 0, 1),
        8: (0, 0, 1),
        9: (0,),
        99: ()
    }

    def __init__(self, puzzle: list):
        self.mem = puzzle
        self.ip = 0
        self.rbase = 0
        self.inp = deque()
        self.out = []

    def interpretOP(self, op):
        modes = []
        o = op % 100
        op //= 100
        while op > 0:
            modes.append(op % 10)
            op //= 10
        return o, modes

    def addInput(self, l):
        self.inp.extend(l)

    def clearOutput(self):
        self.out = []

    def setV(self, offset, v, mode):
        if mode == 0:
            self.mem[self.mem[self.ip + offset]] = v
        elif mode == 2:
            self.mem[self.mem[self.ip + offset] + self.rbase] = v


    def runToBlock(self):
        while self.mem[self.ip] != 99:
            op, modes = self.interpretOP(self.mem[self.ip])
            modes += [0] * (len(self.arity[op]) - len(modes))

            values = []
            for ix, mode in enumerate(modes):
                if mode == 0:
                    values.append(self.mem[self.mem[self.ip+ix+1]])
                elif mode == 2:
                    values.append(self.mem[self.mem[self.ip+ix+1] + self.rbase])
                else:
                    values.append(self.mem[self.ip+ix+1])

            skip_inc = False
            if op == 1:
                self.setV(3, values[0] + values[1], modes[2])
            elif op == 2:
                self.setV(3, values[0] * values[1], modes[2])
            elif op == 3:
                if len(self.inp) == 0:
                    return False
                self.setV(1, self.inp.popleft(), modes[0])
            elif op == 4:
                self.out.append(values[0])
            elif op == 5:
                if values[0] != 0:
                    self.ip = values[1]
                    skip_inc = True
            elif op == 6:
                if values[0] == 0:
                    self.ip = values[1]
                    skip_inc = True
            elif op == 7:
                if values[0] < values[1]:
                    self.setV(3, 1, modes[2])
                else:
                    self.setV(3, 0, modes[2])
            elif op == 8:
                if values[0] == values[1]:
                    self.setV(3, 1, modes[2])
                else:
                    self.setV(3, 0, modes[2])
            elif op == 9:
                self.rbase += values[0]
            if not skip_inc:
                self.ip += len(self.arity[op]) + 1
        return True

   
puzzle = list(map(int, open('15.in').readline().strip().split(",")))

DIRECTIONS = {
    1: (0, 1),
    4: (1, 0),
    2: (0, -1),
    3: (-1, 0), 
}


vm = IntCode(puzzle)
grid = defaultdict(lambda: None)
x, y = 0, 0


BACKWARDS = {1: 2, 2: 1, 3: 4, 4: 3}

def explore(x, y):
    for direction in range(1, 5):
        dx, dy = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        if grid[(nx, ny)] is not None:
            continue

        vm.addInput([direction])
        vm.runToBlock()

        grid[(nx, ny)] = vm.out[-1]
        if vm.out[-1] in (1, 2):
            explore(nx, ny)
            vm.addInput([BACKWARDS[direction]])
            vm.runToBlock()
            assert vm.out[-1] != 0

explore(x, y)

def bfsFlood(startX, startY):
    q = deque([(startX, startY, 0)])
    s = set()
    minToTarget = (float('inf'), 0, 0)
    maxSteps = 0

    while len(q) > 0:
        x, y, step = q.popleft()

        maxSteps = max(maxSteps, step)
        if grid[(x, y)] == 2:
            minToTarget = min(minToTarget, (step, x, y))

        s.add((x, y))
        for direction in range(1, 5):
            dx, dy = DIRECTIONS[direction]
            nx = x + dx
            ny = y + dy

            if (nx, ny) in s or grid[(nx, ny)] is None or grid[(nx, ny)] == 0:
                continue
            else:
                q.append((nx, ny, step+1))

    return minToTarget, maxSteps

part1, tx, ty = bfsFlood(0, 0)[0]
print(part1)

part2 = bfsFlood(tx, ty)[1]
print(part2)
