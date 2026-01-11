package programs;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

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

    public static void main(String[] args) throws FileNotFoundException, IOException {

        int[][] sudoku = new int[9][9];
        
        File file = new File("./sudoku.txt");

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            int row = 0;

            while ((line = br.readLine()) != null) {
                String[] vals = line.trim().split("\\s+");

                for (int col = 0; col < 9; col++) {
                    sudoku[row][col] = Integer.parseInt(vals[col]);
                }

                row++;
            }
        }

        Sudoku solver = new Sudoku();
        solver.solveSudoku(sudoku);

        try (java.io.FileWriter fw = new java.io.FileWriter("./sudoku_solved.txt")) {
            for (int[] row : sudoku) {
                for (int i = 0; i < row.length; i++) {
                    fw.write(String.valueOf(row[i]));
                    if (i < row.length - 1) fw.write(" ");
                }
                fw.write("\n");
            }
        }
    }
}