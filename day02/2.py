from argparse import ArgumentParser
from itertools import product


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def hamming(string1, string2):
    return sum(
        0 if char1 == char2 else 1
        for char1, char2 in zip(string1, string2)
    )


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()

    for first, second in product(data, data):
        if hamming(first, second) == 1:
            break
    else:
        raise RuntimeError('No valid string found!')

    for char1, char2 in zip(first, second):
        if char1 == char2:
            print(char1, end='')
    print()


if __name__ == '__main__':
    main()
