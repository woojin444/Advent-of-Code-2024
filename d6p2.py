import copy
from alive_progress import alive_bar

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
        # If the same location was checked before with the same orientation then it must be a loop.
        if (self.current_position[0], self.current_position[1]) in self.x:
            if self.direction in self.room[self.current_position[0]][self.current_position[1]][1]:
                return "Loop"
        self.x.add((self.current_position[0], self.current_position[1]))
        self.room[self.current_position[0]][self.current_position[1]][1].add(self.direction)
        self.current_position = (self.current_position[0] + self.direction[0], self.current_position[1] + self.direction[1])
        return "Move"
    
    # Must simulate each scenario with a # on the possible X's.
    def find_loops(self):
        self.x.remove(self.starting_position)
        with alive_bar(len(self.x)) as bar:
            for x in self.x:
                simulated_room = Room()
                simulated_room.room = copy.deepcopy(self.starting_room)
                simulated_room.current_position = copy.deepcopy(self.starting_position)
                simulated_room.direction = copy.deepcopy(self.starting_direction)
                simulated_room.room[x[0]][x[1]] = '#'
            
                while True:
                    result = simulated_room.move()
                    if result == "End":
                        break
                    if result == "Loop":
                        self.loop_opportunity.add(x)
                        break
                bar()

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