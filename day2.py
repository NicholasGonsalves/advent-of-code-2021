# from common_code import read_file
from typing import List


def read_file(file_name: str, delimiter: str = "\n"):
    with open(file_name) as f:
        inputs = f.read()
    parsed = [i.split() for i in inputs.split(delimiter)]
    return parsed


def part_one(instructions):
    depth = hoz = 0

    for i in instructions:
        direction, distance = i
        distance = int(distance)

        if direction == "forward":
            hoz += distance
        elif direction == "up":
            depth -= distance
        elif direction == "down":
            depth += distance
        else:
            raise ValueError("Oh no!")

    return depth * hoz


def part_two(instructions):
    aim = 0
    depth = 0
    hoz = 0
    for i in instructions:
        direction, distance = i
        distance = int(distance)

        if direction == "forward":
            hoz += distance
            depth += aim * distance
        elif direction == "up":
            aim -= distance
        elif direction == "down":
            aim += distance
        else:
            raise ValueError("Oh no!")

    return depth * hoz


if __name__ == "__main__":
    data = read_file("day2.txt")

    print(part_one(data))

    print(part_two(data))
