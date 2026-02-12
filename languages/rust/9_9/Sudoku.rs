use std::fs::File;
use std::io::Write;
use std::io::{BufRead, BufReader};

fn valid_num(sudoku: &[[i32; 9]; 9], row: usize, col: usize, num: i32) -> bool {
    for i in 0..9 {
        if sudoku[i][col] == num {
            return false;
        }
    }

    for i in 0..9 {
        if sudoku[row][i] == num {
            return false;
        }
    }

    let start_row = row - (row % 3);
    let start_col = col - (col % 3);

    for i in 0..3 {
        for j in 0..3 {
            if sudoku[i + start_row][j + start_col] == num {
                return false;
            }
        }
    }
    true
}

fn solve_sudoku(sudoku: &mut [[i32; 9]; 9], row: usize, col: usize) -> bool {
    if row == 9 {
        return true;
    }

    let (next_row, next_col) = if col == 8 {
        (row + 1, 0)
    } else {
        (row, col + 1)
    };

    if sudoku[row][col] != 0 {
        return solve_sudoku(sudoku, next_row, next_col);
    }

    for num in 1..=9 {
        if valid_num(sudoku, row, col, num) {
            sudoku[row][col] = num;

            if solve_sudoku(sudoku, next_row, next_col) {
                return true;
            }

            sudoku[row][col] = 0;
        }
    }

    false
}

fn read_sudoku(path: &str) -> [[i32; 9]; 9] {
    let file = File::open(path).expect("Couldn't open file");
    let reader = BufReader::new(file);

    let mut grid = [[0; 9]; 9];

    for (row, line) in reader.lines().enumerate() {
        let line = line.expect("Couldnt to read line");

        for (col, val) in line.split_whitespace().enumerate() {
            grid[row][col] = val.parse().expect("Not int")
        }
    }

    grid
}

fn save_sudoku(path: &str, sudoku: &[[i32; 9]; 9]) {
    let mut file = File::create(path).expect("Couldnt make file");

    for row in sudoku {
        for num in row {
            write!(file, "{} ", num).expect("failed to write");
        }
        writeln!(file).expect("write failed")
    }
}

fn main() {
    let mut sudoku = read_sudoku("puzzles/sudoku_9_9.txt");

    solve_sudoku(&mut sudoku, 0, 0);

    save_sudoku("puzzles/sudoku_9_9_solved.txt", &sudoku);
}
