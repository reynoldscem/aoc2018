from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()
    frequency = sum(map(int, data))
    print(frequency)


if __name__ == '__main__':
    main()
