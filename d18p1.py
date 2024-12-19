import math
import heapq


ROW = 71
COLUMN = 71
grid = [[1 for _ in range(COLUMN)] for _ in range(ROW)]
errors = []

with open("inputs/d18p12.txt", "r") as input_file:
    for line in input_file:
        coordinate = line.strip().split(",")
        errors.append((int(coordinate[0]), int(coordinate[1])))

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
    return grid[row][column] == 1

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
    print(len(path)-1)

    print("The path is ")
    for i in path:
        print("->", i, end=" ")
        grid[i[0]][i[1]] = "_"
    print("\n")
    for row in grid:
        print(''.join(str(x) for x in row))

    print(len(path)-1)
    

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
                    trace_path(cell_details, destination)
                    found_destination = True
                    return 1
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

for i in range(1024):
    grid[errors[i][0]][errors[i][1]] = "#"
    
a_star_search(grid, (0,0), (70,70))