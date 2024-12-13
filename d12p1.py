garden = []

with open("inputs/d12p12.txt") as input_file:
    for line in input_file:
        garden.append(list(line.strip()))

print(garden)