inp = (402328, 864247)

def solution1():
    total, total2 = 0, 0
    for x in range(inp[0], inp[1]+1):
        x = str(x)
        if all(l <= r for l, r in zip(x[::], x[1::])):
            total += bool(any(d*2 in x for d in '0123456789'))
            total2 += bool(any(d*2 in x and d*3 not in x for d in '0123456789')) 
        #tunnel visioned on using zip and doing it in an elegant way which took way too much time

    print(total)
    print(total2)

def solution2():
    from collections import Counter
    total, total2 = 0, 0
    for x in range(inp[0], inp[1]+1):
        x = str(x)
        if list(x) == sorted(x):
            total += bool(any(n >= 2 for n in Counter(x).values()))
            total2 += bool(any(n == 2 for n in Counter(x).values()))

    print(total)
    print(total2)

solution1()
solution2()
