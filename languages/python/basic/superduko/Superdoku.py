from pathlib import Path

POSS_CHARS = [1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G"]

IN_PATH = Path("puzzles/superdoku.txt")
OUT_PATH = Path("puzzles/superdoku_solved.txt")

def validChar(sudoku, row, col, char):

    for i in range(16):
        if sudoku[i][col] == char:
            return False
        
    for i in range(16):
        if sudoku[row][i] == char:
            return False
        
    startRow = row - (row % 4)
    startCol = col - (col % 4)

    for i in range(4):
        for j in range(4):
            if sudoku[i + startRow][j + startCol] == char:
                return False
            
    return True


def _solveSudokuRec(sudoku, row, col):
    if row == 16:
        return True
    
    if col == 16:
        return _solveSudokuRec(sudoku, row + 1, 0)
    
    if sudoku[row][col] != 0:
        return _solveSudokuRec(sudoku, row, col + 1)
    
    for char in POSS_CHARS:
        if validChar(sudoku, row, col, char):
            sudoku[row][col] = char
            if _solveSudokuRec(sudoku, row, col + 1):
                return True
            sudoku[row][col] = 0
            
    return False


def solve(sudoku):
    return _solveSudokuRec(sudoku, 0, 0)


if __name__ == "__main__":
    file = open(IN_PATH)
    sudoku = []
    for line in file:
        row = []
        for x in line.split():
            row.append(int(x) if x.isdigit() else x)
        sudoku.append(row)

    solve(sudoku)

    with open(OUT_PATH, "w") as f:
        for row in sudoku:
            f.write(" ".join(map(str, row)) + "\n")

    print("Solved superdoku saved to", OUT_PATH)
