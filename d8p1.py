antenna_map = []

with open("inputs/d8p12.txt") as input_file:
    for line in input_file:
        antenna_map.append(line.strip())

print(antenna_map)
