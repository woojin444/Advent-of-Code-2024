import re

number = 0
pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

with open("inputs/d3p12.txt", "r") as input_file:
    wholeline = ""
    for line in input_file:
        wholeline += line
    
    # Splitting it by the do() chunks all sections that come right after it
    dosplit = re.split(r"do\(\)", wholeline)
    for chunk in dosplit:
        # Then splitting it by the don't() ensures the first chunk is inbetween a do() and a don't(). The rest are all don't()'s
        dontsplit = re.split(r"don't\(\)", chunk)
        filtered_muls = re.findall(pattern, dontsplit[0])
        for mul in filtered_muls:
            number1, number2 = mul[4:-1].split(",")
            number += int(number1) * int(number2)

print(number)