from math import gcd

moon, velocity = [], []


for line in open('12.in').readlines():
    line = line.strip('<>\n')
    line = line.split(', ')
    each = {}
    for w in line:
        k, v = w.split('=')
        each[k] = int(v)
    moon.append(each)
    velocity.append({'x': 0, 'y': 0, 'z': 0})


def step():
    nm, nv = moon, velocity
    for i in range(len(nm)):
        for j in range(len(nm)):
            for k in nm[i]:
                if nm[i][k] < nm[j][k]:
                    nv[i][k] += 1
                elif nm[i][k] > nm[j][k]:
                    nv[i][k] -= 1
    for i in range(len(nm)):    
        for k in nm[i]:
            nm[i][k] += nv[i][k]
    return nm, nv

# part 1
for _ in range(1000):
    nm, nv = step()

ans = 0 
for i in range(len(nm)):
    potential = 0
    kinetic = 0
    for k in moon[i]:
        potential += abs(nm[i][k])
        kinetic += abs(nv[i][k])
    ans += potential * kinetic
print(ans)


# part 2
seen = {k: {} for k in moon[0]}
count = {k: 0 for k in moon[0]}
t = 0
ans = 1
ans_count = 0
while ans_count < 3:
    nm, nv = step()
    key = {k: [] for k in nm[0]}
    for i in range(len(nm)):
        for k in nm[i]:
            key[k].append(nm[i][k])
            key[k].append(nv[i][k])
    key = {k: tuple(v) for k, v in key.items()}
    for k in key:
        if key[k] in seen[k]:
            if count[k] == 0:
                assert seen[k][key[k]] == 0
                ans = ans*t // gcd(ans,t)
                ans_count += 1
                if ans_count == 3:
                    print(ans)
                    break
            count[k] += 1
        seen[k][key[k]] = t
    t += 1
