from collections import defaultdict

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
        self.out = []
        self.gen = self.run()

    def get_pos(self, operand: tuple, modes: int) -> list:
        outs = [None] * 4

        for i, operation in enumerate(operand):
            o = self.mem[self.ip + 1 + i]
            mode = modes % 10
            modes //= 10

            if mode == 2:
                o += self.rbase
            if mode in (0, 2):
                if o >= len(self.mem):
                    self.mem += [0] * (o + 1 - len(self.mem))
                if operation == 0:
                    o = self.mem[o]
            else:
                assert mode == 1, mode

            outs[i] = o
        return outs

    def run(self) -> int:
        while self.mem[self.ip] != 99:
            opcode = self.mem[self.ip] % 100
            modes = self.mem[self.ip] // 100
            operand = self.arity[opcode]

            a, b, c, d = self.get_pos(operand, modes)
            self.ip += len(operand) + 1

            if opcode == 1:
                self.mem[c] = a + b
            elif opcode == 2:
                self.mem[c] = a * b
            elif opcode == 3:
                self.mem[a] = yield self.out
                self.out.clear()
            elif opcode == 4:
                self.out.append(a)
            elif opcode == 7:
                self.mem[c] = 1 if a < b else 0
            elif opcode == 8:
                self.mem[c] = 1 if a == b else 0
            elif opcode == 5:
                if a != 0:
                    self.ip = b
            elif opcode == 6:
                if a == 0:
                    self.ip = b
            elif opcode == 9:
                self.rbase += a
        return self.out

    def run_gen(self, inp):
        return self.gen.send(inp)


puzzle = list(map(int, open('13.in').readline().strip().split(",")))

#part 1
value = defaultdict(int)

def update(output):
    for x, y, t in zip(output[::3], output[1::3], output[2::3]):
        value[(x, y)] = t

try:
    vm = IntCode(puzzle)
    update(vm.run_gen(None))
except StopIteration as e:
    update(e.value)
    print("Part 1:", sum(c == 2 for c in value.values()))

# part 2
puzzle[0] = 2

def play(value):
    for (x, y), v in value.items():
        if v == 4:
            ball = x
        elif v == 3:
            p = x

    if ball > p:
        return 1
    elif ball < p:
        return -1
    else:
        return 0

try:
    vm = IntCode(puzzle)
    update(vm.run_gen(None))
    while True:
        inp = play(value)
        update(vm.run_gen(inp))
except StopIteration as e:
    update(e.value) 
    print("Part 2:", value[(-1, 0)])

