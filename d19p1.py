import heapq

towels = []
designs = []

with open("inputs/d19p12.txt", "r") as input_file:
    lines = input_file.readlines()
    towels = lines[0].strip().split(", ")
    for line in lines[2:]:
        designs.append(line.strip())

max_look_back = len(sorted(towels, key=len, reverse=True)[0])

look_up_dict = {letter: [[] for _ in range(max_look_back)] for letter in ['w', 'u', 'b', 'r', 'g']}
for towel in towels:
    for i in range(len(towel)):
        look_up_dict[towel[i]][i].append(towel)

def check_design(design):
    possibilities = [set() for _ in range(len(design))]
    for i in range(len(design)):
        for l in range(0, min(max_look_back, len(design)-i)):
            possibilities[i].update(look_up_dict[design[i]][l])

    to_check = []
    heapq.heappush(to_check, (len(design), design, 0))
    designs_checked = [design]

    while len(to_check) > 0:
        _, left_over_design, index = heapq.heappop(to_check)
        for possibility in possibilities[index]:
            # print(f"Checking {left_over_design}: Range 0~{len(possibility)}: {left_over_design[0:len(possibility)]} == {possibility}")
            # input()
            if left_over_design[0:len(possibility)] == possibility:
                # print(f"Found a match! New left over design: {left_over_design[len(possibility):]}")
                if len(left_over_design[len(possibility):]) == 0: return 1
                if left_over_design[len(possibility):] not in designs_checked:
                    heapq.heappush(to_check, (len(left_over_design)-len(possibility), left_over_design[len(possibility):], index+len(possibility)))
                    designs_checked.append(left_over_design[len(possibility):])
                    # print(f"Added {left_over_design[len(possibility):]} to the list")
                    
    return 0

answer = 0

for design in designs:
    answer += check_design(design)
    
print(answer)