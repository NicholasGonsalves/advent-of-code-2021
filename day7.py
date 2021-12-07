"""Day 7."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read()
    return list(map(int, inputs.split(",")))


def part_one(positions):
    # optimal position is the median
    positions.sort()
    mid = len(positions) // 2
    optimal = (positions[mid] + positions[~mid]) / 2
    return int(sum([abs(x - optimal) for x in positions]))


def part_two(positions):
    # optimal position is the mean (though unknown if floor(mean) or floor(mean)+1)
    mean = sum(positions) / len(positions)
    optimal_options = [int(mean), round(mean)]
    return min(
        [
            int(sum([sum(range(1, abs(x - optimal) + 1)) for x in positions]))
            for optimal in optimal_options
        ]
    )


if __name__ == "__main__":
    data = read_file("day7.txt")

    print(part_one(data))
    print(part_two(data))
