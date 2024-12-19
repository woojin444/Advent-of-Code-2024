from __future__ import annotations

def print_warehouse(warehouse):
    for row in range(len(warehouse)):
        line = ""
        for column in range(len(warehouse[row])):
            if isinstance(warehouse[row][column], Box):
                if warehouse[row][column].lr == "left":
                    line += "["
                else:
                    line += "]"
            elif isinstance(warehouse[row][column], Robot):
                line += "@"
            else:
                line += warehouse[row][column]
        print(line)

class Box:
    def __init__(self, row: int, column:int):
        self.row = row
        self.column = column
        self.connected_box = None
        self.lr = None

    def connect_right(self, box: Box):
        self.connected_box = box
        self.lr = "left"
        box.connected_box = self
        box.lr = "right"
    
    # Returns True if the box's next direction is an edge or a series of boxes that lead to an edge
    def at_edge(self, direction: tuple[int], warehouse: list[list], lr: str):
        next_position = (self.row + direction[0], self.column + direction[1])
        next_item = warehouse[next_position[0]][next_position[1]]
        # If the next item is a wall then return True
        if next_item == "#":
            return True
        elif isinstance(next_item, Box):
            if direction == (0, -1) or direction == (0, 1):
                # If the check is horizontal, then keep checking the next item as long as it's a box.
                return next_item.at_edge(direction=direction, warehouse=warehouse, lr=next_item.lr)
            else:
                # If the check is vertical, check the next of the current and the next of the connected box.
                if self.connected_box.lr != lr:
                    return next_item.at_edge(direction=direction, warehouse=warehouse, lr=next_item.lr) or self.connected_box.at_edge(direction=direction, warehouse=warehouse, lr=lr)
                else:
                    return next_item.at_edge(direction=direction, warehouse=warehouse, lr=next_item.lr)
        else:
            if (direction == (-1, 0) or direction == (1, 0)) and self.connected_box.lr != lr:
                return self.connected_box.at_edge(direction=direction, warehouse=warehouse, lr=lr)
            else:
                return False
    
    # if the box or the series of boxes aren't at the edge, move the whole series by swapping the "." with the boxes one by one.
    def move(self, direction: tuple[int], warehouse: list[list], lr: str):
        if not self.at_edge(direction=direction, warehouse=warehouse, lr=lr):
            next_position = (self.row + direction[0], self.column + direction[1])
            next_item = warehouse[next_position[0]][next_position[1]]
            if isinstance(next_item,Box):
                if direction in [(0, -1), (0, 1)]:
                    warehouse = next_item.move(direction=direction, warehouse=warehouse, lr=next_item.lr)
                    if warehouse[next_position[0]][next_position[1]] == ".":
                        warehouse[next_position[0]][next_position[1]] = self
                        warehouse[self.row][self.column] = "."
                        self.row = next_position[0]
                        self.column = next_position[1]
                else:
                    if next_item.lr == lr:
                        warehouse = next_item.move(direction=direction, warehouse=warehouse, lr=next_item.lr)
                        next_position_of_connected = (self.connected_box.row + direction[0], self.connected_box.column + direction[1])
                        if warehouse[next_position[0]][next_position[1]] == ".":
                            warehouse[next_position[0]][next_position[1]] = self
                            warehouse[self.row][self.column] = "."
                            warehouse[next_position_of_connected[0]][next_position_of_connected[1]] = self.connected_box
                            warehouse[self.connected_box.row][self.connected_box.column] = "."
                            self.row = next_position[0]
                            self.column = next_position[1]
                            self.connected_box.row = next_position_of_connected[0]
                            self.connected_box.column = next_position_of_connected[1]
                    else:
                        warehouse = next_item.move(direction=direction, warehouse=warehouse, lr=next_item.lr)
                        warehouse = self.connected_box.move(direction=direction, warehouse=warehouse, lr=lr)
                        if warehouse[next_position[0]][next_position[1]] == ".":
                            warehouse[next_position[0]][next_position[1]] = self
                            warehouse[self.row][self.column] = "."
                            self.row = next_position[0]
                            self.column = next_position[1]
            else:
                next_position_of_connected = (self.connected_box.row + direction[0], self.connected_box.column + direction[1])
                if self.lr == lr:
                    warehouse = self.connected_box.move(direction=direction, warehouse=warehouse, lr=lr)
                    warehouse[next_position[0]][next_position[1]] = self
                    warehouse[self.row][self.column] = "."
                    self.row = next_position[0]
                    self.column = next_position[1]
                else:
                    if warehouse[next_position[0]][next_position[1]] == ".":
                        warehouse[next_position[0]][next_position[1]] = self
                        warehouse[self.row][self.column] = "."
                        warehouse[next_position_of_connected[0]][next_position_of_connected[1]] = self.connected_box
                        warehouse[self.connected_box.row][self.connected_box.column] = "."
                        self.row = next_position[0]
                        self.column = next_position[1]
                        self.connected_box.row = next_position_of_connected[0]
                        self.connected_box.column = next_position_of_connected[1]
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
            warehouse = next_item.move(direction=direction, warehouse=warehouse, lr=next_item.lr)
        if warehouse[next_position[0]][next_position[1]] == ".":
            warehouse[next_position[0]][next_position[1]] = self
            warehouse[self.row][self.column] = "."
            self.row = next_position[0]
            self.column = next_position[1]
        return warehouse

# Data ingestion
raw_warehouse = []
raw_movements = []

with open("inputs/playground.txt", "r") as input_file:
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
        new_column = column*2
        if raw_warehouse[row][column] == "O":
            box1 = Box(row, new_column)
            box2 = Box(row, new_column+1)
            box1.connect_right(box2)
            line += [box1, box2]
        elif raw_warehouse[row][column] == "@":
            movements = []
            for movement in raw_movements:
                if movement == "^": movements.append((-1, 0))
                elif movement == ">": movements.append((0, 1))
                elif movement == "v": movements.append((1, 0))
                elif movement == "<": movements.append((0, -1))
            robot = Robot(row, new_column, movements)
            line.append(robot)
            line.append(".")
        else:
            line += raw_warehouse[row][column]*2
    warehouse.append(line)

print_warehouse(warehouse)

# Running through the movements
for n in range(len(movements)):
    print(f"Step {n+1} and movement {raw_movements[n]}:")
    warehouse = robot.move(warehouse=warehouse)
    print_warehouse(warehouse)
    while n > 308: input()

# Calculating the answer
answer = 0
for row in range(len(warehouse)):
    for column in range(len(warehouse[row])):
        if isinstance(warehouse[row][column], Box):
            answer += 100*(row) + (column)

print(answer)