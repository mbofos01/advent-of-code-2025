import sys
import os

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

def find_joltage(bank: str, tail: int) -> int:
    for search in range(9, 0, -1):
        for index in range(len(bank) - tail):  # leave last digit
            if int(bank[index]) == search:
                return index


with open(INPUT_FILE, 'r') as f:
    banks = [line.strip() for line in f.readlines()]

# Part One


@timed
def part_one():
    SUM = 0
    DIGITS = 2
    SOLUTION = 357

    for bank in banks:
        if args.verbose:
            print(f"Processing bank: {bank}")

        tail = 1
        first_index = find_joltage(bank, tail)
        if args.verbose:
            print(f"\t\tFirst Index: {first_index} Value: {bank[first_index]}")
            print(f"\tNew Bank: {bank[first_index+1:]}")
        tail -= 1
        second_index = find_joltage(
            bank[first_index+1:], tail) + first_index + 1
        if args.verbose:
            print(
                f"\t\tSecond Index: {second_index} Value: {bank[second_index]}")
        if args.verbose:
            print(
                f"Max joltage for bank {bank}: {bank[first_index]}{bank[second_index]}")

        SUM += int(f"{bank[first_index]}{bank[second_index]}")

    if args.debug:
        assert SUM == SOLUTION, f"Expected SUM to be {SOLUTION} but got {SUM}"

    print(f"Part One: {SUM}")


# Part Two

def find_joltage_recursively(bank: str, to_pick: int) -> str:
    if to_pick == 0:
        return ""
    first_index = find_joltage(bank, to_pick - 1)
    if args.verbose:
        print(f"\t\tIndex: {first_index} Value: {bank[first_index]}")
        print(f"\tNew Bank: {bank[first_index+1:]}")
    return bank[first_index] + find_joltage_recursively(bank[first_index+1:], to_pick - 1)


with open(INPUT_FILE, 'r') as f:
    banks = [line.strip() for line in f.readlines()]


@timed
def part_two():
    SUM = 0
    DIGITS = 12
    if args.debug:
        SOLUTION = 3121910778619
    for bank in banks:
        if args.verbose:
            print(f"Processing bank: {bank}")
        joltage_str = find_joltage_recursively(bank, DIGITS)
        if args.verbose:
            print(f"Max joltage for bank {bank}: {joltage_str}")
        SUM += int(joltage_str)

    if args.debug:
        assert SUM == SOLUTION, f"Expected SUM to be {SOLUTION} but got {SUM}"

    print(f"Part Two: {SUM}")


if __name__ == "__main__":
    part_one()
    part_two()
