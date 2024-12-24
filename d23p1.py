network = {}
with open("inputs/d23p12.txt", "r") as input_file:
    for line in input_file:
        area1, area2 = line.strip().split("-")
        if area1 in network: network[area1].append(area2)
        else: network[area1] = [area2]
        if area2 in network: network[area2].append(area1)
        else: network[area2] = [area1]

triplets = set()
nodes = list(network.keys())

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        for k in range(j + 1, len(nodes)):
            node1, node2, node3 = nodes[i], nodes[j], nodes[k]
            if (node2 in network[node1] and node3 in network[node1] and node3 in network[node2]):
                triplet = tuple(sorted([node1, node2, node3]))
                triplets.add(triplet)

answer = sum(1 for triplet in triplets if any(node.startswith('t') for node in triplet))
print(answer)