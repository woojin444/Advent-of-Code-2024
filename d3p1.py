import re

number = 0
pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

with open("inputs/d3p12.txt", "r") as input_file:
    for line in input_file:
        filtered_muls = re.findall(pattern, line)
        for mul in filtered_muls:
            number1, number2 = mul[4:-1].split(",")
            number += int(number1) * int(number2)

print(number)