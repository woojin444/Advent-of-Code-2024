from __future__ import annotations

# Data ingestion
data = []
with open("inputs/d12p12.txt") as input_file:
    for line in input_file:
        data.append(list(line.strip()))

class Region:
    def __init__(self, letter: str):
        self.letter = letter
        self.coordinates = set()
        self.top_left_row = None
        self.top_left_column = None
        self.bottom_right_row = None
        self.bottom_right_column = None
    
    def populate(self, garden: list[list[Coordinate]], coordinate: Coordinate):
        self.top_left_row = self.bottom_right_row = coordinate.row
        self.top_left_column = self.bottom_right_column = coordinate.column
        coordinate.assign(garden=garden, region=self)
        coordinates_to_check = []
        # If the next coordinate is valid
        for next_coordinate in coordinate.next_coordinates(garden=garden, directions=[(-1,0), (1,0), (0,-1), (0,1)]):
            # and if the next letter is the same letter as the region's letter,
            # and if the next coordinate is not assigned.
            if next_coordinate.letter == self.letter and not next_coordinate.is_assigned():
                # then add the next coordinate to the list of coordinates to check.
                coordinates_to_check.append(next_coordinate)
        while len(coordinates_to_check) > 0:
            coordinate_to_check = coordinates_to_check.pop()
            # Creates the boundary of lines to check for differences
            self.top_left_row = min(self.top_left_row, coordinate_to_check.row)
            self.top_left_column = min(self.top_left_column, coordinate_to_check.column)
            self.bottom_right_row = max(self.bottom_right_row, coordinate_to_check.row)
            self.bottom_right_column = max(self.bottom_right_column, coordinate_to_check.column)
            coordinate_to_check.assign(garden=garden, region=self)
            self.coordinates.add(coordinate_to_check)
            for next_coordinate in coordinate_to_check.next_coordinates(garden=garden, directions=[(-1,0), (1,0), (0,-1), (0,1)]):
                if next_coordinate not in coordinates_to_check and next_coordinate not in self.coordinates:
                    if next_coordinate.letter == self.letter:
                        coordinates_to_check.append(next_coordinate)

    def find_area(self):
        return len(self.coordinates)

    def find_perimeter(self):
        return sum(map(lambda coordinate: coordinate.perimeter, self.coordinates))
    
    def find_sides(self, garden: list[list[Coordinate]]):
        # Checking every row until the end of the boundary +2 (+1 because range isn't inclusive, +1 because the check is with the coord above)
        total_sides = 0
        for row in range(self.top_left_row, self.bottom_right_row+2):
            # Column only needs +1 for inclusiveness.
            horizontal_sides = 0
            # previous_flag[0] indicates if the current_coordinate.region is the same, [1] indicates if the above_coordinate.region is the same
            previous_flag = [1,1]
            for column in range(self.top_left_column, self.bottom_right_column+1):
                current_flag = [0,0]
                if row < len(garden):
                    current_coordinate = garden[row][column]
                    if current_coordinate.region == self: current_flag[0] = 1
                    above_coordinate = current_coordinate.next_coordinates(garden=garden, directions=[(-1,0)])
                    if len(above_coordinate) > 0:
                        if above_coordinate[0].region == self: current_flag[1] = 1 
                else:
                    current_coordinate = garden[row-1][column]
                    if current_coordinate.region == self: current_flag[0] = 1
                    current_flag[1] = 0
                if current_flag != previous_flag:
                    # if current_coordinate and above_coordinate are in the same region
                    if current_flag[0] == current_flag[1]:
                        previous_flag = current_flag
                    else:
                        # Only add a side when the flags are different and if the current flag components are also different
                        horizontal_sides += 1
                        previous_flag = current_flag 
            
            total_sides += horizontal_sides

        for column in range(self.top_left_column, self.bottom_right_column+2):
            vertical_sides = 0
            previous_flag = [1,1]
            for row in range(self.top_left_row, self.bottom_right_row+1):
                current_flag = [0,0]
                if column < len(garden[row]):
                    current_coordinate = garden[row][column]
                    if current_coordinate.region == self: current_flag[0] = 1
                    left_coordinate = current_coordinate.next_coordinates(garden=garden, directions=[(0,-1)])
                    if len(left_coordinate) > 0:
                        if left_coordinate[0].region == self: current_flag[1] = 1
                else:
                    current_coordinate = garden[row][column-1]
                    if current_coordinate.region == self: current_flag[0] = 1
                    current_flag[1] = 0
                if current_flag != previous_flag:
                    if current_flag[0] == current_flag[1]:
                        previous_flag = current_flag
                    else:
                        vertical_sides += 1
                        previous_flag = current_flag
        
            total_sides += vertical_sides

        return total_sides

class Coordinate:
    def __init__(self, row: int, column: int, letter: str):
        self.letter = letter
        self.row = row
        self.column = column
        self.region = None
        self.perimeter = 0

    def assign(self, garden: list[list[Coordinate]], region: Region):
        region.coordinates.add(self)
        self.region = region
        for direction in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_row = self.row + direction[0]
            next_column = self.column + direction[1]
            if next_row >= 0 and next_row < len(garden) and next_column >= 0 and next_column < len(garden[self.row]):
                if self.letter != garden[next_row][next_column].letter:
                    self.perimeter += 1
            else:
                self.perimeter += 1

    def is_assigned(self):
        if self.region == None: return False
        else: return True

    def next_coordinates(self, garden: list[list[Coordinate]], directions: list[tuple[int]]) -> list[Coordinate]:
        valid_coordinates = []
        for direction in directions:
            next_row = self.row + direction[0]
            next_column = self.column + direction[1]
            # If the next coordinate is valid
            if next_row >= 0 and next_row < len(garden) and next_column >= 0 and next_column < len(garden[next_row]):
                valid_coordinates.append(garden[next_row][next_column])
        return valid_coordinates

# Garden creation with all the coordinates
garden = []

for row in range(len(data)):
    row_list = []
    for column in range(len(data[row])):
        coordinate = Coordinate(row=row, column=column, letter=data[row][column])
        row_list.append(coordinate)
    garden.append(row_list)

# Region creation from the garden
regions = []

for row in garden:
    for coordinate in row:
        if not coordinate.is_assigned():
            region = Region(coordinate.letter)
            region.populate(garden=garden, coordinate=coordinate)
            regions.append(region)

# Counts the perimeters
answer = 0

for region in regions:
    print(f"Region letter: {region.letter}, Region coord: [({region.top_left_row}, {region.top_left_column}), ({region.bottom_right_row}, {region.bottom_right_column})], Region area: {region.find_area()}, Region sides: {region.find_sides(garden=garden)}")
    answer += region.find_area() * region.find_sides(garden=garden)

print(answer)