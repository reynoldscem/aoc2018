from itertools import product, zip_longest, chain
from argparse import ArgumentParser
from collections import Counter
from functools import partial


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def parse_point(line):
    return tuple(map(int, line.split(', ')))


def internal_squares(min_x, max_x, min_y, max_y):
    return product(range(min_x + 1, max_x), range(min_y + 1, max_y))


def edge_squares(min_x, max_x, min_y, max_y):
    return chain(
        zip_longest(tuple(), range(min_y, max_y + 1), fillvalue=min_x),
        zip_longest(tuple(), range(min_y, max_y + 1), fillvalue=max_x),
        zip_longest(range(min_x + 1, max_x), tuple(), fillvalue=min_y),
        zip_longest(range(min_x + 1, max_x), tuple(), fillvalue=max_y),
    )


def get_closest_coordinates(coordinate_list, x, y):
    if (x, y) in coordinate_list:
        return (coordinate_list.index((x, y)), )
    distances = [
        abs(x - centroid_x) + abs(y - centroid_y)
        for centroid_x, centroid_y in coordinate_list
    ]

    return tuple(
        index
        for index, distance in enumerate(distances)
        if distance == min(distances)
    )


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()
    coordinates = [parse_point(line) for line in data]
    get_closest = partial(get_closest_coordinates, coordinates)

    x_coords, y_coords = zip(*coordinates)
    ((min_x, min_y), (max_x, max_y)) = (
        map(func, (x_coords, y_coords))
        for func in (min, max)
    )
    # import numpy as np
    # from matplotlib import pyplot as plt
    # blah = np.zeros((max_x + 1, max_y + 1))
    # for x, y in edge_squares(min_x, max_x, min_y, max_y):
    #     print(x, y)
    #     blah[x, y] = 1
    # plt.imshow(blah)
    # plt.show()

    # chars = 'abcdef'
    blacklisted = [
        get_closest(x, y)
        for x, y in edge_squares(min_x, max_x, min_y, max_y)
    ]
    blacklisted = [
        entry[0]
        for entry in blacklisted
        if len(entry) == 1
    ]
    # print(blacklisted)

    internal_occupancy = Counter()
    for x, y in internal_squares(min_x, max_x, min_y, max_y):
        closest = get_closest(x, y)
        if len(closest) > 1:
            continue
        point_owner, *_ = closest
        if point_owner in blacklisted:
            continue
        internal_occupancy[point_owner] += 1
    (index, size), *_ = internal_occupancy.most_common(1)
    print(index, size)


if __name__ == '__main__':
    main()
