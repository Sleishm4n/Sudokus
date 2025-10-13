

public class Sudoku {

    public boolean validNum(int[][] sudoku, int row, int col, int num) {

        // check if num exists in column
        for (int i = 0; i < 9; i++) {
            if (sudoku[i][col] == num) {
                return false;
            }
        }

        // check if num exists in row
        for (int i = 0; i < 9; i++) {
            if (sudoku[row][i] == num) {
                return false;
            }
        }

        // check 3x3 matrix for num
        int startRow = row - (row % 3);
        int startCol = col - (col % 3);

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (sudoku[i + startRow][j + startCol] == num) {
                    return false;
                }
            }
        }

        return true;
    }

    public boolean solveSudokuRec(int[][] sudoku, int row, int col) {

        // base case reached nth column of last row
        if (row == 9) {
            return true;
        }

        // if last column reached in row, move to next
        if (col == 9) {
           return solveSudokuRec(sudoku, row + 1, 0);
        }

        // if a number from 1 to 9 is in box then move on
        if (sudoku[row][col] != 0) {
            return solveSudokuRec(sudoku, row, col + 1);
        }

        // check if number is going to be valid in box
        for (int num = 1; num <= 9; num++) {
            if (validNum(sudoku, row, col, num)) {
                sudoku[row][col] = num;
                if (solveSudokuRec(sudoku, row, col)) {
                    return true;
                }
                sudoku[row][col] = 0;
            }
        }

        return false;
    }

    public void solveSudoku(int[][] sudoku) {
        solveSudokuRec(sudoku, 0, 0);
    }

    public static void main(String[] args) {

        // initialisation of unsolved sudoku
        int[][] sudoku = {
            {2, 0, 3, 0, 0, 9, 5, 0, 0},
            {1, 9, 5, 0, 0, 2, 4, 8, 0},
            {0, 0, 0, 8, 0, 5, 2, 1, 9},
            {0, 2, 0, 0, 5, 0, 6, 0, 4},
            {4, 5, 9, 0, 0, 0, 0, 0, 1},
            {0, 0, 0, 7, 8, 4, 0, 0, 5},
            {0, 0, 0, 3, 0, 0, 1, 4, 8},
            {9, 6, 0, 0, 4, 0, 0, 5, 0},
            {3, 1, 0, 0, 2, 0, 0, 0, 0}
        };

        Sudoku solver = new Sudoku();
        solver.solveSudoku(sudoku);

        for (int[] row : sudoku) {
            for (int num : row) {
                System.out.print(num + " ");
            }
            System.out.println();
        }
    }
}