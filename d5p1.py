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
def is_correct(update):
    for i in reversed(range(len(update))):
        if i == 0: return True
        if update[i] in ruleset:
            if update[i-1] not in ruleset[update[i]]:
                return False
            else:
                continue
        else:
            continue

number = 0

for update in updates:
    if is_correct(update): number += int(update[int((len(update)-1)/2)])

print(number)