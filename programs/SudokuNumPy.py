import numpy as np

def validNum(sudoku, row, col, num):
    
    # check if number exists in row or column
    if np.any(sudoku[row, :] == num) or np.any(sudoku[:, col] == num):
        return False
        
    # check 3x3 matrix for number
    startRow, startCol = 3 * (row // 3),  3 * (col // 3)
    if np.any(sudoku[startRow:startRow + 3, startCol:startCol + 3] == num):
        return False

    return True

def solveSudoku(sudoku):

    # find the first empty cell
    emptyCells = np.argwhere(sudoku == 0)
  
    # solved
    if emptyCells.size == 0:
        return True
    
    row, col = emptyCells[0]

    for num in range(1, 10):
        if validNum(sudoku, row, col, num):
            sudoku[row, col] = num
            if solveSudoku(sudoku):
                return True
            sudoku[row, col] = 0

    return False

if __name__ == "__main__":
    #initialisation of sudoku
    file = open("./sudoku.txt")
    sudoku = []
    for line in file:
        sudoku.append([int(x) for x in line.split()])

    sudoku = np.array(sudoku)

    solveSudoku(sudoku)
    with open("./sudoku_solved.txt", "w") as f:
        for row in sudoku:
            f.write(" ".join(map(str, row)) + "\n")