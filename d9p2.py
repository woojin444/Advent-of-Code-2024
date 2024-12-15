disk_map = []

with open("inputs/d9p12.txt") as input_file:
    disk_map = list(input_file.read().strip())

disk = []
number = 0
for i in range(len(disk_map)):
    repeat = int(disk_map[i])
    if i % 2 == 0:
        for j in range(repeat):
            disk.append(number)
        number += 1
    else:
        for j in range(repeat):
            disk.append(".")

def find_chunks(disk: list, type: str) -> list:
    current_index = 0
    end_index = 0
    chunks = []
    while current_index < len(disk):
        if type == "empty":
            if disk[current_index] == ".":
                end_index = current_index
                while end_index < len(disk) and disk[end_index] == ".":
                    end_index += 1
                chunks.append((current_index, end_index-1))
                current_index = end_index
            else:
                current_index += 1
        elif type == "number":
            if disk[current_index] != ".":
                n = disk[current_index]
                end_index = current_index
                while end_index < len(disk) and disk[end_index] == n:
                    end_index += 1
                chunks.append((current_index, end_index-1))
                current_index = end_index
            else:
                current_index += 1
        else:
            print("Type Error.")

    return chunks

def disk_len(disk_indices: tuple[int, int]) -> int:
    return disk_indices[1] - disk_indices[0] + 1

def condense_disk(disk: list, empty_chunks: list, number_chunks: list) -> list:
    # While going backwards on the number chunks,
    for number_chunk in reversed(number_chunks):
        # and while checking all the empty chunks with ending index to be lower than the starting index of the number chunk,
        empty_chunk_index = 0
        while empty_chunk_index < len(empty_chunks) and empty_chunks[empty_chunk_index][1] < number_chunk[0]:
            # if the empty chunk has more or equal space than the number chunk,
            empty_chunk = empty_chunks[empty_chunk_index]
            if disk_len(empty_chunk) >= disk_len(number_chunk):
                # Replace the dots with those numbers and then replace those numbers with dots.
                for empty in range(empty_chunk[0], empty_chunk[0]+disk_len(number_chunk)):
                    disk[empty] = disk[number_chunk[0]]
                # Update the empty chunk to the correct size after number movement.
                if disk_len(empty_chunk) == disk_len(number_chunk):
                    empty_chunks.pop(empty_chunk_index)
                else:
                    empty_chunks[empty_chunk_index] = (empty_chunk[0] + disk_len(number_chunk), empty_chunk[1])
                # Update the last numbers with "."'s
                for number in range(number_chunk[0], number_chunk[1]+1):
                    disk[number] = "."
                break
            else:
                empty_chunk_index += 1
    
    return disk

dense_disk = condense_disk(disk, find_chunks(disk, "empty"), find_chunks(disk, "number"))

answer = 0
number = 0

for n in dense_disk:
    if n != ".": answer += number * int(n)
    number += 1

print(answer)