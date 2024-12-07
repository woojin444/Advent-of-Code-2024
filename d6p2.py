import copy

class Room():
    def __init__(self):
        self.current_position = None
        self.room = []
        self.direction = (-1,0)
        self.directions = [(-1,0), (0,1), (1,0), (0,-1)]
        self.loop_opportunity = set()

    def add_to_room(self, line, index):
        if "^" in line: self.current_position = (index, line.index("^"))
        # new
        self.room.insert(index, [[symbol, set()] for symbol in line])

    def is_next_edge(self):
        if self.current_position[0] + self.direction[0] < 0 or self.current_position[0] + self.direction[0] >= len(self.room): return True
        if self.current_position[1] + self.direction[1] < 0 or self.current_position[1] + self.direction[1] >= len(self.room[self.current_position[0]]): return True
        return False
    
    def is_next_obstacle(self):
        if self.room[self.current_position[0] + self.direction[0]][self.current_position[1] + self.direction[1]][0] == "#": return True
        return False
    
    def move(self):
        print(self.count_x())
        if self.is_next_edge():
            self.room[self.current_position[0]][self.current_position[1]][0] = "X"
            return "End"
        if self.is_next_obstacle():
            self.direction = self.directions[(self.directions.index(self.direction) + 1) % len(self.directions)]
            return "Obstacle"
        print(f"Simulating {self.current_position}")
        result, coordinate = self.simulate()
        if result == "Loop":
            self.loop_opportunity.add(coordinate)
        self.room[self.current_position[0]][self.current_position[1]][0] = "X"
        self.room[self.current_position[0]][self.current_position[1]][1].add(self.direction)
        self.current_position = (self.current_position[0] + self.direction[0], self.current_position[1] + self.direction[1])
        return "Move"

    def simulate_move(self):
        if self.is_next_edge():
            self.room[self.current_position[0]][self.current_position[1]][0] = "X"
            return "End"
        if self.is_next_obstacle():
            self.direction = self.directions[(self.directions.index(self.direction) + 1) % len(self.directions)]
            return "Obstacle"
        if self.room[self.current_position[0]][self.current_position[1]][0] == "X":
            if self.direction in self.room[self.current_position[0]][self.current_position[1]][1]:
                print("Found a loop opportunity")
                return "Loop"
        self.room[self.current_position[0]][self.current_position[1]][0] = "X"
        self.room[self.current_position[0]][self.current_position[1]][1].add(self.direction)
        self.current_position = (self.current_position[0] + self.direction[0], self.current_position[1] + self.direction[1])
        return "Move"

    def simulate(self):
        simulated_room = Room()
        simulated_room.room = copy.deepcopy(self.room)
        simulated_room.current_position = copy.deepcopy(self.current_position)
        simulated_room.direction = copy.deepcopy(self.direction)

        simulated_room.room[simulated_room.current_position[0] + simulated_room.direction[0]][simulated_room.current_position[1] + simulated_room.direction[1]][0] = "#"

        while True:
            result = simulated_room.simulate_move()
            if result == "End" or result == "Loop": return (result, simulated_room.current_position)

    def count_x(self):
        x = 0
        for row in range(len(self.room)):
            for column in range(len(self.room[row])):
                if self.room[row][column][0] == "X": x += 1
        
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

print(room.count_x(), len(room.loop_opportunity))