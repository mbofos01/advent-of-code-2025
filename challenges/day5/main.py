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
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def __str__(self):
        return f"Range({self.start} - {self.end})"


ranges = []
ids = []


with open(INPUT_FILE, 'r') as f:
    content = f.read().strip()

    # Split by empty lines to separate different sections
    sections = content.split('\n\n')

    if args.verbose:
        print(f"Found {len(sections)} sections in input file")
        for i, section in enumerate(sections):
            print(f"Section {i+1}:")
            print(section)
            print()

    # Parse ranges (first section)
    if len(sections) > 0:
        range_lines = sections[0].strip().split('\n')
        for line in range_lines:
            if '-' in line:
                start, end = map(int, line.split('-'))
                ranges.append(Range(start, end))

    # Parse individual numbers (second section)
    if len(sections) > 1:
        number_lines = sections[1].strip().split('\n')
        for line in number_lines:
            if line.strip():
                ids.append(int(line.strip()))

    if args.verbose:
        print(f"Ranges: {[(r.start, r.end) for r in ranges]}")
        print(f"Numbers: {ids}")


@timed
def part_one():
    if args.verbose:
        print("--" * 30)
        print("Starting Part One")
        print("--" * 30)
    count = 0
    for num in ids:
        for r in ranges:
            if r.contains(Range(num, num)):
                count += 1
                if args.verbose:
                    print(f"Number {num} is contained in range {r}")
                break

    if args.debug and SOLUTION_DEMO_PART_ONE is not None:
        assert count == SOLUTION_DEMO_PART_ONE, f"Expected count to be {SOLUTION_DEMO_PART_ONE} but got {count}"
    elif SOLUTION_PART_ONE is not None:
        assert count == SOLUTION_PART_ONE, f"Expected count to be {SOLUTION_PART_ONE} but got {count}"

    print(f"Part One: {count}")


# Part Two
class SoloRange:
    def __init__(self):
        self.ranges = []

    def attach_range(self, new_range):
        if len(self.ranges) == 0:
            self.ranges.append(new_range)
            return

        conflict = False
        empty = False

        for sr in self.ranges:
            if args.verbose:
                print(f"Checking {new_range} against {sr}")
            if sr.start <= new_range.start <= sr.end and new_range.end > sr.end:
                # new range overlaps start of sr
                self.ranges.remove(sr)
                conflict = True
                new_range = Range(sr.start, new_range.end)
                if args.verbose:
                    print("Type 1 conflict")
                    print(f"\tPop {sr} from ranges")
                    print(f"\tUpdate new_range to {new_range}")
                break
            elif sr.start <= new_range.end <= sr.end and new_range.start < sr.start:
                # new range overlaps end of sr
                self.ranges.remove(sr)
                conflict = True
                new_range = Range(new_range.start, sr.end)
                if args.verbose:
                    print("Type 2 conflict")
                    print(f"\tPop {sr} from ranges")
                    print(f"\tUpdate new_range to {new_range}")
                break
            elif sr.start <= new_range.start <= sr.end and sr.start <= new_range.end <= sr.end:
                # new range is completely contained within sr
                conflict = True
                empty = True
                if args.verbose:
                    print("Type 3 conflict")
                break
            elif new_range.start <= sr.start <= new_range.end and new_range.start <= sr.end <= new_range.end:
                # new range completely contains sr
                self.ranges.remove(sr)
                conflict = True
                new_range = Range(new_range.start, new_range.end)
                if args.verbose:
                    print("Type 4 conflict")
                    print(f"\tPop {sr} from ranges")
                    print(f"\tKeep new_range to {new_range}")
                break

        if not conflict:
            self.ranges.append(new_range)
        else:
            if not empty:
                self.attach_range(new_range)

    def find_containing_range(self):
        count = 0
        for r in self.ranges:
            count += r.end - r.start + 1
        return count


@timed
def part_two():
    if args.verbose:
        print("--" * 30)
        print("Starting Part Two")
        print("--" * 30)
    solo_range = SoloRange()

    for r in ranges:
        solo_range.attach_range(r)
    total_covered = solo_range.find_containing_range()

    if args.debug and SOLUTION_DEMO_PART_TWO is not None:
        assert total_covered == SOLUTION_DEMO_PART_TWO, f"Expected total_covered to be {SOLUTION_DEMO_PART_TWO} but got {total_covered}"
    elif SOLUTION_PART_TWO is not None:
        assert total_covered == SOLUTION_PART_TWO, f"Expected total_covered to be {SOLUTION_PART_TWO} but got {total_covered}"

    print(f"Part Two: {total_covered}")


if __name__ == "__main__":
    part_one()
    part_two()
