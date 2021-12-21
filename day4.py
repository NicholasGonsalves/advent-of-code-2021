"""Day 4."""
from itertools import chain

import numpy as np


def read_file(file_name: str):
    with open(file_name) as f:
        inputs = f.read()

    parsed = [d for d in inputs.split("\n\n") if d != ""]

    numbers = list(map(int, parsed[0].split(",")))
    board_strings = [board for board in parsed[1:]]
    board_row_strings = [board.split("\n") for board in board_strings]
    boards_value_strings = [[row.split() for row in board] for board in board_row_strings]
    boards = [[[int(float(j)) for j in i] for i in board] for board in boards_value_strings]

    return numbers, boards


def part_one(picks, boards):
    for pick in picks:
        for i in range(len(boards)):
            new_board = update_board(board=boards[i], value=pick)
            boards[i] = new_board
            if check_board_for_win(new_board):
                # print(pick, get_unmarked_board_values(new_board))
                return pick * get_unmarked_board_values(new_board)


def part_two(picks, boards):
    number_of_boards = len(boards)
    have_won = set()
    for pick in picks:
        for i in range(len(boards)):
            new_board = update_board(board=boards[i], value=pick)
            boards[i] = new_board
            if check_board_for_win(new_board):
                have_won.add(i)
                if len(have_won) == number_of_boards:
                    return pick * get_unmarked_board_values(boards[i])


def get_unmarked_board_values(board):
    filtered_board = [[v for v in row if v != "#"] for row in board]
    return sum(list(chain.from_iterable(filtered_board)))


def update_board(board, value):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == value:
                board[r][c] = "#"
    return board


def check_rows_for_win(board):
    # check rows
    row_length = len(board[0])
    for row in board:
        matches = 0
        for value in row:
            if value == "#":
                matches += 1
        if matches == row_length:
            return True
    return False


def check_board_for_win(board):
    # check rows and transpose to check columns
    if check_rows_for_win(board) or check_rows_for_win(np.array(board).T.tolist()):
        return True
    return False


if __name__ == "__main__":
    data_picks, data_boards = read_file("day4.txt")
    # print(data_picks, data_boards)

    print(part_one(data_picks, data_boards))
    print(part_two(data_picks, data_boards))
