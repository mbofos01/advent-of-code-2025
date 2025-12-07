import sys
import os
try:
    from solutions import *
except ImportError:
    SOLUTION_DEMO_PART_ONE = None
    SOLUTION_PART_ONE = None
    SOLUTION_DEMO_PART_TWO = None
    SOLUTION_PART_TWO = None
    print("No solutions.py found, skipping solution checks.")

try:
    from tools.timed import timed
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..')))
    from tools.timed import timed

import argparse
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true',
                    help='Use demo.txt instead of input.txt')
parser.add_argument('--verbose', action='store_true',
                    help='Enable verbose output')
args = parser.parse_args()
base_dir = os.path.dirname(os.path.abspath(__file__))
demo_path = os.path.join(base_dir, "demo.txt")
input_path = os.path.join(base_dir, "input.txt")
INPUT_FILE = demo_path if args.debug else input_path


class Grid:
    def __init__(self, file):
        with open(file, 'r') as f:
            self.lines = [line.strip() for line in f.readlines()]

        self.grid = [[char for char in line] for line in self.lines]
        self.visited = [[0 if char == '.' else -1 for char in line]
                        for line in self.lines]
        self.splits = 0
        self.timelines = 0
        self.initial_tachyon = self.locate_tachyon()
        self.visited[self.initial_tachyon[1]][self.initial_tachyon[0]] = 1

    def inbounds(self, x, y):
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def print(self):
        print("====" * 20)
        for row in self.grid:
            print(''.join(str(cell) for cell in row))
        print("====" * 20)

    def print_visited(self):
        print("====" * 20)
        for row in self.visited:
            print(' '.join(f"{cell:<3}" for cell in row))
        print("====" * 20)

    def locate_tachyon(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'S':
                    return (x, y)
        return None

    def deactivate_tachyon(self, x, y):
        if self.inbounds(x, y):
            self.grid[y][x] = 'E'
            if args.verbose:
                print(f"Deactivating tachyon at ({x}, {y}) {self.grid[y][x]}")
            return True
        return False

    def activate_tachyon(self, x, y):
        if self.inbounds(x, y):
            self.grid[y][x] = 'S'
            if args.verbose:
                print(f"Activating tachyon at ({x}, {y}) {self.grid[y][x]}")
            return True
        return False

    def create_new_tachyon(self, x, y):
        if self.inbounds(x, y) and self.grid[y][x] == '.':
            self.grid[y][x] = 'S'
            if args.verbose:
                print(f"Creating new tachyon at ({x}, {y}) {self.grid[y][x]}")
            return True
        return False

    def in_last_row(self, y):
        return y == len(self.grid) - 1

    def go_down(self, x, y):
        if args.verbose:
            print(f"Going down from ({x}, {y}) {self.grid[y][x]}")
        down = (x, y + 1)
        if self.inbounds(*down):
            if self.grid[down[1]][down[0]] == '.':
                if self.grid[y][x] == 'S':
                    self.deactivate_tachyon(x, y)

                self.grid[down[1]][down[0]] = '|'
                self.visited[down[1]][down[0]] = self.visited[y][x]
                self.go_down(x, y + 1)
            elif self.grid[down[1]][down[0]] == '^':
                right = (down[0] + 1, down[1])
                left = (down[0] - 1, down[1])
                if self.inbounds(*right):
                    self.visited[left[1]][left[0]] += self.visited[y][x]
                if self.inbounds(*left):
                    self.visited[right[1]][right[0]] += self.visited[y][x]
                self.create_new_tachyon(*right)
                self.create_new_tachyon(*left)
                self.splits += 1

                if args.verbose:
                    print(
                        f"Hit a booster at ({down[0]}, {down[1]}) split at {right} and {left}")
                self.go_down(*right)
                self.go_down(*left)
            else:
                self.visited[down[1]][down[0]] += self.visited[y][x]

        return

    def get_splits(self):
        return self.splits

    def clean_up(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'E' or cell == 'S':
                    self.grid[y][x] = '|'

        self.activate_tachyon(*self.initial_tachyon)

    def go_down_bfs(self):
        queue = deque()
        queue.append(self.initial_tachyon)

        while queue:
            if args.verbose:
                self.print_visited()
                input("Press Enter to continue...")
            x, y = queue.popleft()
            if args.verbose:
                print(f"Processing ({x}, {y}) {self.grid[y][x]}")
            down = (x, y + 1)
            if self.inbounds(*down):
                if self.grid[down[1]][down[0]] == '.':
                    if self.grid[y][x] == 'S':
                        self.deactivate_tachyon(x, y)

                    self.grid[down[1]][down[0]] = '|'
                    self.visited[down[1]][down[0]] += self.visited[y][x]
                    queue.append(down)
                elif self.grid[down[1]][down[0]] == '^':
                    right = (down[0] + 1, down[1])
                    left = (down[0] - 1, down[1])
                    if self.inbounds(*right):
                        self.visited[left[1]][left[0]] += self.visited[y][x]
                    if self.inbounds(*left):
                        self.visited[right[1]][right[0]] += self.visited[y][x]
                    self.create_new_tachyon(*left)
                    self.create_new_tachyon(*right)
                    self.splits += 1

                    if args.verbose:
                        print(
                            f"Hit a booster at ({down[0]}, {down[1]}) split at {right} and {left}")
                    queue.append(left)
                    queue.append(right)
                    
                elif self.grid[down[1]][down[0]] == '|':
                    continue
                else:
                    self.visited[down[1]][down[0]] += self.visited[y][x]

        for item in self.visited[-1]:
            if item > 0:
                self.timelines += item

# Part One


@timed
def part_one(grid: Grid):
    # Use BFS instead of DFS
    grid.go_down(*grid.initial_tachyon)

    if args.verbose:
        grid.clean_up()
        grid.print()

    splits = grid.get_splits()

    if SOLUTION_DEMO_PART_ONE is not None and args.debug:
        assert splits == SOLUTION_DEMO_PART_ONE, f"Expected {SOLUTION_DEMO_PART_ONE}, got {splits}"
    elif SOLUTION_PART_ONE is not None and not args.debug:
        assert splits == SOLUTION_PART_ONE, f"Expected {SOLUTION_PART_ONE}, got {splits}"

    print(f"Part One: {splits}")


# Part Two
@timed
def part_two(grid: Grid):
    grid.go_down_bfs()

    if args.verbose:
        grid.clean_up()
        grid.print()

    timelines = grid.timelines

    if SOLUTION_DEMO_PART_TWO is not None and args.debug:
        assert timelines == SOLUTION_DEMO_PART_TWO, f"Expected {SOLUTION_DEMO_PART_TWO}, got {timelines}"
    elif SOLUTION_PART_TWO is not None and not args.debug:
        assert timelines == SOLUTION_PART_TWO, f"Expected {SOLUTION_PART_TWO}, got {timelines}"

    print(f"Part Two: {timelines}")


if __name__ == '__main__':
    grid = Grid(INPUT_FILE)
    part_one(grid)
    grid = Grid(INPUT_FILE)
    part_two(grid)
