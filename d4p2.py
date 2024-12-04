input = []

with open("inputs/d4p12.txt", "r") as input_file:
    for line in input_file:
        input.append(list(line.strip()))

x_mas_instance = 0

def x_mas_search(row, column, input, word, direction1, direction2):
    if row + direction1[0] < 0 or row + direction1[0] >= len(input): return 0
    if column + direction1[1] < 0 or column + direction1[1] >= len(input): return 0
    if row + direction2[0] < 0 or row + direction2[0] >= len(input): return 0
    if column + direction2[1] < 0 or column + direction2[1] >= len(input): return 0

    newrow1 = row + direction1[0]
    newcolumn1 = column + direction1[1]
    newrow2 = row + direction2[0]
    newcolumn2 = column + direction2[1]

    word = word.replace(input[newrow1][newcolumn1], "", 1)
    word = word.replace(input[newrow2][newcolumn2], "", 1)

    return not word

for row in range(len(input)):
    for column in range(len(input[row])):
        if input[row][column] == "A":
            # Idea is to search for the ends of the crosses, removing a letter from the "SM" and only when
            # the final string is empty, the topleft or topright can come out to be True.
            # If they're both True, then we have the X-MAS.
            topleft = x_mas_search(row, column, input, "SM", (-1,-1), (1,1))
            topright = x_mas_search(row, column, input, "SM", (-1,1), (1,-1))

            if topleft and topright:
                x_mas_instance += 1

print(x_mas_instance)