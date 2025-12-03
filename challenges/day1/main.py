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

# Part One


def move_to(position, direction, distance):
    if direction == "L":
        position -= distance
    elif direction == "R":
        position += distance
    position = position % 100
    return position


with open(INPUT_FILE) as f:
    rotations = f.read().strip().split("\n")


@timed
def part_one():
    starting_position = 50
    zero_moments = 0
    if args.debug:
        SOLUTION = 3
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        starting_position = move_to(starting_position, direction, distance)
        if starting_position == 0:
            zero_moments += 1
            
    if args.debug:
        assert zero_moments == SOLUTION, f"Expected {SOLUTION} zero moments, got {zero_moments}"

    print(f"Part One: {zero_moments}")


# Part Two


def move_to_part_two(position, direction, distance):
    zeros = 0
    for _ in range(distance):
        if direction == "L":
            position = (position - 1) % 100
        elif direction == "R":
            position = (position + 1) % 100
        if position == 0:
            zeros += 1
    return position, zeros


with open(INPUT_FILE) as f:
    rotations = f.read().strip().split("\n")


@timed
def part_two():
    starting_position = 50
    zero_moments = 0
    if args.debug:
        SOLUTION = 6
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        starting_position, zeros = move_to_part_two(
            starting_position, direction, distance)
        zero_moments += zeros
    
    if args.debug:
        assert zero_moments == SOLUTION, f"Expected {SOLUTION} zero moments, got {zero_moments}"

    print(f"Part Two: {zero_moments}")


if __name__ == "__main__":
    part_one()
    part_two()
