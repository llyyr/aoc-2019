#https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Modular_inverse

def egcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = egcd(a, b)
    if g == 1:
        return x % b

class Deck(object):
    def __init__(self, count):
        self.count = count
        self.factor = 1
        self.offset = 0

    def get(self, i):
        return (self.factor*i + self.offset) % self.count

    def new(self):
        self.offset = self.get(-1)
        self.factor = (self.factor * -1) % self.count

    def cut(self, n):
        self.offset = self.get(n)

    def increment(self, n):
        self.factor = (self.factor * modinv(n, self.count)) % self.count

    def shuffle(self, lines):
        for line in lines:
            if line.startswith('cut'):
                n = int(line.strip()[3:])
                self.cut(n)
            elif line.startswith('deal with'):
                n = int(line.strip()[-2:])
                self.increment(n)
            elif line.startswith('deal into'):
                self.new()

    def __mul__(self, other):
        assert self.count == other.count
        nd = Deck(self.count)
        nd.factor = (self.factor * other.factor) % self.count
        nd.offset = (other.factor * self.offset + other.offset) % self.count
        return nd


def my_pow(x, p):
    if p == 0:
        return Deck(x.count)
    elif p == 1:
        return x
    elif p % 2 == 1:
        return x * my_pow(x * x, (p - 1) // 2)
    return my_pow(x * x, p // 2)

def part2(data):
    count = 119315717514047
    d = Deck(count)
    d.shuffle(data)
    d = my_pow(d, 101741582076661)
    return d.get(2020)

def part1(data):
    count = 10007
    d = Deck(count)
    d.shuffle(data)
    for i in range(count):
        if d.get(i) == 2019:
            return i

puzzle = list(map(str, (x for x in open('22.in').readlines())))
part1, part2 = part1(puzzle), part2(puzzle)
print(part1, part2)
