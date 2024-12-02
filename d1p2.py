list1 = []
list2 = {}

with open("inputs/d1p12.txt", "r") as input_file:
    for line in input_file:
        number1, number2 = line.replace("\n","").split("   ")
        list1.append(int(number1))
        if int(number2) in list2:
            list2[int(number2)] += 1
        else:
            list2[int(number2)] = 1

similarity = 0

for number in list1:
    if number in list2:
        similarity += number*list2[number]

print(similarity)