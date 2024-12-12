trail_map = []

with open("inputs/d10p12.txt") as input_file:
    for line in input_file:
        trail_map.append(list(map(int, line.strip())))

def valid_steps(trail_map, position):
    valid_steps = []
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    for direction in directions:
        new_position = (position[0] + direction[0], position[1] + direction[1])
        if new_position[0] >= 0 and new_position[0] < len(trail_map) and new_position[1] >= 0 and new_position[1] < len(trail_map[new_position[0]]):
            if trail_map[new_position[0]][new_position[1]] == trail_map[position[0]][position[1]] + 1:
                valid_steps.append(new_position)

    return valid_steps

# Change the set to a list to find all the non-unique methods of getting to the apex.
def find_trails(trail_map, position):
    apexes = []
    next_steps = valid_steps(trail_map=trail_map, position=position)
    for step in next_steps:
        if trail_map[step[0]][step[1]] == 9:
            apexes.append(step)
        else:
            apexes = apexes + find_trails(trail_map=trail_map, position=step)
    return apexes

score = 0

for x in range(len(trail_map)):
    for y in range(len(trail_map[x])):
        if trail_map[x][y] == 0:
            score += len(find_trails(trail_map=trail_map, position=(x,y)))

print(score)