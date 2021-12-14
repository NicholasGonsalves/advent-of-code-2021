"""Day 13."""


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read().splitlines()
    lines = [i for i in inputs]
    points = []
    folds = []
    for i, line in enumerate(lines):
        if line == '':
            for fold in lines[i+1:]:
                folds.append(fold[11:])
            break
        points.append([int(x) for x in line.split(',')])
    folds = [[fold.split('=')[0], int(fold.split('=')[1])] for fold in folds]
    return points, folds


def create_paper(points):
    paper = [[0 for _ in range(max([x[0] for x in points]) + 1)] for _ in range(max([y[1] for y in points]) + 1)]
    for point in points:
        x, y = point
        paper[y][x] = 1
    return paper


def apply_fold(fold_section, paper):
    for y, row in enumerate(fold_section):
        for x, dot in enumerate(row):
            paper[y][x] = paper[y][x] or dot
    return paper


def fold_paper(paper, fold):

    fold_dir, fold_pos = fold

    if fold_dir == 'y':
        fold_section = list(reversed(paper[fold_pos:]))
        paper = apply_fold(fold_section, paper)
        paper = paper[:fold_pos]
    elif fold_dir == 'x':
        fold_section = [list(reversed(row[-fold_pos:])) for row in paper]
        paper = apply_fold(fold_section, paper)
        paper = [row[:fold_pos] for row in paper]
    else:
        raise ValueError(f"Fold_dir {fold_dir} unknown.")
    return paper


def part_one(points, folds):
    paper = create_paper(points)

    paper = fold_paper(paper, folds[0])

    # count dots
    return sum([dot for row in paper for dot in row])


def part_two(points, folds):
    paper = create_paper(points)

    for fold in folds:
        paper = fold_paper(paper, fold)

    for row in paper:
        print(row)


if __name__ == "__main__":
    data1, data2 = read_file("day13.txt")

    print(part_one(data1, data2))
    part_two(data1, data2)
