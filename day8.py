"""Day 8."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    return inputs


def part_one(patterns):
    count = 0
    lookup = {2, 3, 4, 7}

    for pattern in patterns:
        _, code = pattern.split(" | ")
        for digit in code.split(" "):
            if len(digit) in lookup:
                count += 1
    return count


def intersection_of_sets(arr1, arr2, arr3):
    s1 = set(arr1)
    s2 = set(arr2)
    s3 = set(arr3)
    set1 = s1.intersection(s2)
    result_set = set1.intersection(s3)
    final_list = list(result_set)
    return final_list


class SegmentSolver:
    def __init__(self, patterns):
        self.patterns = patterns

    def solve(self):
        total = 0
        for pattern in self.patterns:
            signals, digits = pattern.split(" | ")
            total += self.solve_pattern(signals, digits)
        return total

    def solve_pattern(self, signals, digits):
        signals = ["".join(sorted(signal)) for signal in signals.split(" ")]
        digits = ["".join(sorted(digit)) for digit in digits.split(" ")]

        # build up map of 'signal letter' to 'possible digit'
        # e.g. {'a': {1, 7}, ...} worked out from 'a' being used in 'ab' (1) and 'abc' (7)
        mapping = {l: set() for l in "abcdefg"}

        # work out signal->digit mapping
        digit_map = {d: set() for d in range(10)}
        for signal in signals:
            values = self.check_lengths(signal)
            if not values:
                continue
            for value in values:
                for char in signal:
                    digit_map[value].update(char)

        signal_map = {
            "".join(sorted(list(letters))): digit
            for digit, letters in digit_map.items()
            if letters
        }

        # work out shared properties
        signal_map = self.calculate_unique(signals, digit_map, signal_map)

        # decode 4 digits and return as 4 digit int
        solved_digits = []
        for digit in digits:
            solved_digits.append(signal_map.get(digit))
        return int("".join([str(i) for i in solved_digits]))

    # Python3 program to find common elements
    # in three lists using sets

    @staticmethod
    def calculate_unique(signals, digit_map, signal_map):
        two_three_five = [signal for signal in signals if len(signal) == 5]
        zero_six_nine = [signal for signal in signals if len(signal) == 6]

        top_middle_bottom = intersection_of_sets(*two_three_five)

        # find 0, it does not have all in (top_middle_bottom)
        top_bottom = None
        six_nine = None
        for signal in zero_six_nine:
            for value in top_middle_bottom:
                if value not in signal:
                    signal_map[signal] = 0
                    middle = value
                    top_bottom = [v for v in top_middle_bottom if v != middle]
                    six_nine = [v for v in zero_six_nine if v != signal]
                    break
            if 0 in signal_map.values():
                break

        for v in six_nine:
            value = list(v) + list(digit_map.get(1))
            if set(value) == digit_map.get(8):
                signal_map[v] = 6

        value = list(six_nine[0]) + list(digit_map.get(1))

        if set(value) == digit_map.get(8):
            six = list(sorted(six_nine[0]))
            nine = list(sorted(six_nine[1]))
            signal_map[six_nine[0]] = 6
            signal_map[six_nine[1]] = 9
        else:
            six = list(sorted(six_nine[1]))
            nine = list(sorted(six_nine[0]))
            signal_map[six_nine[0]] = 9
            signal_map[six_nine[1]] = 6

        # now 2, 3, 5
        # 2 and 3 have (8-6), 5 doesn't
        upper_right = digit_map.get(8).difference(set(six)).pop()
        signal_map[[v for v in two_three_five if upper_right not in v][0]] = 5

        bottom_left = digit_map.get(8).difference(set(nine)).pop()
        signal_map[[v for v in two_three_five if bottom_left in v][0]] = 2

        signal_map[[v for v in signals if v not in signal_map.keys()][0]] = 3

        return signal_map

    @staticmethod
    def check_lengths(signal):
        length_lookup = {
            2: {1},
            3: {7},
            4: {4},
            7: {8},
            # 5: {2, 3, 5},
            # 6: {0, 6, 9},
        }
        return length_lookup.get(len(signal))


def part_two(patterns):
    solver = SegmentSolver(patterns)
    return solver.solve()


if __name__ == "__main__":
    data = read_file("day8.txt")

    print(part_one(data))
    print(part_two(data))
