# Parsing input
rules = []
updates = []

with open("inputs/d5p12.txt", "r") as input_file:
    space = False
    for line in input_file:
        if not line.strip(): 
            space = True
        else:
            if space == False: 
                rules.append(line.strip().split("|"))
            else:
                updates.append(line.strip().split(","))

# Creating rulesets: a dictionary with a key that maps to all the possible previous numbers
ruleset = {}

for rule in rules:
    if rule[1] in ruleset:
        ruleset[rule[1]].append(rule[0])
    else:
        ruleset[rule[1]] = [rule[0]]

# Loops through the update in reverse checking that its previous number is in its ruleset dictionary.
# For part 2, it also outputs the index of where it went wrong, if it went wrong.
def is_correct(update):
    for i in reversed(range(len(update))):
        if i == 0: return (True, None)
        if update[i] in ruleset:
            if update[i-1] not in ruleset[update[i]]:
                return (False, i)
            else:
                continue
        else:
            continue

# If it's correct from the beginning, ignore,
# If it's not correct, it swaps the number with its left and checks for correctness again.
# If the there have been any changes and now the update is correct, it adds its middle number.
number = 0

for update in updates:
    changes = 0 
    while True:
        correct, index = is_correct(update)
        if correct:
            if changes != 0:
                number += int(update[int((len(update)-1)/2)])
            break
        else:
            update = [*update[:index-1], update[index], update[index-1], *update[index+1:]]
            changes += 1

print(number)