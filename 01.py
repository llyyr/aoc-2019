def calculateFuel(i):
    return int(int(i)/3) - 2

def calculateFuel2(i):
    add = calculateFuel(i)
    return (add + calculateFuel2(add)) if add >= 0 else 0

with open("01.in", "r") as f:
    totalFuelMass = 0
    totalFuelMass2 = 0
    for mass in f:
        totalFuelMass += calculateFuel(mass)
        totalFuelMass2 += calculateFuel2(mass)

print("Part 1: {}".format(totalFuelMass))
print("Part 2: {}".format(totalFuelMass2))
