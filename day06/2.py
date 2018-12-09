from argparse import ArgumentParser
from itertools import product
from functools import partial


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('distance_threshold', type=int)

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def parse_point(line):
    return tuple(map(int, line.split(', ')))


def get_dist(coordinate_list, x, y):
    distance_total = sum(
        abs(x - centroid_x) + abs(y - centroid_y)
        for centroid_x, centroid_y in coordinate_list
    )

    return distance_total


def region_coords(
        min_x, max_x, min_y, max_y, distance_threshold):
    return product(
        range(min_x - distance_threshold, max_x + distance_threshold + 1),
        range(min_y - distance_threshold, max_y + distance_threshold + 1),
    )


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()
    coordinates = [parse_point(line) for line in data]
    get_dist_ = partial(get_dist, coordinates)

    x_coords, y_coords = zip(*coordinates)
    ((min_x, min_y), (max_x, max_y)) = (
        map(func, (x_coords, y_coords))
        for func in (min, max)
    )

    region_size = 0
    coord_iterator = region_coords(
        min_x, max_x, min_y, max_y, args.distance_threshold
    )
    for x, y in coord_iterator:
        manhattan_dist = get_dist_(x, y)
        if manhattan_dist < args.distance_threshold:
            region_size += 1
    print(region_size)


if __name__ == '__main__':
    main()
