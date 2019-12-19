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
        self.mem = puzzle + [0] * 10000
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

   
puzzle = list(map(int, open('19.in').readline().strip().split(",")))


def check(x, y, p=puzzle):
    vm = IntCode(p)
    vm.addInput([x, y])
    vm.runToBlock()
    return vm.out[0]


total = 0
for y in range(50):
    for x in range(50):
        total += check(x, y)
print(total)


y = 99
x = 0
while True:
    while check(x, y) == 0:
        x += 1
    if check(x + 99, y - 99) == 1:
        print(x*10000 + y-99)
        break
    y += 1
