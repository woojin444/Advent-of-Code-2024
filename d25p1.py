key_schematics = []
lock_schematics = []

with open("inputs/d25p12.txt", 'r') as input_file:
    schematic = [0,0,0,0,0]
    lock = None
    for line in input_file:
        line = line.strip()
        if line == "": 
            if lock:
                lock_schematics.append(schematic)
            else:
                schematic = list(map(lambda x: x-1, schematic)) 
                key_schematics.append(schematic)
            lock = None
            schematic = [0,0,0,0,0]
        if lock == None:
            if line == "#####":
                lock = True
            if line == ".....":
                lock = False
        else:
            for i in range(len(line.strip())):
                schematic[i] += 1 if line[i] == "#" else 0

answer = 0

def check_lock_key(lock, key):
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True

for lock in lock_schematics:
    for key in key_schematics:
        if check_lock_key(lock, key): answer += 1

print(len(key_schematics)+len(lock_schematics))
print(answer)