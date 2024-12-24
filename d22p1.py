buyers = []
with open("inputs/d22p12.txt", "r") as input_file:
    for line in input_file:
        buyers.append(int(line.strip()))

def mix(secret: int, result: int) -> int:
    return result ^ secret

def prune(secret: int) -> int:
    return secret % 16777216

def evolve(secret: int) -> int:
    step1 = secret * 64
    secret = prune(mix(secret=secret, result=step1))
    
    step2 = int(secret / 32)
    secret = prune(mix(secret=secret, result=step2))

    step3 = secret * 2048
    secret = prune(mix(secret=secret, result=step3))

    return secret

answer = 0

for buyer in buyers:
    for _ in range(2000):
        buyer = evolve(buyer)
    answer += buyer

print(answer)