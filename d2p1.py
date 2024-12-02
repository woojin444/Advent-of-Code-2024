def meetsCondition(number1, number2, ascending):
    diff = number1 - number2
    if ascending is None and abs(diff) >= 1 and abs(diff) <= 3:
        return True
    if ascending is True and diff <= -1 and diff >= -3:
        return True
    if ascending is False and diff >= 1 and diff <= 3:
        return True
    return False

def isSafe(report):
    ascending = None
    for i in range(len(report) - 1):
        if report[i] - report[i+1] < 0:
            ascending = True

        for i in range(len(report) - 1):
            if not meetsCondition(report[i], report[i+1], ascending): 
                return False

    return True

safe_reports = 0

with open("inputs/d2p12.txt", "r") as input_file:
    for line in input_file:
        report = [int(x) for x in line.split(" ")]
        l = len(report)

        # First check if the report can even be safe
        if abs(report[0] - report[-1]) > (l-1)*3 or abs(report[0] - report[-1]) < l-1: continue

        # Flag it safe if the array length is 1 or 0
        if l == 1 or l == 0: 
            safe_reports += 1
            continue
        
        safe_reports += 1 if isSafe(report) else 0

print(safe_reports)