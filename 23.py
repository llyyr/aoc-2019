from collections import *
from more_itertools import sliced


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

    def __init__(self, prog):
        self.prog = prog.copy()
        self.memory = {}
        self.ip = 0
        self.rbase = 0
        self.await_inp = False
        self.halted = False

    def run(self, inp, out):
        assert not self.halted, 'called run when halted'
        if self.await_inp:
            assert len(inp) > 0, 'called run with empty inp awaiting inp'
        
        def getmem(i):
            assert i >= 0, f'invalid address {i} for getmem'
            if i in self.memory:
                return self.memory[i]
            if i < len(self.prog):
                return self.prog[i]
            return 0

        def setmem(i, v):
            assert i >= 0, f'invalid address {i} for setmem'
            self.memory[i] = v

        def getp(i):
            assert i < len(self.arity[opcode]), f'i={i} >= arity={len(self.arity[opcode])}'
            p = getmem(self.ip+i)
            mode = modes[i]
            assert mode == 0 or mode == 1 or mode == 2, f'unknown mode={mode} for getp'
            if mode == 0:
                return getmem(p)
            if mode == 1:
                return p
            if mode == 2:
                return getmem(self.rbase + p)

        def setp(i, v):
            assert i < len(self.arity[opcode]), f'i={i} >= arity={len(self.arity[opcode])}'
            mode = modes[i]
            p = getmem(self.ip+i)
            assert mode == 0 or mode == 2, f'unknown mode={mode} for setp'
            if mode == 0:
                setmem(p, v)
                return
            if mode == 2:
                setmem(self.rbase + p, v)
                return

        def adv():
            self.ip += len(self.arity[opcode])

        while True:
            modes = [0] * 3
            modes_int, opcode = divmod(getmem(self.ip), 100)
            modes_int, modes[0] = divmod(modes_int, 10)
            modes_int, modes[1] = divmod(modes_int, 10)
            modes_int, modes[2] = divmod(modes_int, 10)
            
            assert modes_int == 0, f'modes_int={modes_int} unexpectedly non-zero'
            assert opcode in self.arity, f'unknown opcode {opcode}'

            self.ip += 1
            if opcode == 1:
                setp(2, getp(0) + getp(1))
                adv()
            elif opcode == 2:
                setp(2, getp(0) * getp(1))
                adv()
            elif opcode == 3:
                if len(inp) == 0:
                    self.await_inp = True
                    self.ip -= 1
                    return
                self.await_inp = False
                v = inp.pop(0)
                setp(0, v)
                adv()
            elif opcode == 4:
                v = getp(0)
                out.append(v)
                adv()
            elif opcode == 5:
                if getp(0) != 0:
                    self.ip = getp(1)
                else:
                    adv()
            elif opcode == 6:
                if getp(0) == 0:
                    self.ip = getp(1)
                else:
                    adv()
            elif opcode == 7:
                setp(2, int(getp(0) < getp(1)))
                adv()
            elif opcode == 8:
                setp(2, int(getp(0) == getp(1)))
                adv()
            elif opcode == 9:
                self.rbase += getp(0)
                adv()
            else:
                assert opcode == 99, opcode
                self.halted = True
                return


program = list(map(int, (open('23.in').readline().strip().split(','))))
queues = defaultdict(list)
int_count = 50
vms = list(IntCode(program) for _ in range(int_count))
inps = list([i] for i in range(int_count))
outs = list([] for _ in range(int_count))

nat = None
last_nat = None

for i, x in enumerate(vms):
    x.run(inps[i], outs[i])

while True:
    for out in outs:
        for dest, x, y in sliced(out, 3):
            queues[dest].append((x, y))
        out.clear()

    idle = True
    for i, x in enumerate(vms):
        if not x.await_inp:
            continue
        queue = queues[i]
        if queue:
            for a, b in queue:
                inps[i].append(a)
                inps[i].append(b)
            queue.clear()
            idle = False
        else:
            inps[i].append(-1)
        x.run(inps[i], outs[i])

    for out in outs:
        if len(out) > 0:
            idle = False

    if queues[255]:
        nat = queues[255][-1]
        print(f'setting nat packet to {nat}')
        queues[255].clear()

    if idle:
        print(f'is idle, nat packet is {nat}')
        assert nat is not None, 'nat is none'
        queues[0].append(nat)
        if nat == last_nat:
            break
        last_nat = nat

