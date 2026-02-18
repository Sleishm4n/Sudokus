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
    ".rs": lambda f: ["rustc", f.name],
}


def load_sudoku(filename):
    file = open(filename)
    sudoku = []
    for line in file:
        sudoku.append([int(x) for x in line.split()])
    return sudoku


def load_superdoku(filename):
    file = open(filename)
    sudoku = []
    for line in file:
        row = []
        for x in line.split():
            row.append(int(x) if x.isdigit() else x)
        sudoku.append(row)
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


def display_superdoku(filename):
    sudoku = load_superdoku(filename)
    print()
    for i in range(16):
        if i % 4 == 0 and i != 0:
            print("------------+-------------+-------------+------------")
        for j in range(16):
            if j % 4 == 0 and j != 0:
                print("|", end=" ")
            cell = sudoku[i][j]
            print(f"{cell if cell != 0 else '.':>2}", end=" ")
        print()
    print()


def get_implementations(languages_dir):
    implementations = []
    for item in languages_dir.rglob("*"):
        if item.is_file() and item.suffix in SUPPORTED_FILES:
            rel_path = item.relative_to(languages_dir)
            implementations.append((str(rel_path), item))
    return sorted(implementations)


def display_implementations(implementations):
    print("\n" + "=" * 60)
    for i, (display_name, _) in enumerate(implementations, 1):
        print(f"{i:2d}. {display_name}")
    print("=" * 60)


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
        print(
            f"Error: {file.name} failed to run. Check compilation or missing dependencies."
        )

    end = time.perf_counter()
    print(f"\n{str(file)} solved the Sudoku in {end-start:.3f} seconds.")


def run_java(file):
    abs_path = file.resolve()

    subprocess.run(["javac", str(abs_path)], check=True, cwd=file.parent)

    # Run from the file's directory (no package prefix needed)
    subprocess.run(["java", file.stem], check=True, cwd=file.parent)


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
    output_dir = Path("compiled")
    output_dir.mkdir(exist_ok=True)

    exe_name = output_dir / f"{file.stem}_rust"
    if os.name == "nt":
        exe_name = exe_name.with_suffix(".exe")

    try:
        subprocess.run(["rustc", str(file), "-o", str(exe_name)], check=True)
        subprocess.run([str(exe_name)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {file.name} failed to compile or run.")
        print(e)


def create_new_puzzle():
    creator = Path("utils/SudokuCreator9_9.py")
    if creator.exists():
        print("\nGenerating new puzzle...\n")
        subprocess.run(["python3", str(creator)], check=True)
        return True
    print("Error: SudokuCreator9_9.py not found.")
    return False


def create_new_superdoku_puzzle():
    creator = Path("utils/SuperdukoCreator.py")
    if creator.exists():
        print("\nGenerating new superdoku puzzle...\n")
        subprocess.run(["python3", str(creator)], check=True)
        return True
    print("Error: SuperdukoCreator.py not found.")
    return False


def launch():
    languages_dir = Path("languages")

    implementations = get_implementations(languages_dir)
    display_implementations(implementations)
    selection = get_user_selection(len(implementations))
    _, file = implementations[selection]

    run(file)

    if "superduk" in str(file).lower():
        solved_file = Path("puzzles/superdoku_solved.txt")
        if solved_file.exists():
            print("\nSolved superdoku:")
            display_superdoku(str(solved_file))
    else:
        solved_file = Path("puzzles/sudoku_9_9_solved.txt")
        if solved_file.exists():
            print("\nSolved puzzle:")
            display_sudoku(str(solved_file))


def welcome():
    print("\n" + "=" * 60)
    print("1: Make new sudoku")
    print("2: See current sudoku")
    print("3: Run a solver")
    print("4: Make new superdoku")
    print("5: See current superdoku")
    print("6: Exit")
    print("=" * 60)

    while True:
        try:
            choice = int(input("\nEnter choice > "))
            if 1 <= choice <= 6:
                break
        except ValueError:
            pass
        except KeyboardInterrupt:
            print("\n\nExiting Sudoku Project. Goodbye!")
            exit(0)
        print("Invalid selection")

    if choice == 1:
        if create_new_puzzle():
            display_sudoku("puzzles/sudoku_9_9.txt")
        welcome()
    elif choice == 2:
        display_sudoku("puzzles/sudoku_9_9.txt")
        welcome()
    elif choice == 3:
        launch()
        welcome()
    elif choice == 4:
        if create_new_superdoku_puzzle():
            display_superdoku("puzzles/superdoku.txt")
        welcome()
    elif choice == 5:
        display_superdoku("puzzles/superdoku.txt")
        welcome()
    else:
        print("\nExiting Sudoku Project. Goodbye!")
        exit(0)


if __name__ == "__main__":
    print("Welcome to the Sudoku Project...")
    welcome()
