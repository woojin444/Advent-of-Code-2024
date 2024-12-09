from itertools import product

calibrations = []

with open("inputs/d7p12.txt") as input_file:
    for line in input_file:
        final, numbers = line.replace("\n","").split(": ")
        numbers = numbers.replace(" ", " + ").split(" ")
        calibrations.append([int(final), numbers])

def calculate(numbers):
    answer = int(numbers[0])
    for i in range(1, len(numbers)):
        if i % 2 != 0:
            operator = numbers[i]
        else:
            if operator == "+": answer = answer + int(numbers[i])
            if operator == "*": answer = answer * int(numbers[i])
            if operator == "||": answer = int(str(answer)+numbers[i])

    return answer

def generate_permutations(lst):
    # Extract numbers and operators
    numbers = lst[::2]   # Every other element, starting from index 0
    operators = lst[1::2]  # Every other element, starting from index 1
    
    # Generate all possible combinations of "+" and "*"
    possible_operators = list(product(["+", "*", "||"], repeat=len(operators)))
    
    permutations = []
    for ops in possible_operators:
        perm = []
        for i in range(len(numbers)):
            perm.append(numbers[i])
            if i < len(ops):
                perm.append(ops[i])
        permutations.append(perm)

    return permutations

brute_force = 0

for calibration in calibrations:
    permutations = generate_permutations(calibration[1])
    for permutation in permutations:
        if calculate(permutation) == calibration[0]: 
            brute_force += calibration[0]
            break

print(brute_force)

