def insort(sorted_list, number):
    low, high = 0, len(sorted_list)
    while low < high:
        mid = (low + high) // 2
        if sorted_list[mid] < number:
            low = mid + 1
        else:
            high = mid
    
    sorted_list.insert(low, number)

list1 = []
list2 = []

with open("inputs/d1p12.txt", "r") as input_file:
    for line in input_file:
        number1, number2 = line.replace("\n","").split("   ")
        insort(list1, int(number1))
        insort(list2, int(number2))

difference = 0

for i in range(len(list1)):
    difference += abs(list1[i]-list2[i])

print(difference)