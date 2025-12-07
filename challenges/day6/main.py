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

# Part One


@timed
def part_one():
    operations = len([item for item in lines[0].split() if item])
    operators = lines[-1].split()
    numbers = [[] for _ in range(operations)]
    for line in lines[:-1]:
        index = 0
        for item in line.split(" "):
            if item.isdigit():
                numbers[index].append(int(item))
                index += 1

    results = []
    for index, sign in enumerate(operators):
        if sign == "+":
            results.append(sum(numbers[index][:]))
        elif sign == "*":
            result = 1
            for num in numbers[index]:
                result *= num
            results.append(result)

    sum_total = sum(results)

    if args.debug and SOLUTION_DEMO_PART_ONE is not None:
        assert sum_total == SOLUTION_DEMO_PART_ONE, f"Expected {SOLUTION_DEMO_PART_ONE}, got {sum_total}"
    elif SOLUTION_PART_ONE is not None:
        assert sum_total == SOLUTION_PART_ONE, f"Expected {SOLUTION_PART_ONE}, got {sum_total}"

    print(f"Part One: {sum_total}")

# Part Two


@timed
def part_two():
    sum_total = 0
    operators = lines[-1].split()
    if args.verbose:
        print(f"Operators: {operators}")

    op_index = len(operators) - 1
    values = []
    for j in range(len(lines[0]), 0, -1):
        num = 0
        for i in range(len(lines[:-1])):
            if lines[i][j-1].isdigit():
                num = num + \
                    10 ** (len(lines[:-1]) - i - 1) * int(lines[i][j-1])
            elif lines[i][j-1].isspace():
                num = int(num / 10)
        if num == 0:
            if operators[op_index] == "+":
                if args.verbose:
                    print(f"Adding values: {values}")
                sum_total += sum(values)
            elif operators[op_index] == "*":
                if args.verbose:
                    print(f"Multiplying values: {values}")
                result = 1
                for val in values:
                    result *= val
                sum_total += result
            op_index -= 1
            values = []
        else:
            values.append(num)
    else:
        if operators[op_index] == "+":
            if args.verbose:
                print(f"Adding values: {values}")
            sum_total += sum(values)
        elif operators[op_index] == "*":
            if args.verbose:
                print(f"Multiplying values: {values}")
            result = 1
            for val in values:
                result *= val
            sum_total += result

    if args.debug and SOLUTION_DEMO_PART_TWO is not None:
        assert sum_total == SOLUTION_DEMO_PART_TWO, f"Expected {SOLUTION_DEMO_PART_TWO}, got {sum_total}"
    elif SOLUTION_PART_TWO is not None:
        assert sum_total == SOLUTION_PART_TWO, f"Expected {SOLUTION_PART_TWO}, got {sum_total}"

    print(f"Part Two: {sum_total}")


if __name__ == "__main__":

    with open(INPUT_FILE, 'r') as f:
        lines = f.read().strip().splitlines()

    part_one()
    part_two()
