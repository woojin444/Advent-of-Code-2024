import copy

class Room():
    def __init__(self):
        self.current_position = None
        self.starting_position = None
        self.room = []
        self.starting_room = []
        self.direction = (-1,0)
        self.starting_direction = (-1,0)
        self.directions = [(-1,0), (0,1), (1,0), (0,-1)]
        self.loop_opportunity = set()
        self.x = set()

    def add_to_room(self, line, index):
        if "^" in line: 
            self.current_position = (index, line.index("^"))
            self.starting_position = (index, line.index("^"))
        # new
        self.room.insert(index, [[symbol, set()] for symbol in line])
        self.starting_room.insert(index, [[symbol, set()] for symbol in line])

    def is_next_edge(self):
        if self.current_position[0] + self.direction[0] < 0 or self.current_position[0] + self.direction[0] >= len(self.room): return True
        if self.current_position[1] + self.direction[1] < 0 or self.current_position[1] + self.direction[1] >= len(self.room[self.current_position[0]]): return True
        return False
    
    def is_next_obstacle(self):
        if self.room[self.current_position[0] + self.direction[0]][self.current_position[1] + self.direction[1]][0] == "#": return True
        return False
    
    def move(self):
        if self.is_next_edge():
            self.x.add((self.current_position[0], self.current_position[1]))
            return "End"
        if self.is_next_obstacle():
            self.direction = self.directions[(self.directions.index(self.direction) + 1) % len(self.directions)]
            return "Obstacle"
        if (self.current_position[0], self.current_position[1]) in self.x:
            if self.direction in self.room[self.current_position[0]][self.current_position[1]][1]:
                print("Found a loop opportunity")
                return "Loop"
        self.x.add((self.current_position[0], self.current_position[1]))
        self.room[self.current_position[0]][self.current_position[1]][1].add(self.direction)
        self.current_position = (self.current_position[0] + self.direction[0], self.current_position[1] + self.direction[1])
        return "Move"
    
    def find_loops(self):
        i = 0
        for x in self.x:
            i += 1
            print(f"Checking {i} out of {len(self.x)} X's")
            simulated_room = Room()
            simulated_room.room = copy.deepcopy(self.starting_room)
            simulated_room.current_position = copy.deepcopy(self.starting_position)
            simulated_room.direction = copy.deepcopy(self.starting_direction)
            print(x)
            simulated_room.room[x[0]][x[1]] = '#'
        
            while True:
                result = simulated_room.move()
                if result == "End":
                    break
                if result == "Loop":
                    self.loop_opportunity.add(x)
                    break

room = Room()

with open("inputs/d6p12.txt", "r") as input_file:
    array_count = 0
    for line in input_file:
        room.add_to_room(line, array_count)
        array_count += 1

end = False
while not end:
    if room.move() == "End": end = True

room.find_loops()

print(len(room.loop_opportunity))