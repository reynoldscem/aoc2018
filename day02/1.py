from argparse import ArgumentParser
from collections import Counter


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def count_duplicates(strings, number_required):
    return sum(
        1 if number_required in Counter(string).values() else 0
        for string in strings
    )


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()

    checksum = (
        count_duplicates(data, 2) *
        count_duplicates(data, 3)
    )

    print(checksum)


if __name__ == '__main__':
    main()
