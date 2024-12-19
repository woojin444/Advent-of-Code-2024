class Computer:
    def __init__(self):
        self.pointer = 0
        self.register = {"A": 0, "B": 0, "C": 0}
        self.program = []
        self.output = []

    def assign_program(self, program: list[int]):
        self.program = program

    def combo_operand(self, operand: int) -> int:
        if operand in [0,1,2,3]: return operand
        elif operand == 4: return self.register["A"]
        elif operand == 5: return self.register["B"]
        elif operand == 6: return self.register["C"]
        else: return 0

    def run(self):
        # opcode 0: register_a DIVIDED by (combo operand)^2 -> int to register_a
        # opcode 1: bitwise XOR with register_b and (literal operand) -> int to register_b
        # opcode 2: (combo operand) % 8 -> int to register_b
        # opcode 3: nothing if regtister_a == 0, else: pointer = (literal operand)
        # opcode 4: bitwise XOR of register_b and register_c -> int to register_b. Ignore (literal operand)
        # opcode 5: (combo operand) % 8 -> output separated by commas if multiple values
        # opcode 6: register_a DIVIDED by (combo operand)^2 -> int to register_b
        # opcode 7: register_a DIVIDED by (combo operand)^2 -> int to register_c
        if self.pointer >= len(self.program): return ",".join(map(str, self.output))
        opcode = self.program[self.pointer]
        self.pointer += 1
        operand = self.program[self.pointer]
        self.pointer += 1

        if opcode == 0:
            self.register["A"] = int(self.register["A"] / pow(2, self.combo_operand(operand)))
        elif opcode == 1:
            self.register["B"] = self.register["B"] ^ operand
        elif opcode == 2:
            self.register["B"] = self.combo_operand(operand) % 8
        elif opcode == 3:
            if self.register["A"] != 0:
                self.pointer = operand
        elif opcode == 4:
            self.register["B"] = self.register["B"] ^ self.register["C"]
        elif opcode == 5:
            self.output.append(self.combo_operand(operand) % 8)
        elif opcode == 6:
            self.register["B"] = int(self.register["A"] / pow(2, self.combo_operand(operand)))
        elif opcode == 7:
            self.register["C"] = int(self.register["A"] / pow(2, self.combo_operand(operand)))
        else:
            print("Opcode Error")
        return self.pointer

computer = Computer()

with open("inputs/d17p12.txt") as input_file:
    lines = input_file.readlines()
    computer.register["A"] = int(lines[0].split(" ")[2].strip())
    computer.register["B"] = int(lines[1].split(" ")[2].strip())
    computer.register["C"] = int(lines[2].split(" ")[2].strip())
    computer.assign_program(list(map(int, lines[4].split(" ")[1].split(","))))


while True:
    result = computer.run()
    if type(result) != int:
        if result == ",".join(map(str, computer.program)):
            print(a)
        else: print(f"a={a}: {result}")
        break

