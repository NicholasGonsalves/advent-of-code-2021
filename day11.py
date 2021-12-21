"""Day 11."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    return [list(map(int, list(i))) for i in inputs]


directions = [
    [-1, 0],
    [-1, 1],
    [-1, -1],
    [0, 1],
    [0, -1],
    [1, 0],
    [1, 1],
    [1, -1],
]


def check_in_bounds(i, j):
    return (i >= 0) and (i < 10) and (j >= 0) and (j < 10)


def multi_pass_flash(octopi):
    flashed = set()

    did_flash = True
    while did_flash:
        prev_len_flashed = len(flashed)
        for i in range(10):
            for j in range(10):
                if (octopi[i][j] > 9) and ((i, j) not in flashed):
                    flashed.add((i, j))
                    for direction in directions:
                        adj_i = i + direction[0]
                        adj_j = j + direction[1]
                        if check_in_bounds(adj_i, adj_j):
                            octopi[adj_i][adj_j] += 1
        if len(flashed) == prev_len_flashed:
            did_flash = False

    # return value
    return octopi


def part_one(octopi):
    flashes = 0
    for _ in range(100):
        # increment all octopi
        octopi = [[j+1 for j in row] for row in octopi]

        # use find which should flash, and flash them
        octopi = multi_pass_flash(octopi)

        # count flashes and set flashes to 0
        for i in range(10):
            for j in range(10):
                if octopi[i][j] > 9:
                    flashes += 1
                    octopi[i][j] = 0

    return flashes


def part_two(octopi):
    flashes = 0
    simul = False
    count = 0
    while not simul:
        count += 1
        # increment all octopi
        octopi = [[j + 1 for j in row] for row in octopi]

        # use find which should flash, and flash them
        octopi = multi_pass_flash(octopi)

        # count flashes and set flashes to 0
        for i in range(10):
            for j in range(10):
                if octopi[i][j] > 9:
                    flashes += 1
                    octopi[i][j] = 0

        # check if all flashed at once
        simul = all(v == 0 for v in [item for sublist in octopi for item in sublist])

    return count


if __name__ == "__main__":
    data = read_file("day11.txt")

    print(part_one(data))
    print(part_two(data))
