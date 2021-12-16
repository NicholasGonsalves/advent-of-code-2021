"""Day 15."""
from copy import deepcopy
from heapq import heappush, heappop


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.read().splitlines()
    lines = [list(map(int, i)) for i in inputs]
    return lines


def find_path(grid):
    # Dijkstra (wikipedia)
    queue, visited, dist = [], {}, {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dist[(i, j)] = float('inf')
            queue.append((i, j))
            visited[(i, j)] = None
    dist[(0, 0)] = 0

    def in_bounds(point):
        if (point[0] >= 0) and (point[0] < len(grid)) and (point[1] >= 0) and (point[1] < len(grid[0])):
            return True
        return False

    checked_nodes = 0
    while queue:
        checked_nodes += 1
        u = min(queue, key=dist.__getitem__)
        queue.remove(u)

        for neighbour in [(u[0]+1, u[1]), (u[0], u[1]+1)]:
            if not in_bounds(neighbour): continue
            alt = dist[u] + grid[neighbour[0]][neighbour[1]]
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                visited[neighbour] = u

        if checked_nodes % 100 == 0:
            print(f"Checked {checked_nodes} nodes.")

    # Step backwards through values to get path
    destination = (len(grid)-1, len(grid[0])-1)
    path = [destination]
    current = destination

    while visited[current]:
        path.append(visited[current])
        current = visited[current]

    return list(reversed(path))


def part_one(cave):
    path = find_path(cave)
    return sum([cave[p[0]][p[1]] for p in path]) - cave[0][0]


def apply_wrapping_increment(tile, increment):
    for i in range(len(tile)):
        for j in range(len(tile[0])):
            val = tile[i][j] + increment
            if val > 9:
                val = val % 9
            tile[i][j] = val
    return tile


def combine_horizontal_caves(tiles):
    expanded_cave = []
    for i in range(len(tiles[0])):
        new_row = []
        for tile in tiles:
            new_row += tile[i]
        expanded_cave.append(new_row)
    return expanded_cave


def part_two(cave):
    # tile horizontally
    tile_map = {0: deepcopy(cave)}
    for i in range(1, 9):
        tile_map[i] = apply_wrapping_increment(deepcopy(cave), i)

    # Ordering
    ordering = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
    ]

    # Expand cave
    expanded_cave = []
    for row in ordering:
        expanded_row = []
        for position in row:
            expanded_row.append(deepcopy(tile_map[position]))
        combined_expanded_row = combine_horizontal_caves(expanded_row)
        expanded_cave.append(combined_expanded_row)

    expanded_cave = [row for hoz in expanded_cave for row in hoz]

    # Compute path
    path = find_path(expanded_cave)
    return sum([expanded_cave[p[0]][p[1]] for p in path]) - expanded_cave[0][0]



if __name__ == "__main__":
    data = read_file("day15.txt")

    print(part_one(data))
    print(part_two(data))
