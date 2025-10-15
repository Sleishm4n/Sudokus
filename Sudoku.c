#include <stdio.h>
#include <stdlib.h>

void print(int sudoku[9][9])
{
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			printf("%d ", sudoku[i][j]);
		}
		printf("\n");
	}
}

int validNum(int sudoku[9][9], int row, int col, int num)
{
	for (int i = 0; i < 9; i++) {
		if (sudoku[i][col] == num) {
			return 0;
		}
	}

	for (int i = 0; i < 9; i++) {
		if (sudoku[row][i] == num) {
			return 0;
        	}
    	}

	int startRow = row - (row % 3);
	int startCol = col - (col % 3);

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if (sudoku[i + startRow][j + startCol] == num) {
				return 0;
			}
		}
	}

	return 1;
}

int solveSudoku(int sudoku[9][9], int row, int col) {

	if (row == 9) {
		return 1;
	}

	if (col == 9) {
		return solveSudoku(sudoku, row + 1, 0);
	}

	if (sudoku[row][col] != 0) {
		return solveSudoku(sudoku, row, col + 1);
	}

	for (int num = 1; num <= 9; num++) {
		if (validNum(sudoku, row, col, num) == 1) {
		       sudoku[row][col] = num;
		       if (solveSudoku(sudoku, row, col + 1) == 1) {
			       return 1;
		       }
		}
		sudoku[row][col] = 0;
	}

	return 0;

}

int main()
{
    	int sudoku[9][9] = {
        	{2, 0, 3, 0, 0, 9, 5, 0, 0},
        	{1, 9, 5, 0, 0, 2, 4, 8, 0},
	        {0, 0, 0, 8, 0, 5, 2, 1, 9},
       		{0, 2, 0, 0, 5, 0, 6, 0, 4},
        	{4, 5, 9, 0, 0, 0, 0, 0, 1},
        	{0, 0, 0, 7, 8, 4, 0, 0, 5},
        	{0, 0, 0, 3, 0, 0, 1, 4, 8},
        	{9, 6, 0, 0, 4, 0, 0, 5, 0},
        	{3, 1, 0, 0, 2, 0, 0, 0, 0}};

	solveSudoku(sudoku, 0, 0);
	print(sudoku);

	return 0;
}
