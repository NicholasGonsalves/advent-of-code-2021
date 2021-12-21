"""Day 3."""


def read_file(file_name: str, delimiter: str = "\n"):
    with open(file_name) as f:
        inputs = f.read()
    parsed = [list(d) for d in inputs.split(delimiter)]
    return parsed


def part_one(report):
    counts = [0] * len(report[0])
    for i in range(len(report[0])):
        for row in report:
            if row[i] == "1":
                counts[i] += 1
            else:
                counts[i] -= 1

    epsilon = []
    gamma = []
    for bit in counts:
        if bit > 0:
            epsilon.append(1)
            gamma.append(0)
        else:
            epsilon.append(0)
            gamma.append(1)

    return int("".join([str(i) for i in epsilon]), 2) * int(
        "".join([str(i) for i in gamma]), 2
    )


def part_two(report):
    oxygen = report.copy()
    co2 = report.copy()

    # oxygen
    for i in range(len(oxygen[0])):
        tmp = []
        count = 0
        for row in oxygen:
            if row[i] == "1":
                count += 1
            else:
                count -= 1
        if count >= 0:
            for row in oxygen:
                if row[i] == "1":
                    tmp.append(row)
        else:
            for row in oxygen:
                if row[i] == "0":
                    tmp.append(row)
        oxygen = tmp
        if len(oxygen) == 1:
            break

    print(oxygen)
    ox_num = int("".join([str(i) for i in oxygen[0]]), 2)

    # co2
    for i in range(len(co2[0])):
        tmp = []
        count = 0
        for row in co2:
            if row[i] == "0":
                count += 1
            else:
                count -= 1
        if count > 0:
            for row in co2:
                if row[i] == "1":
                    tmp.append(row)
        else:
            for row in co2:
                if row[i] == "0":
                    tmp.append(row)
        co2 = tmp
        if len(co2) == 1:
            break

    print(co2)
    co2_num = int("".join([str(i) for i in co2[0]]), 2)

    return co2_num * ox_num


if __name__ == "__main__":
    data = read_file("day3.txt")

    print(part_one(data))
    print(part_two(data))
