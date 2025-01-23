nodes = {}
gates = []

with open("inputs/d24p12.txt", "r") as input_file:
    gate_flag = False
    for line in input_file:
        if line == "\n": 
            gate_flag = True
            continue
        if not gate_flag:
            node, value = line.replace("\n","").split(": ")
            nodes[node] = int(value)
        else:
            split_line = line.replace("\n","").split(" ")
            gates.append((split_line[0], split_line[1], split_line[2], split_line[4]))

while len(gates) > 0:
    gate = gates.pop(0)
    if gate[0] in nodes and gate[2] in nodes:
        if gate[1] == "XOR": nodes[gate[3]] = nodes[gate[0]] ^ nodes[gate[2]]
        elif gate[1] == "AND": nodes[gate[3]] = nodes[gate[0]] and nodes[gate[2]]
        elif gate[1] == "OR": nodes[gate[3]] = nodes[gate[0]] or nodes[gate[2]]
    else:
        gates.append(gate)

x_binary = "".join(map(str,[nodes[x_node] for x_node in reversed(sorted([node for node in nodes if node.startswith('x')]))]))
y_binary = "".join(map(str,[nodes[y_node] for y_node in reversed(sorted([node for node in nodes if node.startswith('y')]))]))
z_binary = "".join(map(str,[nodes[z_node] for z_node in reversed(sorted([node for node in nodes if node.startswith('z')]))]))

print(int(z_binary, 2))