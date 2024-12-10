antenna_map = []
antenna_coordinates = {}

with open("inputs/d8p12.txt") as input_file:
    for line in input_file:
        antenna_map.append(list(line.strip()))

for row in range(len(antenna_map)):
    for col in range(len(antenna_map[row])):
        symbol = antenna_map[row][col]
        if symbol != ".":
            if symbol in antenna_coordinates: antenna_coordinates[symbol].append((row, col))
            else: antenna_coordinates[symbol] = [(row, col)]

def combination(lst):
    combinations = []
    for i in range(len(lst)-1):
        for j in range(i+1, len(lst)):
            combinations.append((lst[i], lst[j]))
    return combinations

antinodes = set()

for antenna in antenna_coordinates.keys():
    antenna_pairs = combination(antenna_coordinates[antenna])
    for pair in antenna_pairs:
        vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
        antinode1 = (pair[0][0] - vector[0], pair[0][1] - vector[1])
        antinode2 = (pair[1][0] + vector[0], pair[1][1] + vector[1])

        for antinode in [antinode1, antinode2]:
            if antinode[0] < 0 or antinode[0] >= len(antenna_map): continue
            if antinode[1] < 0 or antinode[1] >= len(antenna_map[antinode[0]]): continue
            antinodes.add(antinode)

print(len(antinodes))


