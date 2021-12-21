# from common_code import read_file
from typing import List


def read_file(file_name: str, delimiter: str = "\n"):
    with open(file_name) as f:
        inputs = f.read()
    parsed = [int(i) for i in inputs.split(delimiter)]
    return parsed


def part_one(depths):
    # count = 0
    # for i in range(1, len(depths)):
    #     if depths[i] > depths[i - 1]:
    #         count += 1
    # return count
    return sum(y > x for x, y in zip(depths, depths[1:]))


def part_two(depths):
    # count = 0
    # window = []
    #
    # window.append(depths[0])
    # window.append(depths[1])
    # window.append(depths[2])
    #
    # for d in depths[3:]:
    #     sum1 = sum(window)
    #     print(window)
    #     window.pop(0)
    #     window.append(d)
    #     sum2 = sum(window)
    #     print(window)
    #     if sum2 > sum1:
    #         count += 1
    #
    #     print(sum1, sum2)
    # return count
    r = [x + y + z for x, y, z in zip(depths, depths[1:], depths[2:])]
    return sum(y > x for x, y in zip(r, r[1:]))


if __name__ == "__main__":
    # print(read_file("day_1.txt"))

    data = read_file("day1.txt")

    print(part_one(data))
    print(part_two(data))
