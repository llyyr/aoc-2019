recipes = {}


def parse_helper(x):
    idx = x.find(' ')
    return (int(x[:idx]), x[idx+1:])

for line in open('14.in').read().strip().split('\n'):
    inp, out = line.split(' => ')
    inp = inp.split(', ')
    inp = list(map(tuple, (parse_helper(inpx) for inpx in inp)))
    out = parse_helper(out)
    recipes[out[1]] = (inp, out)

def get_cost(nfuel):
    cost = {}
    cost['FUEL'] = nfuel

    while any(cost[key] > 0 and key != "ORE" for key in cost):
        x = list(map(str, (k for k in cost if cost[k] > 0 and k != 'ORE')))
        x = x[0]
        outq = recipes[x][1][0]
        qq = -(cost[x] // -outq)
        cost[x] -= outq*qq
        for inp in recipes[x][0]:
            if inp[1] in cost:
                cost[inp[1]] += inp[0]*qq
            else:
                cost[inp[1]] = inp[0]*qq
    return cost['ORE']
print(get_cost(1))

lo = 0
hi = int(1e12)
while lo < hi:
    mid = (lo+hi+1) // 2
    if get_cost(mid) <= int(1e12):
        lo = mid
    else:
        hi = mid -1
print(lo)
