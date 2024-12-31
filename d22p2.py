from alive_progress import alive_bar

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

total_profits = {}

with alive_bar(len(buyers)) as bar:
    for buyer in buyers:
        prices = [buyer]
        profits = {}
        for _ in range(2000):
            prices.append(evolve(prices[-1]))
        look_back = 4
        for i in range(look_back, len(prices)):
            # imN = (i minus N)th number's ones digit
            price_block = [prices[i-n] % 10 for n in reversed(range(look_back+1))]
            changes = "".join(map(str, [after - before for before, after in zip(price_block, price_block[1:])]))
            if changes not in profits:
                profits[changes] = price_block[-1]
        for changes in profits:
            if changes in total_profits:
                total_profits[changes] += profits[changes]
            else:
                total_profits[changes] = profits[changes]
        bar()

max_sequence = max(total_profits, key=total_profits.get)
max_banana = total_profits[max_sequence]
print(max_sequence, max_banana)