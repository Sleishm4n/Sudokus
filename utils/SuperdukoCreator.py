import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # Sudoku/
sys.path.insert(0, str(ROOT / "languages" / "python" / "basic" / "superduko"))

import Superdoku

POSS_CHARS = [1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G"]


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


def createSudoku(clues):
    sudoku = [[0 for _ in range(16)] for _ in range(16)]
    fillSudoku(sudoku)

    removeNums(sudoku, clues)

    return sudoku


def fillSudoku(sudoku):
    for row in range(16):
        for col in range(16):
            if sudoku[row][col] == 0:
                random.shuffle(POSS_CHARS)

                for char in POSS_CHARS:
                    if validChar(sudoku, row, col, char):
                        sudoku[row][col] = char

                        if fillSudoku(sudoku):
                            return True

                        sudoku[row][col] = 0

                return False

    return True


def removeNums(sudoku, clues):
    attempts = clues
    while attempts > 0:
        row, col = random.randint(0, 15), random.randint(0, 15)

        if sudoku[row][col] != 0:
            backup = sudoku[row][col]
            sudoku[row][col] = 0

            test_sudoku = [row[:] for row in sudoku]

            if not Superdoku.solveSudoku(test_sudoku, 0, 0):
                sudoku[row][col] = backup

            attempts -= 1


if __name__ == "__main__":
    # Create a Sudoku puzzle
    # Difficulty level: 30-35 (easy), 40-45 (medium), 50-55 (hard)
    print("What level of difficulty?\n")
    print("30-35 (easy), 40-45 (medium), 50-55 (hard)\n")
    while True:
        try:
            difficulty = int(input("Difficulty: "))
            if 30 <= difficulty <= 55:
                break
        except ValueError:
            pass
        print("Invalid selection")

    puzzle = createSudoku(difficulty)

    puzzle_file = Path("puzzles/superdoku.txt")

    with open(puzzle_file, "w") as file:
        for row in puzzle:
            file.write(" ".join(str(x) for x in row) + "\n")

    print(f"\nPuzzle saved to {puzzle_file}")
