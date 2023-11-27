import tkinter as tk
from tkinter import messagebox, Scale, IntVar, simpledialog
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.difficulty_var = IntVar()
        difficulty_scale = Scale(self.root, label="Difficulty Level", from_=1, to=10, orient="horizontal", variable=self.difficulty_var)
        difficulty_scale.grid(row=9, column=2, columnspan=4)

        new_puzzle_button = tk.Button(self.root, text="New Puzzle", command=self.create_new_puzzle)
        new_puzzle_button.grid(row=9, column=0, columnspan=2)

        check_button = tk.Button(self.root, text="Check", command=self.check_puzzle)
        check_button.grid(row=9, column=6, columnspan=2)

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=9, column=4, columnspan=2)

    def generate_sudoku(self, difficulty):
        board = [[0] * 9 for _ in range(9)]
        solve_sudoku(board)

        # Adjust difficulty by controlling the number of filled cells
        filled_cells = random.randint(12 + difficulty, 28 + difficulty)
        for _ in range(filled_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0

        return board

    def create_board_gui(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Entry, tk.Label, Scale)):
                widget.destroy()

        for i in range(9):
            for j in range(9):
                cell_value = self.board[i][j]
                if cell_value != 0:
                    label = tk.Label(self.root, text=str(cell_value), width=4, height=2, relief="solid", borderwidth=1)
                else:
                    entry_var = tk.StringVar()
                    entry = tk.Entry(self.root, textvariable=entry_var, width=4, justify="center", bd=1)
                    entry.insert(0, "")
                    entry_var.trace_add("write", lambda name, index, mode, entry=entry: self.validate_entry(entry))
                    label = entry
                label.grid(row=i, column=j, padx=2, pady=2)

    def validate_entry(self, entry):
        value = entry.get()
        if value and not value.isdigit():
            entry.delete(0, tk.END)

    def create_new_puzzle(self):
        difficulty = self.difficulty_var.get()

        # Ask for confirmation on the difficulty level
        confirmed_difficulty = self.confirm_difficulty(difficulty)
        if confirmed_difficulty is None:
            return  # User canceled the operation

        self.board = self.generate_sudoku(confirmed_difficulty)
        self.create_board_gui()

    def confirm_difficulty(self, difficulty):
        # Ask the user for confirmation on the difficulty level
        message = f"Are you sure you want to generate a puzzle with difficulty level {difficulty}?"
        result = messagebox.askyesno("Confirm Difficulty", message)
        if result:
            return difficulty
        else:
            return None

    def check_puzzle(self):
        current_board = [[int(entry.get()) if isinstance(entry, tk.Entry) and entry.get().isdigit() else 0 for entry in self.root.grid_slaves(row=i, column=j)] for i in range(9) for j in range(9)]
        if self.is_board_correct(current_board):
            messagebox.showinfo("Sudoku Solver", "Sudoku is correct!")
        else:
            messagebox.showwarning("Sudoku Solver", "Sudoku is not correct.")

    def is_board_correct(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != self.board[i][j]:
                    return False
        return True

    def solve_puzzle(self):
        solved_board = [row[:] for row in self.board]
        if solve_sudoku(solved_board):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        entry = self.root.grid_slaves(row=i, column=j)[0]
                        entry.delete(0, tk.END)
                        entry.insert(0, str(solved_board[i][j]))
            messagebox.showinfo("Sudoku Solver", "Puzzle solved!")
        else:
            messagebox.showwarning("Sudoku Solver", "No solution exists for the current puzzle.")

def is_valid_move(board, row, col, num):
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_sudoku(board):
    empty_location = find_empty_location(board)
    if not empty_location:
        return True

    row, col = empty_location
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
