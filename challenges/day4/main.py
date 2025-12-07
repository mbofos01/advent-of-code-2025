import argparse
import sys
import os
import time
import sys

# Try to import colorama for better cross-platform terminal control
try:
    import colorama
    from colorama import Cursor
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    print("Install colorama for better visualization: pip install colorama")

# ANSI color codes


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


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

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true',
                    help='Use demo.txt instead of input.txt')
parser.add_argument('--verbose', action='store_true',
                    help='Enable verbose output')
parser.add_argument('--visualize', action='store_true',
                    help='Show real-time grid visualization')
parser.add_argument('--delay', type=float, default=0.5,
                    help='Delay between visualization updates (seconds)')
args = parser.parse_args()
base_dir = os.path.dirname(os.path.abspath(__file__))
demo_path = os.path.join(base_dir, "demo.txt")
input_path = os.path.join(base_dir, "input.txt")
INPUT_FILE = demo_path if args.debug else input_path


class Grid:
    def __init__(self, file, roll_char='@', marked_char='x', empty_char='.', threshold=4):
        with open(file, 'r') as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.height = len(self.lines)
        self.width = len(self.lines[0]) if self.height > 0 else 0
        if args.verbose:
            print(f"Grid loaded with dimensions: {self.width}x{self.height}")
        self.grid = [[char for char in line] for line in self.lines]
        self.ROLL = roll_char
        self.MARKED = marked_char
        self.EMPTY = empty_char
        self.THRESHOLD = threshold

    def height(self):
        return self.height

    def width(self):
        return self.width

    def __str__(self):
        return '\n'.join(''.join(str(cell) for cell in row) for row in self.grid)

    def inbounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x, y):
        if self.inbounds(x, y):
            return self.grid[y][x]
        else:
            return None

    def set_cell(self, x, y, value):
        if self.inbounds(x, y):
            self.grid[y][x] = value

    def check_neighbors(self, x, y):
        neighbors = 0
        directions_x_y = [(-1, 0), (1, 0), (0, -1), (0, 1)
                          ]  # left, right, up, down
        for dx, dy in directions_x_y:
            nx, ny = x + dx, y + dy
            if self.inbounds(nx, ny) and (self.get_cell(nx, ny) == self.MARKED or self.get_cell(nx, ny) == self.ROLL):
                neighbors += 1

        directions_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
        for dx, dy in directions_diag:
            nx, ny = x + dx, y + dy
            if self.inbounds(nx, ny) and (self.get_cell(nx, ny) == self.MARKED or self.get_cell(nx, ny) == self.ROLL):
                neighbors += 1

        return neighbors

    def is_rollable(self, x, y):
        if not self.inbounds(x, y):
            return False

        cell = self.get_cell(x, y)
        if cell == self.ROLL:
            neighbors = self.check_neighbors(x, y)
            return neighbors < self.THRESHOLD

    def mark_cell(self, x, y):
        self.set_cell(x, y, self.MARKED)

    def empty_cell(self, x, y):
        self.set_cell(x, y, self.EMPTY)

    def clean_up(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) == self.MARKED:
                    self.empty_cell(x, y)

    def display(self, clear=True, round_num=0, rollable_count=0, total_rolled=0):
        if args.visualize:
            if clear:
                if HAS_COLORAMA:
                    # Move cursor to home position and clear from cursor to end of screen
                    print('\033[H\033[J', end='')
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')

            # Header with round info
            print(
                f"{Colors.BOLD}{Colors.CYAN}═══ Advent of Code 2025 - Day 4 ═══{Colors.RESET}")
            if round_num > 0:
                print(
                    f"{Colors.YELLOW}Round: {round_num} | This round: {rollable_count} | Total: {total_rolled}{Colors.RESET}")
            print()

            # Display grid with colors
            for row in self.grid:
                line = ""
                for cell in row:
                    if cell == self.ROLL:
                        line += f"{Colors.GREEN}{cell}{Colors.RESET}"
                    elif cell == self.MARKED:
                        line += f"{Colors.RED}{cell}{Colors.RESET}"
                    elif cell == self.EMPTY:
                        line += f"{Colors.WHITE}{cell}{Colors.RESET}"
                    else:
                        line += cell
                print(line)

            print(f"\n{Colors.BLUE}Grid: {self.width}x{self.height}{Colors.RESET}")
            print(f"{Colors.GREEN}@ = Rollable{Colors.RESET} | {Colors.RED}x = Marked{Colors.RESET} | {Colors.WHITE}. = Empty{Colors.RESET}")

            sys.stdout.flush()  # Ensure immediate output
            time.sleep(args.delay)

# Part One


@timed
def part_one(grid: Grid):
    sum_rollable = 0

    if args.visualize:
        grid.display(round_num=1, rollable_count=0, total_rolled=0)

    for y in range(grid.height):
        for x in range(grid.width):
            if grid.is_rollable(x, y):
                grid.mark_cell(x, y)
                if args.verbose:
                    print(f"Rollable cell found at ({x}, {y})")
                sum_rollable += 1

    if args.visualize:
        grid.display(round_num=1, rollable_count=sum_rollable,
                     total_rolled=sum_rollable)

    if args.debug and SOLUTION_DEMO_PART_ONE is not None:
        assert sum_rollable == SOLUTION_DEMO_PART_ONE, f"Expected {SOLUTION_DEMO_PART_ONE} rollable cells, but found {sum_rollable}"
    elif SOLUTION_PART_ONE is not None:
        assert sum_rollable == SOLUTION_PART_ONE, f"Expected {SOLUTION_PART_ONE} rollable cells, but found {sum_rollable}"

    print(f"Part One: {sum_rollable}")


# Part Two
@timed
def part_two(grid: Grid):
    sum_rollable = 0
    rollable = 1
    round_count = 0

    if args.visualize:
        grid.display(round_num=0, rollable_count=0, total_rolled=0)

    while rollable != 0:
        rollable = 0
        round_count += 1
        round_rollable = 0

        for y in range(grid.height):
            for x in range(grid.width):
                if grid.is_rollable(x, y):
                    rollable += 1
                    round_rollable += 1
                    grid.mark_cell(x, y)
                    if args.verbose:
                        print(f"Rollable cell found at ({x}, {y})")
                    sum_rollable += 1

        if args.visualize:
            grid.display(round_num=round_count,
                         rollable_count=round_rollable, total_rolled=sum_rollable)

        grid.clean_up()

        if args.visualize and rollable > 0:
            grid.display(round_num=round_count,
                         rollable_count=round_rollable, total_rolled=sum_rollable)

    if args.debug and SOLUTION_DEMO_PART_TWO is not None:
        assert sum_rollable == SOLUTION_DEMO_PART_TWO, f"Expected {SOLUTION_DEMO_PART_TWO} rollable cells, but found {sum_rollable}"
    elif SOLUTION_PART_TWO is not None:
        assert sum_rollable == SOLUTION_PART_TWO, f"Expected {SOLUTION_PART_TWO} rollable cells, but found {sum_rollable}"

    print(f"Part Two: {sum_rollable}")


if __name__ == '__main__':
    grid = Grid(INPUT_FILE)
    part_one(grid)
    grid = Grid(INPUT_FILE)
    part_two(grid)
