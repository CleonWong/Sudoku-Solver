# Pre-existing libraries:
import time

# Third-party libraries:
import numpy as np
import pandas as pd

# ------------------------------
# Functions used:

def parse_quiz(quiz):
    for i in range(0, 81, 9):
        board.append(quiz[i:i+9])
    return board


def parse_soln(soln):
    for i in range(0, 81, 9):
        soln.append(quiz[i:i+9])
    return soln


full_set = {1,2,3,4,5,6,7,8,9}

def check_row(i, j):
    poss_row = full_set - set(board[i])
    return poss_row


def check_col(i, j):
    poss_col = full_set - set([board[x][j] for x in range(9)])
    return poss_col


def check_box(i, j):
    first = [0,1,2]
    second = [3,4,5]
    third = [6,7,8]
    find_box = [first, second, third]

    for l in find_box:
        if i in l:
            row = l
        if j in l:
            col = l

    poss_box = full_set - set([board[i][j] for i in row for j in col])
    return poss_box


def get_poss_vals(i, j):
    poss_vals = check_row(i, j) & check_col(i, j) & check_box(i, j)
    return poss_vals


def fill_definite_val(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                poss_vals = get_poss_vals(i, j)
                if len(poss_vals) == 1:
                    board[i][j] = list(poss_vals)[0]
    return board


def implicit_solver(i, j, board):
    if board[i][j] == 0:
        poss_vals = get_poss_vals(i ,j)

        # Check row:
        poss_list_row = []
        for y in range(9):
            if y == j:
                continue
            if board[i][y] == 0:
                for val in get_poss_vals(i, y):
                    poss_list_row.append(val)
        unique_diff = poss_vals.difference(set(poss_list_row))
        if len(unique_diff) == 1:
            board[i][j] = list(unique_diff)[0]

        # Check col:
        poss_list_col = []
        for y in range(9):
            if y == i:
                continue
            if board[y][j] == 0:
                for val in get_poss_vals(i, j):
                    poss_list_col.append(val)
        unique_diff = poss_vals.difference(set(poss_list_col))
        if len(unique_diff) == 1:
            board[i][j] = list(unique_diff)[0]


        # Check box:
        poss_list_box = []
        first = [0,1,2]
        second = [3,4,5]
        third = [6,7,8]
        find_box = [first, second, third]

        for l in find_box:
            if i in l:
                row = l
            if j in l:
                col = l

        for x in row:
            for y in col:
                if x == i and y == j:
                    continue
                if board[x][y] == 0:
                    for val in get_poss_vals(x, y):
                        poss_list_box.append(val)
        unique_diff = poss_vals.difference(set(poss_list_box))
        if len(unique_diff) == 1:
            board[i][j] = list(unique_diff)[0]

        return board


def done_or_not(board):

    for i in range(9):
        row = board[i]
        if sum(row) != 45:
            return "Try again!"
        col = [board[j][i] for j in range(9)]
        if sum(col) != 45:
            return "Try again!"
        subgrid = [board[(j//3) + 3*(i//3)][(j%3) + 3*(i%3)] for j in range (9)]
        if sum(subgrid) != 45:
            return "Try again!"

    return "Finished!"

# ------------------------------
# Parsing the quizzes:

board_all = []
soln_all = []

df_quizzes = pd.read_csv('sudoku.csv', nrows = 1000)

for row in df_quizzes.iterrows():
    quiz = [int(i) for i in row[1]['quizzes']]
    soln = [int(i) for i in row[1]['solutions']]
    board = []
    board = parse_quiz(quiz)
    board_all.append(board)
    soln = []
    soln = parse_soln(soln)
    soln_all.append(soln)

# ------------------------------
# Running the code:

play_count = 0
solved_count = 0
unsolved_count = 0
unsolved_list = []
time_list = []

for board in board_all:
    play_count += 1
    start_time = time.time()
    zcount = 0
    zcount_hist = []

    for row in board:
        for val in row:
            if val == 0:
                zcount +=1
    zcount_hist.append(zcount)

    while zcount != 0:
        fill_definite_val(board)

        for i in range(9):
            for j in range(9):
                implicit_solver(i, j, board)

        zcount = 0
        for row in board:
            for val in row:
                if val == 0:
                    zcount +=1
        zcount_hist.append(zcount)

        # If unsolvable:
        if zcount_hist[-1] == zcount_hist[-2]:
            break

    end_time = time.time()

    tot_time = end_time - start_time
    time_list.append(tot_time)

    if done_or_not(board) == "Finished!":
        solved_count += 1
    elif done_or_not(board) == "Try again!":
        unsolved_count += 1
        unsolved_list.append(play_count - 1)


print("Number of plays:", play_count)
print("Solved: {} ({:.2f}%)".format(solved_count, (solved_count / play_count) * 100))
print("Unsolved {} ({:.2f}%):".format(unsolved_count, (unsolved_count / play_count) * 100))
print("Max. time taken: {:.4f} seconds".format(max(time_list)))
print("Min. time taken: {:.4f} seconds".format(min(time_list)))
s = sum(time_list)
print("Total time taken: {:02}h : {:02}m : {:02}s".format(int(s // 3600), int(s // 60 % 60), int(s % 60)))
print("Indices of unsolved boards: {}".format(unsolved_list))
