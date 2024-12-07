class Room():
    def __init__(self):
        self.current_position = None
        self.room = []
        self.direction = (-1,0)
        self.directions = [(-1,0), (0,1), (1,0), (0,-1)]

    def add_to_room(self, line, index):
        if "^" in line: self.current_position = (index, line.index("^"))
        self.room.insert(index, list(line))

    def is_next_edge(self):
        if self.current_position[0] + self.direction[0] < 0 or self.current_position[0] + self.direction[0] >= len(self.room): return True
        if self.current_position[1] + self.direction[1] < 0 or self.current_position[1] + self.direction[1] >= len(self.room[self.current_position[0]]): return True
        return False
    
    def is_next_obstacle(self):
        if self.room[self.current_position[0] + self.direction[0]][self.current_position[1] + self.direction[1]] == "#": return True
        return False
    
    def move(self):
        if self.is_next_edge():
            self.room[self.current_position[0]][self.current_position[1]] = "X"
            return "End"
        if self.is_next_obstacle():
            self.direction = self.directions[(self.directions.index(self.direction) + 1) % len(self.directions)]
            return "Obstacle"
        self.room[self.current_position[0]][self.current_position[1]] = "X"
        self.current_position = (self.current_position[0] + self.direction[0], self.current_position[1] + self.direction[1])
        return "Move"

    def count_x(self):
        x = 0
        for row in range(len(self.room)):
            for column in range(len(self.room[row])):
                if self.room[row][column] == "X": x += 1
        
        return x

room = Room()

with open("inputs/d6p12.txt", "r") as input_file:
    array_count = 0
    for line in input_file:
        room.add_to_room(line, array_count)
        array_count += 1

end = False
while not end:
    if room.move() == "End": end = True

print(room.count_x())