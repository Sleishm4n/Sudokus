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
    sudoku = np.array([
        [2, 0, 3, 0, 0, 9, 5, 0, 0],
        [1, 9, 5, 0, 0, 2, 4, 8, 0],
        [0, 0, 0, 8, 0, 5, 2, 1, 9],
        [0, 2, 0, 0, 5, 0, 6, 0, 4],
        [4, 5, 9, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 7, 8, 4, 0, 0, 5],
        [0, 0, 0, 3, 0, 0, 1, 4, 8],
        [9, 6, 0, 0, 4, 0, 0, 5, 0],
        [3, 1, 0, 0, 2, 0, 0, 0, 0],
    ])

    solveSudoku(sudoku)
    print(sudoku)