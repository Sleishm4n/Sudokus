import os
from pathlib import Path
import subprocess
import time

SUPPORTED_FILES = [".py", ".java", ".c", ".cpp", ".rs"]

LANG_COMMANDS = {
    ".py": lambda f: ["python3", str(f)],
    ".c": lambda f: ["make", f.stem],
    ".cpp": lambda f: ["make", f.stem],
    ".java": lambda f: ["javac", f.name, "&&", "java", f.stem],
    ".rs": lambda f: ["rustc", f.name]
}

def load_sudoku(filename):
    file = open(filename)
    sudoku = []
    for line in file:
        sudoku.append([int(x) for x in line.split()])
    
    return sudoku
    
def display_sudoku(filename):
    sudoku = load_sudoku(filename)
    print()
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            cell = sudoku[i][j]
            print(cell if cell != 0 else ".", end=" ")
        print()
    print()

def get_files(programs_dir):
    return [f for f in programs_dir.iterdir()
            if f.is_file() and f.suffix in SUPPORTED_FILES and f.name != "SudokuCreator.py"]

def display_files(files):
    for i, file in enumerate(files, 1):
        print(f"{i}: {file}")

def get_user_selection(num_files):
    while True:
        try:
            choice = int(input("Which file do you want to run > "))
            if 1 <= choice <= num_files:
                return choice - 1
        except ValueError:
            pass
        print("Invalid selection")

def run(file):
    ext = file.suffix

    start = time.perf_counter()

    try:
        if ext == ".java":
            run_java(file)
        elif ext in [".c", ".cpp"]:
            run_c(file)
        elif ext == ".rs":
            run_rust(file)
        else:
            command = LANG_COMMANDS[file.suffix](file)
            subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error: {file.name} failed to run. Check compilation or missing dependencies.")

    end = time.perf_counter()
    print(f"{str(file)} solved the Sudoku in {end-start:.3f} seconds.\n")

def run_java(file):
    subprocess.run(["javac", str(file)], check=True)
    subprocess.run(["java", f"programs.{file.stem}"], check=True)

def run_c(file):
    compiler = "gcc" if file.suffix == ".c" else "g++"
    output = file.stem
    exe_name = output + (".exe" if os.name == "nt" else "")
    try:
        # Compile
        subprocess.run([compiler, str(file), "-o", exe_name], check=True)
        # Run executable
        subprocess.run([f"./{exe_name}"], check=True)
    except subprocess.CalledProcessError:
        print(f"Error: {file.name} failed to compile or run.")

def run_rust(file):
    exe_name = file.stem + ".exe"
    try:
        subprocess.run(["rustc", str(file)], check=True)
        subprocess.run([exe_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {file.name} failed to compile or run.")
        print(e)

def launch():
    files = get_files(programs_dir)
    display_files(files)
    selection = get_user_selection(len(files))
    run(files[selection])
    display_sudoku("./sudoku_solved.txt")

def welcome():
    print(" 1: Make new sudoku \n 2: See current sudoku \n 3: Enter program selection")

    while True:
        try:
            choice = int(input("Enter choice > "))
            if 1 <= choice <= 3:
                break
        except ValueError:
            pass
        print("Invalid selection")

    if choice == 1:
        creator_file = programs_dir / "SudokuCreator.py"
        run(creator_file)
        display_sudoku("./sudoku.txt")
        welcome()
    elif choice == 2:
        display_sudoku("./sudoku.txt")
        welcome()
    else:
        launch()

if __name__ == "__main__":
    programs_dir = Path("./programs")
    print("Welcome to the Sudoku Project...")
    welcome()
