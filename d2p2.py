def meetsCondition(number1, number2, ascending):
    diff = number1 - number2
    if ascending is None and abs(diff) >= 1 and abs(diff) <= 3:
        return True
    if ascending is True and diff <= -1 and diff >= -3:
        return True
    if ascending is False and diff >= 1 and diff <= 3:
        return True
    return False

safe_reports = 0

def is_safe_with_dampener(checked, report, ascending=None, dampened=False):
    # If the report check is at the end then auto pass.
    if len(report) == 1: return True
    if len(report) == 2 and dampened == False: return True

    # Setting ascend flag
    if ascending == None: ascending = True if report[0] - report[1] < 0 else False

    # If the condition isn't met at any point then start the check again with the number or the neighbours removed.
    if not meetsCondition(report[0], report[1], ascending):
        if dampened: return False
        return is_safe_with_dampener(checked=[], report=[*checked, *report[1:]], ascending=None, dampened=True) \
            or is_safe_with_dampener(checked=[], report=[*checked[:-1], *report], ascending=None, dampened=True) \
            or is_safe_with_dampener(checked=[], report=[*checked, report[0], *report[2:]], ascending=None, dampened=True)
    else:
        return is_safe_with_dampener([*checked, report[0]], report[1:], ascending=True if report[0] - report[1] < 0 else False, dampened=dampened)

with open("inputs/d2p12.txt", "r") as input_file:
    for line in input_file:
        report = [int(x) for x in line.split(" ")]
        
        safe_reports += 1 if is_safe_with_dampener(checked=[], report=report, ascending=None, dampened=False) else 0

print(safe_reports)