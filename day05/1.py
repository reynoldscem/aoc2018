from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def react(chunk_list):
    iterator = zip(chunk_list, chunk_list[1:])
    for first, second in iterator:
        if chunks_match(first, second):
            next(iterator)
            yield None
            for first, second in iterator:
                yield first
            yield second
            return
        else:
            yield first
    else:
        yield second


def chunks_match(first, second):
    return (
        (first.islower() and second.isupper() and first == second.lower()) or
        (first.isupper() and second.islower() and first == second.upper())
    )


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        polymer = fd.read().strip()
    while True:
        polymer = list(react(polymer))
        if None not in polymer:
            break
        polymer = ''.join([chunk for chunk in polymer if chunk is not None])
    print(len(polymer))


if __name__ == '__main__':
    main()
