"""Day 9."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    return [list(map(int, list(i))) for i in inputs]


directions = [
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1],
]


def check_in_bounds(i, j, height_map):
    return (i >= 0) and (i < len(height_map)) and (j >= 0) and (j < len(height_map[0]))


def part_one(height_map):
    low_point_values = []
    low_point_indexes = []
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            # consider adjacent points
            # if all are greater than current position, add to list
            adj_values = []
            for direction in directions:
                adj_i = i + direction[0]
                adj_j = j + direction[1]
                in_bounds = (
                    (adj_i >= 0)
                    and (adj_i < len(height_map))
                    and (adj_j >= 0)
                    and (adj_j < len(height_map[0]))
                )
                if in_bounds:
                    adj_values.append(height_map[adj_i][adj_j])

            found_higher = [v for v in adj_values if v <= height_map[i][j]]
            if not found_higher:
                low_point_values.append(height_map[i][j])
                low_point_indexes.append((i, j))

    return sum([1 + v for v in low_point_values]), low_point_indexes


def bfs(height_map, visited, pos):
    queue = [pos]
    visited.add(pos)

    while len(queue) > 0:
        p = queue.pop(0)
        for direction in directions:
            adj_i = p[0] + direction[0]
            adj_j = p[1] + direction[1]
            in_bounds = check_in_bounds(adj_i, adj_j, height_map)
            if (
                in_bounds
                and (height_map[adj_i][adj_j] != 9)
                and ((adj_i, adj_j) not in visited)
            ):
                queue.append((adj_i, adj_j))
                visited.add((adj_i, adj_j))
    return visited


def part_two(height_map, seed_points):
    # find basins, they are ringed with 9's
    # bfs? starting from low points?
    basin_sizes = []
    for pos in seed_points:
        visited = set()
        basin_sizes.append(len(bfs(height_map, visited, pos)))

    basin_sizes = sorted(basin_sizes)
    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


if __name__ == "__main__":
    data = read_file("day9.txt")

    part_one_ans, low_points = part_one(data)
    print(part_one_ans)
    print(part_two(data, low_points))
