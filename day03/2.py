from argparse import ArgumentParser
from collections import Counter
import re

UNOCCUPIED = None
DOUBLE = -1


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


class Grid():
    def __init__(self, width, height):
        self.cells = [
            [None] * height
            for _ in range(width)
        ]
        self.requested_squares_map = {}

    def count_overlapping(self):
        return sum(
            sum(1 for entry in row if entry == DOUBLE)
            for row in self.cells
        )

    def claim_cells(self, claim_index, position, size):
        start_w, start_h = position
        size_w, size_h = size

        self.requested_squares_map[claim_index] = size_w * size_h

        for w_index in range(start_w, start_w + size_w):
            for h_index in range(start_h, start_h + size_h):
                if self.cells[w_index][h_index] == UNOCCUPIED:
                    self.cells[w_index][h_index] = claim_index
                else:
                    self.cells[w_index][h_index] = DOUBLE

    def set_occupancy_map(self):
        occupancy_map = Counter()
        for col in self.cells:
            for entry in col:
                if entry != UNOCCUPIED and entry != DOUBLE:
                    occupancy_map[entry] += 1

        self.occupancy_map = occupancy_map

    @staticmethod
    def parse_claim(line):
        matches = re.match(
            r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line
        ).groups()
        claim_index, pos_w, pos_h, size_w, size_h = map(int, matches)

        return claim_index, (pos_w, pos_h), (size_w, size_h)

    def print_grid(self):
        for row in self.cells:
            for col in row:
                if col == UNOCCUPIED:
                    print('.', end='')
                elif col == DOUBLE:
                    print('X', end='')
                else:
                    print(col, end='')
            print()


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()
    claims = [Grid.parse_claim(line) for line in data]

    grid = Grid(1000, 1000)
    for claim in claims:
        grid.claim_cells(*claim)

    grid.set_occupancy_map()
    for claim_id in grid.occupancy_map.keys():
        match = (
            grid.occupancy_map[claim_id] ==
            grid.requested_squares_map[claim_id]
        )
        if match:
            print(claim_id)
            break
    else:
        print('No overlapping claims found!')


if __name__ == '__main__':
    main()
