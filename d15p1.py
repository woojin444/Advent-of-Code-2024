class Box:
    def __init__(self, row: int, column:int):
        self.row = row
        self.column = column
    
    # Returns True if the box's next direction is an edge or a series of boxes that lead to an edge
    def at_edge(self, direction: tuple[int], warehouse: list[list]):
        next_position = (self.row + direction[0], self.column + direction[1])
        next_item = warehouse[next_position[0]][next_position[1]]
        if next_item == "#":
            return True
        elif isinstance(next_item, Box):
            return next_item.at_edge(direction=direction, warehouse=warehouse)
        else:
            return False
    
    # if the box or the series of boxes aren't at the edge, move the whole series by swapping the "." with the boxes one by one.
    def move(self, direction: tuple[int], warehouse: list[list]):
        if not self.at_edge(direction=direction, warehouse=warehouse):
            next_position = (self.row + direction[0], self.column + direction[1])
            next_item = warehouse[next_position[0]][next_position[1]]
            if isinstance(next_item, Box):
                warehouse = next_item.move(direction=direction, warehouse=warehouse)
            if warehouse[next_position[0]][next_position[1]] == ".":
                warehouse[next_position[0]][next_position[1]] = self
                warehouse[self.row][self.column] = "."
                self.row = next_position[0]
                self.column = next_position[1]
        return warehouse
                
class Robot:
    def __init__(self, row: int, column: int, movements: list[tuple[int]]):
        self.row = row
        self.column = column
        self.movements = movements

    # Get next movement from the list of movements. If the next is a box then move the box.
    # If the box or the series of boxes could be moved, the next item should turn to "."
    def move(self, warehouse = list[list]):
        if len(self.movements) == 0: return warehouse
        direction = self.movements.pop(0)
        next_position = (self.row + direction[0], self.column + direction[1])
        next_item = warehouse[next_position[0]][next_position[1]]
        if isinstance(next_item, Box):
            warehouse = next_item.move(direction=direction, warehouse=warehouse)
        if warehouse[next_position[0]][next_position[1]] == ".":
            warehouse[next_position[0]][next_position[1]] = self
            warehouse[self.row][self.column] = "."
            self.row = next_position[0]
            self.column = next_position[1]
        return warehouse

# Data ingestion
raw_warehouse = []
raw_movements = []

with open("inputs/d15p12.txt", "r") as input_file:
    movement_tag = False
    for line in input_file:
        if not movement_tag:
            if line == "\n": movement_tag = True
            else: raw_warehouse.append(list(line.strip()))
        else:
            raw_movements = raw_movements + list(line.strip())

# Creation of the warehouse map with robot and boxes objects
warehouse = []
robot = None

for row in range(len(raw_warehouse)):
    line = []
    for column in range(len(raw_warehouse[row])):
        if raw_warehouse[row][column] == "O":
            line.append(Box(row, column))
        elif raw_warehouse[row][column] == "@":
            movements = []
            for movement in raw_movements:
                if movement == "^": movements.append((-1, 0))
                elif movement == ">": movements.append((0, 1))
                elif movement == "v": movements.append((1, 0))
                elif movement == "<": movements.append((0, -1))
            robot = Robot(row, column, movements)
            line.append(robot)
        else:
            line.append(raw_warehouse[row][column])
    warehouse.append(line)

# for row in range(len(warehouse)):
#     line = ""
#     for column in range(len(warehouse[row])):
#         if isinstance(warehouse[row][column], Box):
#             line += "O"
#         elif isinstance(warehouse[row][column], Robot):
#             line += "@"
#         else:
#             line += warehouse[row][column]
#     print(line)

# Running through the movements
for n in range(len(movements)):
    warehouse = robot.move(warehouse=warehouse)
    # print(f"Step {n+1} and movement {raw_movements[n]}:")
    # for row in range(len(warehouse)):
    #     line = ""
    #     for column in range(len(warehouse[row])):
    #         if isinstance(warehouse[row][column], Box):
    #             line += "O"
    #         elif isinstance(warehouse[row][column], Robot):
    #             line += "@"
    #         else:
    #             line += warehouse[row][column]
    #     print(line)

# Calculating the answer
answer = 0
for row in range(len(warehouse)):
    for column in range(len(warehouse[row])):
        if isinstance(warehouse[row][column], Box):
            answer += 100*(row) + (column)

print(answer)