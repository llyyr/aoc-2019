from itertools import permutations


with open("7.in", "r") as f:
    a = list(map(int, f.read().split(',')))


def wtffff(a, iPos, num, jump=False):
    n = 2 if jump else 3
    while n > len(num):
        num = [0]+num
    if not jump:
        num[0] = 1
    return [x if num[len(num) - 1 - i] == 1 else a[x] for i, x in enumerate(a[iPos+1:iPos+n+1])]


def intcode(inputs, iPos=0):
    while True:
        num = [int(x) for x in str(a[iPos])]
        opcode = (0 if len(num) == 1 else num[-2]) * 10 + num[-1]
        num = num[:-2]
        if opcode in [1, 2, 7, 8]:
            i1, i2, i3 = wtffff(a, iPos, num)
            iPos += 4
            if opcode == 1:
                a[i3] = i1 + i2
            elif opcode == 2:
                a[i3] = i1 * i2
            elif opcode == 7:
                a[i3] = 1 if i1 < i2 else 0
            elif opcode == 8:
                a[i3] = 1 if i1 == i2 else 0
        elif opcode in [5, 6]:
            i1, i2 = wtffff(a, iPos, num, True)
            if opcode == 5:
                if i1 != 0:
                    iPos = i2
                else:
                    iPos += 3
            elif opcode == 6:
                if i1 == 0:
                    iPos = i2
                else:
                    iPos += 3
        elif opcode in [3, 4]:
            i1 = a[iPos+1]
            iPos += 2
            if opcode == 3:
                a[i1] = inputs[0]
                inputs.pop(0)
            elif opcode == 4:
                return a[i1], iPos
        else:
            return None, iPos


def run(a, b):
    out = 0
    for perm in permutations(range(a, b)):
        oldVal = 0
        iPos = [0 for _ in range(len(perm))]
        newVal = iPos[:]
        Q = [[perm[i]] for i in range(len(perm))]
        Q[0].append(0)
        halt = False
        while not halt:
            for i in range(len(perm)):
                oldVal, iPos[i] = intcode(Q[i], iPos[i])
                Q[(i+1) % len(Q)].append(oldVal)
                if oldVal == None:
                    if newVal[-1] > out:
                        out = newVal[-1]
                    halt = True
                    break
                else:
                    newVal[i] = oldVal
    return out


print("Part 1: {}".format(run(0, 5)))
print("Part 2: {}".format(run(5, 10)))
