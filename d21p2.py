import fileinput, functools

numpad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"]
]
dirpad = [
    [" ", "^", "A"],
    ["<", "v", ">"]
]

def path(pad, start, end):
    start_x, start_y = next((x, y) for y, row in enumerate(pad) for x, column in enumerate(row) if column == start)
    end_x, end_y = next((x, y) for y, row in enumerate(pad) for x, column in enumerate(row) if column == end)
    def g(x, y, s):
        if ( x, y ) == ( end_x, end_y ):       yield s + 'A'
        if end_x < x and pad[y][x - 1] != ' ': yield from g(x - 1, y, s + '<')
        if end_y < y and pad[y - 1][x] != ' ': yield from g(x, y - 1, s + '^')
        if end_y > y and pad[y + 1][x] != ' ': yield from g(x, y + 1, s + 'v')
        if end_x > x and pad[y][x + 1] != ' ': yield from g(x + 1, y, s + '>')
    return min( g( start_x, start_y, "" ),
                key = lambda pad: sum( a != b for a, b in zip( pad, pad[ 1 : ] ) ) )

@functools.cache
def solve(code, loop):
    if loop > 25: return len(code)
    start_end_pairs = zip("A" + code, code)
    total = 0
    for start, end in start_end_pairs:
        pad = dirpad if loop else numpad

        total += solve(path(pad, start, end), loop+1)

    return total

codes = []
with open("inputs/d21p12.txt", "r") as input_file:
    for line in input_file:
        codes.append(line.strip())

print(sum(solve(code, 0) * int(code[:-1]) for code in codes))