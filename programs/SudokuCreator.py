import random
import Sudoku as Sudoku

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

def createSudoku(clues):

    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    fillSudoku(sudoku)
    solution = [row[:] for row in sudoku]

    removeNums(sudoku, clues)

    return sudoku, solution

def fillSudoku(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                digits = list(range(1,10))
                random.shuffle(digits)

                for num in digits:
                    if validNum(sudoku, row, col, num):
                        sudoku[row][col] = num

                        if fillSudoku(sudoku):
                            return True
                        
                        sudoku[row][col] = 0

                return False
            
    return True

def removeNums(sudoku, clues):
    attempts = clues
    while attempts > 0:
        row, col = random.randint(0,8), random.randint(0,8)

        if sudoku[row][col] != 0:
            backup = sudoku[row][col]
            sudoku[row][col] = 0

            test_sudoku = [row[:] for row in sudoku]

            if not Sudoku.solveSudokuRec(test_sudoku,0,0):
                sudoku[row][col] = backup

            attempts -= 1


if __name__ == "__main__":
    # Create a Sudoku puzzle
    # Difficulty level: 30-35 (easy), 40-45 (medium), 50-55 (hard)
    puzzle, solution = createSudoku(42)

    with open("./sudoku.txt", "w") as file:
        for row in puzzle:
            file.write(" ".join(str(x) for x in row) + "\n")