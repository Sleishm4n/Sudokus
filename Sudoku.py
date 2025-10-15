def validNum(sudoku, row, col, num):

    # check if num exists in column
    for i in range(9):
        if sudoku[i][col] == num:
            return False

    # check if num exists in row
    for i in range(9):
        if sudoku[row][i] == num:
            return False

    # check 3x3 matrix for num
    startRow = row - (row % 3)
    startCol = col - (col % 3)

    for i in range(3):
        for j in range(3):
            if sudoku[i + startRow][j + startCol] == num:
                return False

    return True


def solveSudokuRec(sudoku, row, col):

    # base case reached nth column of the last row
    if row == 9:
        return True

    # if last column reached in row, move to next row
    if col == 9:
        return solveSudokuRec(sudoku, row + 1, 0)

    # if a number from 1-9 in box then move on
    if sudoku[row][col] != 0:
        return solveSudokuRec(sudoku, row, col + 1)

    # check if number is going to be valid in box
    for num in range(1, 10):
        if validNum(sudoku, row, col, num):
            sudoku[row][col] = num
            if solveSudokuRec(sudoku, row, col):
                return True
            sudoku[row][col] = 0

    return False

def solveSudoku(sudoku):
    solveSudokuRec(sudoku, 0, 0)

if __name__ == "__main__":
    # initialisation of sudoku
    sudoku = [
        [2, 0, 3, 0, 0, 9, 5, 0, 0],
        [1, 9, 5, 0, 0, 2, 4, 8, 0],
        [0, 0, 0, 8, 0, 5, 2, 1, 9],
        [0, 2, 0, 0, 5, 0, 6, 0, 4],
        [4, 5, 9, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 7, 8, 4, 0, 0, 5],
        [0, 0, 0, 3, 0, 0, 1, 4, 8],
        [9, 6, 0, 0, 4, 0, 0, 5, 0],
        [3, 1, 0, 0, 2, 0, 0, 0, 0],
    ]

    solveSudoku(sudoku)

    for row in sudoku:
        print(" ".join(map(str, row)))
