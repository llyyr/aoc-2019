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
        self.gen.send(None)

    def get_pos(self, operand: tuple, modes: int) -> list:
        outs = [0] * 3

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

            a, b, c = self.get_pos(operand, modes)
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


def fillGrid(puzzle, start):
    img = defaultdict(int)
    x, y = 0, 0
    img[(x, y)] = start
    vm = IntCode(puzzle)
    dir = 0
    dir_r = [-1,0,1,0]
    dir_c = [0,1,0,-1]
    while True:
        try:
            color, turn = vm.run_gen(img[(x, y)])
            img[(x, y)] = color
            dir = (dir + turn * 2 - 1) % 4
            x += dir_c[dir]
            y += dir_r[dir]
        except StopIteration:
            return img

puzzle = list(map(int, open('11.in').readline().strip().split(",")))

print("Part 1:", len(fillGrid(puzzle, 0)))

img = fillGrid(puzzle, 1)
min_width, min_height = min(x[0] for x in img.keys()), min(x[1] for x in img.keys())
img = {(x - min_width, y - min_height): v for (x, y), v in img.items()}
width, height = max(x[0] for x in img.keys()) + 1, max(x[1] for x in img.keys()) + 1
image = [[" "] * width for _ in range(height)]

for (x, y), v in img.items():
    if v == 1:
        image[y][x] = "#"

print("Part 2:")
for line in image:
    print("".join(line))