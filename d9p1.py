disk_map = []

with open("inputs/d9p12.txt") as input_file:
    disk_map = list(input_file.read().strip())

disk = []
number = 0
for i in range(len(disk_map)):
    repeat = int(disk_map[i])
    if i % 2 == 0:
        for j in range(repeat):
            disk.append(number)
        number += 1
    else:
        for j in range(repeat):
            disk.append(".")

left_pointer = 0
right_pointer = len(disk)-1

dense_disk = []

while left_pointer <= right_pointer:
    if disk[left_pointer] != ".":
        dense_disk.append(disk[left_pointer])
        left_pointer += 1
    else:
        while disk[right_pointer] == ".": right_pointer -= 1
        dense_disk.append(disk[right_pointer])
        left_pointer += 1
        right_pointer -= 1

answer = 0
number = 0

for item in dense_disk:
    answer += number * item
    number += 1

print(answer)