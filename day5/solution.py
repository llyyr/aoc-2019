with open("input.txt", "r") as f:
	b = list(map(int, f.read().split(',')))


def wtffff(a, iPos, num, jump=False):
	n = 2 if jump else 3
	while n > len(num):
		num = [0]+num
	if not jump:
		num[0] = 1
	return [x if num[len(num)-1-i] == 1 else a[x] for i, x in enumerate(a[iPos+1:iPos+n+1])]


a = [x for x in b]
iPos = 0

while True:
	num = [int(x) for x in str(a[iPos])]
	opcode = (0 if len(num) == 1 else num[-2])*10+num[-1]
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
			a[i1] = int(input('Number: '))

		elif opcode == 4:
			print(a[i1])

	else:
		break
