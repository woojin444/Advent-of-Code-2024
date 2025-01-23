import math
import heapq

ROW = 141
COLUMN = 141
grid = [[1 for _ in range(COLUMN)] for _ in range(ROW)]
maze = []
START = None
END = None

with open("inputs/d20p12.txt", "r") as input_file:
    for line in input_file:
        maze.append(list(line.strip()))

for row in range(len(maze)):
    for column in range(len(maze[row])):
        if maze[row][column] == "#":
            grid[row][column] = "#"
        if maze[row][column] == "S":
            START = (row, column)
        if maze[row][column] == "E":
            END = (row, column)

class Cell:
    def __init__(self):
        self.parent_row = 0
        self.parent_column = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def is_valid(row, column):
    return (row >= 0) and (row < ROW) and (column >= 0) and (column < COLUMN)

def is_unblocked(grid, row, column):
    return grid[row][column] != "#"

def is_destination(row, column, destination):
    return row == destination[0] and column == destination[1]

def calculate_heuristic(row, column, destination):
    return abs(row - destination[0]) + abs(column - destination[1])

def trace_path(cell_details, destination):
    path = []
    row = destination[0]
    column = destination[1]

    while not (cell_details[row][column].parent_row == row and cell_details[row][column].parent_column == column):
        path.append((row, column))
        temp_row = cell_details[row][column].parent_row
        temp_column = cell_details[row][column].parent_column
        row = temp_row
        column = temp_column

    path.append((row, column))
    path.reverse()
    # print(len(path)-1)

    # print("The path is ")
    # for i in path:
        # print("->", i, end=" ")
    #     grid[i[0]][i[1]] = "_"
    # print("\n")
    # for row in grid:
    #     print(''.join(str(x) for x in row))

    # print(len(path)-1)
    return path
    

def a_star_search(grid, start, destination):
    if not is_valid(start[0], start[1]) or not is_valid(destination[0], destination[1]): 
        print("not valid")
        return

    if not is_unblocked(grid, start[0], start[1]) or not is_unblocked(grid, destination[0], destination[1]):
        print("is blocked")
        return

    if is_destination(start[0], start[1], destination): 
        print("is destination")
        return

    closed_list = [[False for _ in range(COLUMN)] for _ in range(ROW)]

    cell_details = [[Cell() for _ in range(COLUMN)] for _ in range(ROW)]

    row = start[0]
    column = start[1]
    cell_details[row][column].f = 0
    cell_details[row][column].g = 0
    cell_details[row][column].h = 0
    cell_details[row][column].parent_row = row
    cell_details[row][column].parent_column = column

    open_list = []
    heapq.heappush(open_list, (0.0, row, column))

    found_destination = False
    
    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        row = p[1]
        column = p[2]
        closed_list[row][column] = True
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for direction in directions:
            new_row = row + direction[0]
            new_column = column + direction[1]

            if is_valid(new_row, new_column) and is_unblocked(grid, new_row, new_column) and not closed_list[new_row][new_column]:
                if is_destination(new_row, new_column, destination):
                    cell_details[new_row][new_column].parent_row = row
                    cell_details[new_row][new_column].parent_column = column
                    print("destination found")
                    path = trace_path(cell_details, destination)
                    found_destination = True
                    return path
                else:
                    g_new = cell_details[row][column].g + 1.0
                    h_new = calculate_heuristic(new_row, new_column, destination)
                    f_new = g_new + h_new

                    if cell_details[new_row][column].f == float('inf') or cell_details[new_row][new_column].f > f_new:
                        heapq.heappush(open_list, (f_new, new_row, new_column))
                        cell_details[new_row][new_column].f = f_new
                        cell_details[new_row][new_column].g = g_new
                        cell_details[new_row][new_column].h = h_new
                        cell_details[new_row][new_column].parent_row = row
                        cell_details[new_row][new_column].parent_column = column
    
    if not found_destination:
        print("Failed to find destination")
        return 0
    
path = a_star_search(grid, START, END)

score_grid = [[0 for _ in range(COLUMN)] for _ in range(ROW)]
for row in range(len(maze)):
    for column in range(len(maze[row])):
        if maze[row][column] == "#":
            score_grid[row][column] = "#"

cells_to_check = [END]
score_grid[END[0]][END[1]] = 1

while len(cells_to_check) > 0:
    cell_to_check = cells_to_check.pop(0)
    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
        new_cell_coordinate = (cell_to_check[0] + direction[0], cell_to_check[1] + direction[1])
        if is_valid(new_cell_coordinate[0], new_cell_coordinate[1]) and score_grid[new_cell_coordinate[0]][new_cell_coordinate[1]] == 0:
            score_grid[new_cell_coordinate[0]][new_cell_coordinate[1]] = score_grid[cell_to_check[0]][cell_to_check[1]] + 1
            cells_to_check.append(new_cell_coordinate)

more_than_hundred = set()

for coordinate in path:
    for direction in [(-1,0),(0,1),(1,0),(0,-1)]:
        new_coordinate = (coordinate[0] + direction[0], coordinate[1] + direction[1])
        if is_valid(new_coordinate[0], new_coordinate[1]) and score_grid[new_coordinate[0]][new_coordinate[1]] == "#":
            for direction1 in [(-1,0),(0,1),(1,0),(0,-1)]:
                after_cheat_coordinate = (new_coordinate[0] + direction1[0], new_coordinate[1] + direction1[1])
                if is_valid(after_cheat_coordinate[0], after_cheat_coordinate[1]) and score_grid[after_cheat_coordinate[0]][after_cheat_coordinate[1]] != "#":
                    if (score_grid[coordinate[0]][coordinate[1]]-1) - score_grid[after_cheat_coordinate[0]][after_cheat_coordinate[1]] >= 100:
                        more_than_hundred.add(new_coordinate)

print(len(more_than_hundred))

more_than_hundred = set()
                        
def get_n_steps(current_coordinate: tuple[int], n: int):
    valid_coordinates = set()
    for x in range(n+1):
        for y in range(-n+x, n-x+1):
            if is_valid(current_coordinate[0]+x, current_coordinate[1]+y):
                valid_coordinates.add((current_coordinate[0]+x, current_coordinate[1]+y))
            if is_valid(current_coordinate[0]-x, current_coordinate[1]+y):
                valid_coordinates.add((current_coordinate[0]-x, current_coordinate[1]+y))
    return valid_coordinates

for coordinate in path:
    for after_cheat_coordinate in get_n_steps(coordinate, 2):
        if score_grid[after_cheat_coordinate[0]][after_cheat_coordinate[1]] != "#":
            if (score_grid[coordinate[0]][coordinate[1]]-1) - score_grid[after_cheat_coordinate[0]][after_cheat_coordinate[1]] >= 100:
                more_than_hundred.add((coordinate[0], coordinate[1], after_cheat_coordinate[0], after_cheat_coordinate[1]))

print(len(more_than_hundred))
