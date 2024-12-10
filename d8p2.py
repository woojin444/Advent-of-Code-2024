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
        antinodes.add(pair[0])
        antinodes.add(pair[1])
        vector = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
        antinode1 = (pair[0][0] - vector[0], pair[0][1] - vector[1])
        antinode2 = (pair[1][0] + vector[0], pair[1][1] + vector[1])

        while antinode1[0] >= 0 and antinode1[1] >= 0 and antinode1[0] < len(antenna_map) and antinode1[1] < len(antenna_map[antinode1[0]]):
            antinodes.add(antinode1)
            antinode1 = (antinode1[0] - vector[0], antinode1[1] - vector[1])

        while antinode2[0] >= 0 and antinode2[1] >= 0 and antinode2[0] < len(antenna_map) and antinode2[1] < len(antenna_map[antinode2[0]]):
            antinodes.add(antinode2)
            antinode2 = (antinode2[0] + vector[0], antinode2[1] + vector[1])

print(len(antinodes))


