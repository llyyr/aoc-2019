tree = {y: x for x, y in [x.strip().split(')') for x in open('06.in')]}


def calc(x):
    return (calc(tree[x]) if x in tree else []) + [x] # ty stackoverflow


print(sum(len(calc(x)) - 1 for x in tree.keys()))

you, san = calc('YOU'), calc('SAN')
dist = sum(x == y for x, y in zip(you, san)) + 1
print(len(you + san) - you.index(you[dist]) - san.index(san[dist]))
