# Insort adds items into a sorted array without losing sort. Time complexity of O(log n)
def insort(sorted_array, number):
    low, high = 0, len(sorted_array)
    while low < high:
        mid = (low + high) // 2
        if sorted_array[mid] < number:
            low = mid + 1
        else:
            high = mid
    
    sorted_array.insert(low, number)

list1 = []
list2 = []

# Goes through the list once and creates a sorted list
with open("inputs/d1p12.txt", "r") as input_file:
    for line in input_file:
        number1, number2 = line.replace("\n","").split("   ")
        insort(list1, int(number1))
        insort(list2, int(number2))


# Adds the differences
difference = 0

for i in range(len(list1)):
    difference += abs(list1[i]-list2[i])

# Final time complexity of O(nlog n)
print(difference)