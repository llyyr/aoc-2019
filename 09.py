class IntCode:
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

    def __init__(self, puzzle: list, inp: list):
        self.mem = puzzle
        self.inp = inp
        self.ip = 0
        self.rbase = 0
        self.out = 0

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
                self.mem[a] = self.inp[0]
                self.inp.pop(0)
            elif opcode == 4:
                self.out = a
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


with open('09.in', 'r') as f:
    puzzle = list(map(int, f.readline().strip().split(',')))
    print("Part 1: ", IntCode(puzzle, [1]).run())
    print("Part 2: ", IntCode(puzzle, [2]).run())
