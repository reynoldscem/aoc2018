from argparse import ArgumentParser
from itertools import cycle


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()
    updates = cycle(map(int, data))

    frequency = 0
    seen = set()
    seen.add(frequency)

    for update in updates:
        frequency += update
        if frequency in seen:
            print(frequency)
            break
        seen.add(frequency)


if __name__ == '__main__':
    main()
