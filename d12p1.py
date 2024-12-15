# Data ingestion
data = []
with open("inputs/d12p12.txt") as input_file:
    for line in input_file:
        data.append(list(line.strip()))

class Region:
    def __init__(self, letter: str):
        self.letter = letter
        self.coordinates = set()

class Coordinate:
    def __init__(self, row: int, column: int, letter: str):
        self.letter = letter
        self.row = row
        self.column = column
        self.region = None
        self.perimeter = 0

    def assign(self, garden: "list[list[Coordinate]]", region: Region):
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

while row < len(garden):
    while column < len(garden[row]):
        