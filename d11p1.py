stones = []

with open("inputs/d11p12.txt") as input_file:
    stones = list(map(int, input_file.read().replace("\n","").split(" ")))

def blink(stones):
    next_stones = []

    for stone in stones:
        if stone == 0:
            next_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            middle_index = int(len(str(stone))/2)
            next_stones.append(int(str(stone)[0:middle_index]))
            next_stones.append(int(str(stone)[middle_index:]))
        else:
            next_stones.append(stone*2024)

    return next_stones

for _ in range(25):
    stones = blink(stones)

print(len(stones))