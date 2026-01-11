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
            if solveSudokuRec(sudoku, row, col + 1):
                return True
            sudoku[row][col] = 0

    return False

def solveSudoku(sudoku):
    solveSudokuRec(sudoku, 0, 0)

if __name__ == "__main__":
    # initialisation of sudoku

    file = open("./sudoku.txt")
    sudoku = []
    for line in file:
        sudoku.append([int(x) for x in line.split()])
    
    solveSudoku(sudoku)

    with open("./sudoku_solved.txt", "w") as f:
        for row in sudoku:
            f.write(" ".join(map(str, row)) + "\n")