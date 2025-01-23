import re

nodes = {}
gates = {}

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
            gates[split_line[4]] = split_line[0:3]

z_gates = {}

def expand_gate(gates, gate: str) -> str:
    if gate.startswith('x') or gate.startswith('y'):
        return gate
    else:
        resulting_gate = gates[gate]
        return (f"({expand_gate(gates, resulting_gate[0])} {resulting_gate[1]} {expand_gate(gates, resulting_gate[2])})")

for gate in gates.keys():
    if gate.startswith('z'):
        resulting_gate = gates[gate]
        z_gates[gate] = f"({expand_gate(gates, resulting_gate[0])} {resulting_gate[1]} {expand_gate(gates, resulting_gate[2])})"

pattern = r'[xy]\d{2}'

for gate, result in sorted(z_gates.items()):
    temp = None
    for item in result.split(" "):
        matches = re.findall(pattern, item)
        if len(matches) > 0:
            if temp == None:
                temp = matches[0]
            else:
                if temp[0] != matches[0][0] and temp[1:] == matches[0][1:]:
                    temp = None
                else:
                    print(f"{gate}: {temp}, {matches[0]}")
                    # print(f"{gate}: {result}")
    print(gate, result)

from operator import xor as XOR, or_ as OR, and_ as AND

lines = [l.split() for l in open('inputs/d24p12.txt') if '->' in l]

r = lambda c, y: any(y == x and c in (a, b) for a, x, b, _, _ in lines)

print(*sorted(c for a, x, b, _, c in lines if
    x == "XOR" and all(d[0] not in 'xyz' for d in (a, b, c)) or
    x == "AND" and not "x00" in (a, b) and r(c, 'XOR') or
    x == "XOR" and not "x00" in (a, b) and r(c, 'OR') or
    x != "XOR" and c[0] == 'z' and c != "z45"), sep=',')