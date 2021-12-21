"""Day 17."""


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.read()
    inputs = inputs.split("target area: ")[1].split(", ")
    x = list(map(int, inputs[0].split("=")[1].split("..")))
    y = list(map(int, inputs[1].split("=")[1].split("..")))
    return x, y


def step(pos_x, pos_y, vel_x, vel_y):
    pos_y += vel_y
    vel_y -= 1
    pos_x += vel_x
    if vel_x != 0:
        drag_dir = 1 if vel_x < 0 else -1
        vel_x += drag_dir
    return pos_x, pos_y, vel_x, vel_y


def check_if_target_hit(probe_x, probe_y, target_x, target_y):
    if (target_x[0] <= probe_x <= target_x[1]) and (target_y[0] <= probe_y <= target_y[1]):
        return True
    return False


def check_if_past_target(probe_y, target_y):
    if target_y[0] > probe_y:
        return True
    return False


def simul_initial_velocities(target_x, target_y, x_pos, x_vel, y_pos, y_vel):
    y_positions = []
    while not check_if_past_target(y_pos, target_y):
        y_positions.append(y_pos)
        if check_if_target_hit(x_pos, y_pos, target_x, target_y):
            return max(y_positions)
        x_pos, y_pos, x_vel, y_vel = step(x_pos, y_pos, x_vel, y_vel)
    return None


def part_one(target_x, target_y):
    # calculate search space for initial firing params
    max_x_vel = target_x[1] + 1
    min_x_vel = 0
    max_y_vel = 1000  # this one is a guess because it is late lol
    min_y_vel = target_y[0]

    x_pos, y_pos = 0, 0
    max_y_positions = []

    for x_vel in range(min_x_vel, max_x_vel + 1):
        for y_vel in range(min_y_vel, max_y_vel + 1):
            # print(x_vel, y_vel)
            result = simul_initial_velocities(target_x, target_y, x_pos, x_vel, y_pos, y_vel)
            if result is not None:
                max_y_positions.append(result)
    return max(max_y_positions)


def part_two(target_x, target_y):
    # calculate search space for initial firing params
    max_x_vel = target_x[1] + 1
    min_x_vel = 0
    max_y_vel = 1000  # this one is a guess because it is late lol
    min_y_vel = target_y[0]

    x_pos, y_pos = 0, 0
    count_hits = 0

    for x_vel in range(min_x_vel, max_x_vel + 1):
        for y_vel in range(min_y_vel, max_y_vel + 1):
            result = simul_initial_velocities(target_x, target_y, x_pos, x_vel, y_pos, y_vel)
            if result is not None:
                count_hits += 1
    return count_hits


if __name__ == "__main__":
    x, y = read_file("day17.txt")

    print(part_one(x, y))
    print(part_two(x, y))
