"""Day 10."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    return [list(i) for i in inputs]


pairs = {
    '}': '{',
    ']': '[',
    ')': '(',
    '>': '<',
}

pairs_other = {
    '{': '}',
    '[': ']',
    '(': ')',
    '<': '>',
}

part_1_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

part_2_points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


def part_one(brackets):
    total = []
    for line in brackets:
        stack = []
        for bracket in line:
            # {'{', '[', '(', '<'}
            if bracket in pairs.keys():
                opener = stack.pop()
                if opener != pairs.get(bracket):
                    total.append(part_1_points.get(bracket))
                    break
                else:
                    continue
            stack.append(bracket)
    return sum(total)


def get_incomplete_lines(brackets):
    corrupted = []
    for i, line in enumerate(brackets):
        stack = []
        for bracket in line:
            # {'{', '[', '(', '<'}
            if bracket in pairs.keys():
                opener = stack.pop()
                if opener != pairs.get(bracket):
                    corrupted.append(i)
                    break
                else:
                    continue
            stack.append(bracket)
    return [brackets[i] for i in range(len(brackets)) if i not in corrupted]


def part_two(brackets):
    # get only incomplete lines (not corrupted ones)
    brackets = get_incomplete_lines(brackets)

    total = []
    for line in brackets:
        stack = []
        line_value = 0
        for bracket in line:
            # {'{', '[', '(', '<'}
            if bracket in pairs.keys():
                opener = stack.pop()
                if opener != pairs.get(bracket):
                    break
                else:
                    continue
            stack.append(bracket)
        for bracket in reversed(stack):
            line_value *= 5
            line_value += part_2_points.get(bracket)
        total.append(line_value)

    # find middle
    return sorted(total)[len(total) // 2]


if __name__ == "__main__":
    data = read_file("day10.txt")

    print(part_one(data))
    print(part_two(data))
