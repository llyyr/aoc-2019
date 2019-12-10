f = list(map(int, open('08.in').read().strip()))
w, h = 25, 6
wh = w*h

layers = [f[i*wh:(i+1)*wh] for i in range(len(f) // wh)]

l = min(layers, key=lambda l: l.count(0))

print(l.count(1) * l.count(2))


img = [[x for x in p if x != 2][0] for p in zip(*layers)]
pixels = [img[i*w:(i+1)*w] for i in range(h)]
for row in pixels:
    print(''.join(' #' [i] for i in row))
