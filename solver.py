board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def sudoku_solver(sudoku):
    """solving sudoku"""
    find = isEmpty(sudoku)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if isValid(sudoku, i, (row, col)):
            sudoku[row][col] = i

            if sudoku_solver(sudoku):
                return True

            sudoku[row][col] = 0
    return False


def isValid(sudoku, num, pos):
    """Checking for the next valid number"""

    # Check row
    for i in range(len(sudoku[0])):
        if sudoku[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(sudoku)):
        if sudoku[i][pos[1]] == num and pos[0] != i:
            return False

    # Check Box (3 by 3)
    # to ensure you are in the right box of 9
    box_y = pos[1] // 3
    box_x = pos[0] // 3

    for i in range(box_x * 3, box_x * 3 + 3):
        for j in range(box_y * 3, box_y * 3 + 3):
            if sudoku[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(sudoku):
    """to print sudoku board"""
    print("SUDOKU SOLVER".center(24, '*'))
    print()
    for i in range(len(sudoku)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(sudoku[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j < 8:
                print(str(sudoku[i][j]) + " ", end="")

            else:
                print(sudoku[i][j])


def isEmpty(sudoku):
    """to find the next empty space [0]"""
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                return i, j  # row and col
    return None


def solve_sudoku(sudoku):
    """displaying 'before and after" solving of sudoku"""

    print_board(sudoku)
    sudoku_solver(sudoku)
    print()
    print_board(sudoku)


solve_sudoku(board)
