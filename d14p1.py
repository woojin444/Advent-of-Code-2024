import re, math

class Robot:
    def __init__(self, position_x: int, position_y: int, velocity_x: int, velocity_y: int):
        self.px = position_x
        self.py = position_y
        self.vx = velocity_x
        self.vy = velocity_y
        self.second = 0

    def move(self, room_size: tuple[int]):
        next_position_x = self.px + self.vx
        next_position_y = self.py + self.vy
        width = room_size[0]
        height = room_size[1]

        if next_position_x >= 0 and next_position_x < width:
            self.px = next_position_x
        elif next_position_x < 0:
            self.px = width + next_position_x
        elif next_position_x >= width:
            self.px = next_position_x - width

        if next_position_y >= 0 and next_position_y < height:
            self.py = next_position_y
        elif next_position_y < 0:
            self.py = height + next_position_y
        elif next_position_y >= height:
            self.py = next_position_y - height

        self.second += 1

robots = []

with open("inputs/d14p12.txt", "r") as input_file:
    position_regex = r'p=(-?\d+,-?\d+)'
    velocity_regex = r'v=(-?\d+,-?\d+)'
    for line in input_file:
        position = re.search(position_regex, line).group(1).split(",")
        velocity = re.search(velocity_regex, line).group(1).split(",")
        robot = Robot(int(position[0]), int(position[1]), int(velocity[0]), int(velocity[1]))
        robots.append(robot)

room_size = (101, 103)

for _ in range(100):
    for robot in robots:
        robot.move(room_size=room_size)

quadrants = [0,0,0,0]

for robot in robots:
    if robot.px <= math.floor(room_size[0]/2) - 1:
        if robot.py <= math.floor(room_size[1]/2) - 1:
            quadrants[0] += 1
        elif robot.py >= math.floor(room_size[1]/2) + 1:
            quadrants[1] += 1
    elif robot.px >= math.floor(room_size[0]/2) + 1:
        if robot.py <= math.floor(room_size[1]/2) - 1:
            quadrants[2] += 1
        elif robot.py >= math.floor(room_size[1]/2) + 1:
            quadrants[3] += 1

print(quadrants[0]*quadrants[1]*quadrants[2]*quadrants[3])