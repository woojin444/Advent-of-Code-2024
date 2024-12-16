import re
from fractions import Fraction

class Game:
    def __init__(self, ax: int, ay: int, bx: int, by: int, px: int, py: int):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py
    
    def find_optimal_presses(self):
        # Given they're vectors of positive numbers and that the prize is also in the positives,
        # the angle of the sum of the button A and button B vector must match the angle of the Prize vector.
        # If A = (Ax, Ay), B = (Bx, By), P = (Px, Py), we want arctan(nA + mB) = arctan(P) where n, m are integers (button presses)
        # (nAy + mBy)/(nAx + mBx) = Py/Px
        # Px(nAy + mBy) = Py(nAx + mBx)
        # nPxAy + mPxBy = nPyAx + mPyBx
        # n(PxAy - PyAx) = m(PyBx - PxBy)
        # n = m * (PyBx - PxBy)/(PxAy - PyAx)
        ratio = Fraction(self.py*self.bx - self.px*self.by,self.px*self.ay - self.py*self.ax)
        required_A = ratio.numerator
        required_B = ratio.denominator
        while required_A <= 100 and required_B <= 100:
            x_position = required_A*self.ax + required_B*self.bx
            y_position = required_A*self.ay + required_B*self.by
            if x_position == self.px and y_position == self.py:
                return (required_A, required_B)
            elif x_position > self.px or y_position > self.py: 
                return (0,0)
            else:
                required_A = required_A + ratio.numerator
                required_B = required_B + ratio.denominator
        return (0,0)

games = []

with open("inputs/d13p12.txt", "r") as input_file:
    while True:
        lines = [input_file.readline() for _ in range(4)]
        if not any(lines):
            break
        button_pattern_X = r'X\+(-?\d+)'
        button_pattern_Y = r'Y\+(-?\d+)'
        prize_pattern_X = r'X=(-?\d+)'
        prize_pattern_Y = r'Y=(-?\d+)'
        game = Game(ax=int(re.search(button_pattern_X, lines[0]).group(1)),\
                    ay=int(re.search(button_pattern_Y, lines[0]).group(1)),\
                    bx=int(re.search(button_pattern_X, lines[1]).group(1)),\
                    by=int(re.search(button_pattern_Y, lines[1]).group(1)),\
                    px=int(re.search(prize_pattern_X, lines[2]).group(1)),\
                    py=int(re.search(prize_pattern_Y, lines[2]).group(1)))
        games.append(game)

answer = 0
for game in games:
    optimal_presses = game.find_optimal_presses()
    if optimal_presses != (0,0):
        answer += 3*optimal_presses[0] + optimal_presses[1]

print(answer)

