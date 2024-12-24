from collections import defaultdict

def find_maximum_clique(graph):
    def bron_kerbosch(r, p, x, max_clique):
        if len(p) == 0 and len(x) == 0:
            if len(r) > len(max_clique[0]):
                max_clique[0] = r.copy()
            return
        
        # Choose pivot vertex
        pivot = max(p.union(x), key=lambda u: len(p.intersection(graph[u])), default=None)
        if pivot is None:
            return
            
        # Iterate over vertices not connected to pivot
        for v in p.difference(graph[pivot]):
            new_r = r.union({v})
            new_p = p.intersection(graph[v])
            new_x = x.intersection(graph[v])
            bron_kerbosch(new_r, new_p, new_x, max_clique)
            p.remove(v)
            x.add(v)

    nodes = set(graph.keys())
    max_clique = [set()]  # Using list to allow modification in recursive function
    bron_kerbosch(set(), nodes, set(), max_clique)
    return max_clique[0]

# Process the data
network = {}
with open("inputs/d23p12.txt", "r") as input_file:
    for line in input_file:
        area1, area2 = line.strip().split("-")
        if area1 in network: network[area1].append(area2)
        else: network[area1] = [area2]
        if area2 in network: network[area2].append(area1)
        else: network[area2] = [area1]
max_clique = find_maximum_clique(network)

print("Largest fully-connected network:")
print(f"Size: {len(max_clique)} computers")
print("Computers:", ', '.join(sorted(max_clique)))

password = ','.join(sorted(max_clique))
print(f"Password: {password}")
