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
    
    def populate(self, garden: list[list[Coordinate]], coordinate: Coordinate):
        coordinate.assign(garden=garden, region=self)
        coordinates_to_check = []
        # If the next coordinate is valid
        for next_coordinate in coordinate.next_coordinates(garden=garden):
            # and if the next letter is the same letter as the region's letter,
            # and if the next coordinate is not assigned.
            if next_coordinate.letter == self.letter and not next_coordinate.is_assigned():
                # then add the next coordinate to the list of coordinates to check.
                coordinates_to_check.append(next_coordinate)
        while len(coordinates_to_check) > 0:
            coordinate_to_check = coordinates_to_check.pop()
            coordinate_to_check.assign(garden=garden, region=self)
            self.coordinates.add(coordinate_to_check)
            for next_coordinate in coordinate_to_check.next_coordinates(garden=garden):
                if next_coordinate not in coordinates_to_check and next_coordinate not in self.coordinates:
                    if next_coordinate.letter == self.letter:
                        coordinates_to_check.append(next_coordinate)
            
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

    def next_coordinates(self, garden: list[list[Coordinate]]) -> list[Coordinate]:
        valid_coordinates = []
        for direction in [(-1,0), (1,0), (0,-1), (0,1)]:
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

regions = []

row = 0
column = 0

for row in garden:
    for coordinate in row:
        if not coordinate.is_assigned():
            region = Region(coordinate.letter)
            region.populate(garden=garden, coordinate=coordinate)
            regions.append(region)

answer = 0

for region in regions:
    area = len(region.coordinates)
    perimeter = sum(map(lambda coordinate: coordinate.perimeter, region.coordinates))
    print(f"Letter: {region.letter}. Area: {area}. Perimeter: {perimeter}")
    answer += area * perimeter

print(answer)