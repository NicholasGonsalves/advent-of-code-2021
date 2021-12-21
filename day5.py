"""Day 4."""
import itertools
from typing import List


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.readlines()

    point_strings = [line[:-1].split(" -> ") for line in inputs]
    points = [
        [list(map(int, point.split(","))) for point in pair] for pair in point_strings
    ]
    return points


class Grid:
    def __init__(self, points):
        self.points = points
        self.grid = self._create_grid()

    def __str__(self):
        return "\n".join([str(row) for row in self.grid])

    def _create_grid(self) -> List[List[int]]:
        grid_x, grid_y = self._get_size_of_grid()
        grid = [[0 for _ in range(grid_x + 1)] for _ in range(grid_y + 1)]
        return grid

    def _get_size_of_grid(self) -> (int, int):
        flattened_points = list(itertools.chain(*self.points))
        max_x = max(max(flattened_points, key=lambda x: x[0]))
        max_y = max(max(flattened_points, key=lambda x: x[1]))
        return max_x, max_y

    def update_grid(self, pair, include_diagonals: bool) -> None:
        p1, p2 = pair
        x1, y1 = p1
        x2, y2 = p2

        hoz = y1 == y2
        ver = x1 == x2

        if hoz ^ ver:
            # swap ordering so always increasing for loop, for hoz or ver
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            if hoz:
                self.update_grid_hoz(x1, y1, x2)
            if ver:
                self.update_grid_ver(x1, y1, y2)
        elif include_diagonals:
            self.update_grid_diagonal(x1, y1, x2, y2)

    def update_grid_hoz(self, x1, y, x2) -> None:
        for x in range(x1, x2 + 1):
            self.grid[y][x] += 1

    def update_grid_ver(self, x, y1, y2) -> None:
        for y in range(y1, y2 + 1):
            self.grid[y][x] += 1

    def update_grid_diagonal(self, x1, y1, x2, y2) -> None:
        x_dir = 1
        if x1 > x2:
            x_dir = -1
        y_dir = 1
        if y1 > y2:
            y_dir = -1

        x_coords = [x for x in range(x1, x2 + x_dir, x_dir)]
        y_coords = [y for y in range(y1, y2 + y_dir, y_dir)]
        for x, y in zip(x_coords, y_coords):
            self.grid[y][x] += 1

    def count_overlapping_lines(self):
        count = 0
        for row in self.grid:
            for value in row:
                if value > 1:
                    count += 1
        return count


def part_one(points):
    grid = Grid(points)

    for point in points:
        grid.update_grid(point, include_diagonals=False)

    return grid.count_overlapping_lines()


def part_two(points):
    grid = Grid(points)

    for point in points:
        grid.update_grid(point, include_diagonals=True)

    return grid.count_overlapping_lines()


if __name__ == "__main__":
    data = read_file("day5.txt")

    print(part_one(data))
    print(part_two(data))
