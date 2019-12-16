f = list(map(int, (open('16.in').read().strip())))
pat = [0, 1, 0, -1]

patterns = []
for i in range(len(f)):
    pattern = []
    patindex = 0
    while len(pattern) <= len(f):
        num_copies = min(i + 1, len(f) - len(pattern) + 1)
        copies = [pat[patindex]] * num_copies
        pattern.extend(copies)
        patindex += 1
        patindex %= len(pat)
    pattern.pop(0)
    patterns.append(pattern)


data = f[:]
for i in range(100):
    output = []
    for i in range(len(data)):
        value = [x * y for x, y in zip(data, patterns[i])]
        value = sum(value)
        value = int(str(value)[-1])
        output.append(value)
    assert len(data) == len(output)
    data = output
print('Part 1:', ''.join(map(str, data[:8])))


#part 2 fuck
offset = int(''.join(map(str, f[:7])))
data = (f*10000)[offset:]  # ignore all before the offset
for i in range(100):
    rev_partial_sum = data[-1:]
    for i in data[-2::-1]:
        rev_partial_sum.append(rev_partial_sum[-1]+i)
    data = list(map(abs, (x%10 for x in reversed(rev_partial_sum))))
print('Part 2:', ''.join(map(str, data[:8])))

