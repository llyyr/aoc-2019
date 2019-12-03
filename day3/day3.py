from collections import defaultdict


with open('input.txt', 'r') as data:
	data = data.read().splitlines()
	dirs = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
	grid = defaultdict(dict)
	for k in range(len(data)):
		steps = data[k].split(',')
		currentPos = (0, 0)
		total = 0
		for step in steps:
			dir = step[0]
			s = int(step[1:])
			for i in range(s):
				total += 1
				currentPos = tuple(currentPos[i] + dirs[dir][i] for i in range(len(currentPos)))
				if k not in grid[currentPos]:
					grid[currentPos][k] = total


print('Part 1: {}'.format(min(map(lambda a: sum(map(abs, a)), [z for z in grid if len(grid[z]) > 1]))))
print('Part 2: {}'.format(min(sum(grid[pos].values()) for pos in grid if len(grid[pos]) > 1)))
