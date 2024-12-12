from functools import cache

stones = []

with open("inputs/d11p12.txt") as input_file:
    stones = list(map(int, input_file.read().replace("\n","").split(" ")))

@cache
def blink_singular(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        middle_index = int(len(str(stone))/2)
        return [int(str(stone)[0:middle_index]), int(str(stone)[middle_index:])]
    else:
        return [stone*2024]

@cache
def calculate_num_stones(stone, blinks):
    if blinks == 0:
        return 1
    
    next_stones = blink_singular(stone)
    return sum(calculate_num_stones(num, blinks - 1) for num in next_stones)

total_stones = 0
for stone in stones:
    total_stones += calculate_num_stones(stone, 75)

print(total_stones)