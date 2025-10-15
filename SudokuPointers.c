#include <stdio.h>
#include <stdlib.h>

// Print the sudoku row by row
void print(int *sudoku)
{
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {
			printf("%d ", *(sudoku + i * 9 + j));
		}
		printf("\n");
	}
}


int validNum(int *sudoku, int row, int col, int num)
{
	// check if num exists in column
	for (int i = 0; i < 9; i++) {
		if ( *(sudoku + i * 9 + col) == num ) 
			return 0;
	}

	// check if num exists in row
	for (int i = 0; i < 9; i++) {
		if ( *(sudoku + row * 9 + i) == num )
			return 0;
	}

	// check 3x3 matrix for num
	int startRow = row - (row % 3);
	int startCol = col - (col % 3);

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if ( *(sudoku + (startRow + i) * 9 + (startCol + j)) == num)
				return 0;
		}
	}

	// return true
	return 1;
}

int solveSudoku(int *sudoku, int row, int col)
{
	// base case reached ninth column of last row
	if (row == 9)
		return 1;

	// if last column reached in row, move to next
	if (col == 9)
		return solveSudoku(sudoku, row + 1, 0);

	// if number from 1-9 in box then move on
	if ( *(sudoku + row * 9 + col) != 0)
		return solveSudoku(sudoku, row, col + 1);

	// check if number is going to be valud in box
	for (int num = 1; num <= 9; num++) {
		if (validNum(sudoku, row, col, num) == 1) {
			*(sudoku + row * 9 + col) = num;
			if (solveSudoku(sudoku, row, col + 1) == 1)
				return 1;
		}
		*(sudoku + row * 9 + col) = 0;
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

	solveSudoku(&sudoku[0][0], 0, 0);
	print(&sudoku[0][0]);

	return 0;
}
