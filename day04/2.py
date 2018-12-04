from collections import Counter, defaultdict
from datetime import datetime, timedelta
from argparse import ArgumentParser
from itertools import zip_longest
import re


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--data-path', type=str, required=True)

    return parser


def split_shifts(list_of_events):
    chunk = []
    for line in list_of_events:
        if 'Guard' in line and len(chunk) >= 1:
            yield chunk
            chunk = [line]
        else:
            chunk.append(line)
    yield chunk


class Shift():
    def __init__(self, shift_list):
        self.guard_id, *_ = map(int, re.findall('#(\d+)', shift_list[0]))
        times = [self.get_time_from_line(line) for line in shift_list]

        self.shift_start, *sleep_wake_times = times
        self.sleep_wake_times = sleep_wake_times

        self.set_total_time_asleep()

    def set_total_time_asleep(self):
        self.minutes_asleep = 0
        self.sleeping_times = []
        times_iter_repeated = [iter(self.sleep_wake_times)] * 2
        for first, second in zip_longest(*times_iter_repeated):
            self.minutes_asleep += (second - first).seconds // 60
            minute = first
            while minute != second:
                self.sleeping_times.append(minute.minute)
                minute += timedelta(minutes=1)

    @staticmethod
    def get_time_from_line(line):
        time_string = re.search('\d\d:\d\d', line).group()
        return datetime.strptime(time_string, '%H:%M')


def main():
    args = build_parser().parse_args()
    with open(args.data_path) as fd:
        data = fd.read().splitlines()

    # Sort by dates
    data = sorted(data)
    shifts = map(Shift, split_shifts(data))

    guard_time_counter = Counter()
    guard_id_to_shifts = defaultdict(list)
    for shift in shifts:
        print(shift.guard_id, shift.minutes_asleep)
        guard_time_counter[shift.guard_id] += shift.minutes_asleep
        guard_id_to_shifts[shift.guard_id].append(shift)

    (guard_id, time_asleep),  = guard_time_counter.most_common(1)
    print('{} asleep longest, {} minutes.'.format(guard_id, time_asleep))

    sleeping_minute_info = []
    for guard_id in guard_id_to_shifts.keys():
        minute_asleep_frequencies = Counter()
        for shift in guard_id_to_shifts[guard_id]:
            for minute in shift.sleeping_times:
                minute_asleep_frequencies[minute] += 1

        if len(minute_asleep_frequencies) == 0:
            continue
        (minute, count), = minute_asleep_frequencies.most_common(1)
        sleeping_minute_info.append(
            (count, minute, guard_id)
        )
    (count, minute, guard_id), *_ = reversed(
        sorted(sleeping_minute_info)
    )
    print(guard_id * minute)


if __name__ == '__main__':
    main()
