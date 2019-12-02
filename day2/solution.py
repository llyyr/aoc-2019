with open("input.txt", "r") as f:
	b = [int(x) for x in f.read().split(",")]


for x in range(100):
	for y in range(100):
		a = [x for x in b]
		a[1], a[2] = x, y
		iPos = 0

		while a[iPos] != 99:
			i1, i2, i3 = a[iPos+1], a[iPos+2], a[iPos+3]
			if a[iPos] == 1:
				a[i3] = a[i1] + a[i2]
			if a[iPos] == 2:
				a[i3] = a[i1] * a[i2]
			iPos += 4

		if a[0] == 19690720:
			print("Part 2: {}".format(100 * x + y))

		if x == 12 and y == 2:
			print("Part 1: {}".format(a[0]))
