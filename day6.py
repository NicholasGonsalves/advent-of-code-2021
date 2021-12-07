"""Day 6."""
from typing import List


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read()
    return list(map(int, inputs.split(",")))


def simulate_lanterns(fish: List[int], n: int) -> int:
    fish_counts = [0 for _ in range(9)]
    for timer in fish:
        fish_counts[timer] += 1

    for _ in range(n):
        fish_to_spawn = fish_counts.pop(0)
        fish_counts.append(fish_to_spawn)
        fish_counts[6] += fish_to_spawn

    return sum(fish_counts)


def part_one(initial_fish):
    return simulate_lanterns(initial_fish, 80)


def part_two(initial_fish):
    return simulate_lanterns(initial_fish, 256)


if __name__ == "__main__":
    data = read_file("day6.txt")

    print(part_one(data))
    print(part_two(data))
