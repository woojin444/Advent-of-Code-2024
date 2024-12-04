input = []

with open("inputs/d4p12.txt", "r") as input_file:
    for line in input_file:
        input.append(list(line.strip()))

xmas_instance = 0

def xmas_search(row, column, input, word, index, direction):
    if index == len(word): return 1
    if row + direction[0] < 0 or row + direction[0] >= len(input): return 0
    if column + direction[1] < 0 or column + direction[1] >= len(input): return 0

    newrow = row + direction[0]
    newcolumn = column + direction[1]

    if input[newrow][newcolumn] == word[index]:
        return xmas_search(newrow, newcolumn, input, word, index=index+1, direction=direction)
    else:
        return 0

for row in range(len(input)):
    for column in range(len(input[row])):
        if input[row][column] == "X":
            for direction in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
                xmas_instance += xmas_search(row, column, input, "XMAS", 1, direction)

print(xmas_instance)