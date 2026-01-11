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
	int sudoku[9][9];

	FILE *fptr = fopen("./sudoku.txt", "r");

	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			fscanf(fptr, "%d", &sudoku[i][j]);
		}
	}

	fclose(fptr);
	solveSudoku(sudoku, 0, 0);

	FILE *outfptr = fopen("./sudoku_solved.txt", "w");
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			fprintf(outfptr, "%d ", sudoku[i][j]);
		}
		fprintf(outfptr, "\n");
	}
	fclose(outfptr);

	return 0;
}
