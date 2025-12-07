import regex
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


class Range:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}-{self.end}"

# Part One


with open(INPUT_FILE, 'r') as f:
    line = f.readline().strip()
    ranges = []
    for part in line.split(','):
        start, end = part.split('-')
        ranges.append(Range(int(start), int(end)))


def silly_id(code):
    first_half = code[:len(code)//2]
    second_half = code[len(code)//2:]

    if args.verbose:
        print(f"Checking {code}: {first_half} vs {second_half}")

    return first_half == second_half


@timed
def part_one():
    invalid_ids = []
    for r in ranges:
        printable = []
        for code in range(r.start, r.end + 1):
            code_str = str(code)
            if args.verbose:
                print(f"Checking {code_str}")

            if len(code_str) % 2 == 0 and silly_id(code_str):
                invalid_ids.append(code)
                printable.append(code)

        if args.verbose and printable:
            print(f"{r}: {', '.join(map(str, printable))}")

    if args.debug and SOLUTION_DEMO_PART_ONE is not None:
        assert sum(
            invalid_ids) == SOLUTION_DEMO_PART_ONE, f"Expected sum to be {SOLUTION_DEMO_PART_ONE} but got {sum(invalid_ids)}"
    elif SOLUTION_PART_ONE is not None:
        assert sum(
            invalid_ids) == SOLUTION_PART_ONE, f"Expected sum to be {SOLUTION_PART_ONE} but got {sum(invalid_ids)}"

    print(f"Part One: {sum(invalid_ids)}")


@timed
def part_one_regex():
    invalid_sum = 0
    pattern = r'^(\d+)\1$'

    for r in ranges:
        for code in range(r.start, r.end + 1):
            code_str = str(code)
            if args.verbose:
                print(f"Checking {code_str}")
            if regex.match(pattern, code_str):
                invalid_sum += code

    if args.debug and SOLUTION_DEMO_PART_ONE is not None:
        assert invalid_sum == SOLUTION_DEMO_PART_ONE, f"Expected sum to be {SOLUTION_DEMO_PART_ONE} but got {invalid_sum}"
    elif SOLUTION_PART_ONE is not None:
        assert invalid_sum == SOLUTION_PART_ONE, f"Expected sum to be {SOLUTION_PART_ONE} but got {invalid_sum}"

    print(f"Part One: {invalid_sum}")

# Part Two


def split_to(code, parts):
    # create `parts` pairs from code
    try:
        assert len(code) % parts == 0, "Code length must be divisible by parts"
    except AssertionError as e:
        return []
    part_length = len(code) // parts
    return [code[i*part_length:(i+1)*part_length] for i in range(parts)]


def silly_id_part_two(code):
    for check in range(1, len(code) + 1):
        combos = split_to(code, check)
        if args.verbose:
            print(f"\tChecking {code} into {check} parts: {combos}")
        if len(combos) > 1 and all(c == combos[0] for c in combos):
            if args.verbose:
                print(f"\t\tValid: {code} as {combos}")
            return True

    return False


@timed
def part_two():
    invalid_ids = []
    for r in ranges:
        printable = []
        for code in range(r.start, r.end + 1):
            code_str = str(code)
            if args.verbose:
                print(f"Checking {code_str}")
            if silly_id_part_two(code_str) or silly_id(code_str):
                invalid_ids.append(code)
                printable.append(code)
        if args.verbose and printable:
            print(f"{r}: {', '.join(map(str, printable))}")

    if args.debug and SOLUTION_DEMO_PART_TWO is not None:
        assert sum(
            invalid_ids) == SOLUTION_DEMO_PART_TWO, f"Expected sum to be {SOLUTION_DEMO_PART_TWO} but got {sum(invalid_ids)}"
    elif SOLUTION_PART_TWO is not None:
        assert sum(
            invalid_ids) == SOLUTION_PART_TWO, f"Expected sum to be {SOLUTION_PART_TWO} but got {sum(invalid_ids)}"

    print(f"Part Two: {sum(invalid_ids)}")


@timed
def part_two_regex():
    invalid_sum = 0
    pattern = r'^(\d+)\1+$'

    for r in ranges:
        for code in range(r.start, r.end + 1):
            code_str = str(code)
            if args.verbose:
                print(f"Checking {code_str}")
            if regex.match(pattern, code_str):
                invalid_sum += code
    if args.debug and SOLUTION_DEMO_PART_TWO is not None:
        assert invalid_sum == SOLUTION_DEMO_PART_TWO, f"Expected sum to be {SOLUTION_DEMO_PART_TWO} but got {invalid_sum}"
    elif SOLUTION_PART_TWO is not None:
        assert invalid_sum == SOLUTION_PART_TWO, f"Expected sum to be {SOLUTION_PART_TWO} but got {invalid_sum}"

    print(f"Part Two: {invalid_sum}")


if __name__ == "__main__":
    part_one()
    part_two()
