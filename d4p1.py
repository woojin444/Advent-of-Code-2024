input = []

with open("inputs/d4p12.txt", "r") as input_file:
    for line in input_file:
        input.append(list(line.strip()))

xmas_instance = 0

def xmas_search(row, column, input, word, index, direction):
    # If the index is out of the word, we found all letters
    if index == len(word): return 1
    # If the indexes were to be out of what's available, can't be the answer.
    if row + direction[0] < 0 or row + direction[0] >= len(input): return 0
    if column + direction[1] < 0 or column + direction[1] >= len(input): return 0

    newrow = row + direction[0]
    newcolumn = column + direction[1]

    # Recursive function to find the next letter, adding 1 to the index after the letter is found.
    if input[newrow][newcolumn] == word[index]:
        return xmas_search(newrow, newcolumn, input, word, index=index+1, direction=direction)
    else:
        return 0

for row in range(len(input)):
    for column in range(len(input[row])):
        # Whenever it finds an X, it searches in all directions to find the XMAS. No need to search for reverse as finding one ensures the other will be found.
        if input[row][column] == "X":
            for direction in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
                xmas_instance += xmas_search(row, column, input, "XMAS", 1, direction)

print(xmas_instance)