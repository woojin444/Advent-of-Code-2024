raw_maze = []
with open("inputs/d16p12.txt") as input_file:
    for line in input_file:
        raw_maze.append(list(line.strip()))

maze = dict()

for row in range(1, len(raw_maze)-1):
    for column in range(1, len(raw_maze[row])-1):
        if raw_maze[row][column] != "#":
            maze[(row, column)] = {}
            if raw_maze[row-1][column] != "#": maze[(row, column)]["UP"] = (row-1, column)
            if raw_maze[row+1][column] != "#": maze[(row, column)]["DOWN"] = (row+1, column)
            if raw_maze[row][column-1] != "#": maze[(row, column)]["LEFT"] = (row, column-1)
            if raw_maze[row][column+1] != "#": maze[(row, column)]["RIGHT"] = (row, column+1)
            if raw_maze[row][column] == "S": maze["Start"] = (row, column)
            if raw_maze[row][column] == "E": maze["End"] = (row, column)

class Cell:
    def __init__(self):
        self.parent_row = 0
        self.parent_column = 0
        self.f = float('inf') # Total cost in A*
        self.g = float('inf') # Cost from start to this cell
        self.h = 0 # Heuristic cost from this cell to destination

def is_valid(row, column):
    return (row >= 0) and (row < len(raw_maze)) and (column >= 0) and (column < len(raw_maze[column]))

def is_wall(maze, row, column):
    return maze[row][column] == "#"

def is_destination(row, column, destination):
    return row == destination[0] and column == destination[1]

def calculate_h_value(row, column, destination):
    return abs(current)

def a_star_search()

print(maze)