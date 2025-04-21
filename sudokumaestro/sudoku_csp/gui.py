import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from .board import Board
from .generator import generate_full_board, puzzle_from_full
from .solver import solve
from .timer import Timer
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SudokuMaestroGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Maestro")
        # Canvas setup (blank grid)
        width = 450
        height = 450
        self.cell_size = width // 9
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.draw_grid_lines()
        # Number items
        self.number_items = {}
        # Initial board
        self.board = Board()
        # Track initial puzzle cells for coloring and animation
        self.initial_cells = set()
        self.redraw_numbers()
        # Controls
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10)
        self.gen_btn = ctk.CTkButton(control_frame, text="Generate New Board", command=self.generate_new_board)
        self.gen_btn.pack(side="left", padx=5)
        self.solve_btn = ctk.CTkButton(control_frame, text="Solve", command=self.solve_board)
        self.solve_btn.pack(side="left", padx=5)
        # Status bar
        self.status_label = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_label.pack(fill="x", side="bottom", padx=10, pady=5)

    def draw_grid_lines(self):
        # Draw 9x9 grid with bold lines for 3x3 boxes
        for i in range(10):
            width = 2 if i % 3 == 0 else 1
            pos = i * self.cell_size
            self.canvas.create_line(pos, 0, pos, self.cell_size * 9, width=width)
            self.canvas.create_line(0, pos, self.cell_size * 9, pos, width=width)

    def redraw_numbers(self):
        # Clear existing numbers
        for item in self.number_items.values():
            self.canvas.delete(item)
        self.number_items.clear()
        # Draw numbers
        for r in range(9):
            for c in range(9):
                val = self.board.grid[r][c]
                if val != 0:
                    x = c * self.cell_size + self.cell_size / 2
                    y = r * self.cell_size + self.cell_size / 2
                    # choose color: red for initial puzzle, black for solver-filled
                    fill_color = "red" if (r, c) in self.initial_cells else "black"
                    item = self.canvas.create_text(
                        x, y, text=str(val), font=("Arial", int(self.cell_size / 2)), fill=fill_color
                    )
                    self.number_items[(r, c)] = item

    def generate_new_board(self):
        full = generate_full_board()
        puzzle = puzzle_from_full(full)
        self.board = puzzle
        # record initial puzzle cells
        self.initial_cells = {(r, c) for r in range(9) for c in range(9) if self.board.grid[r][c] != 0}
        self.redraw_numbers()
        self.status_label.configure(text="New board generated.")

    def solve_board(self):
        # Disable buttons
        self.gen_btn.configure(state="disabled")
        self.solve_btn.configure(state="disabled")
        self.status_label.configure(text="Solving...")
        # Start timer
        self.timer = Timer()
        self.timer.start()
        # Solve
        initial_board = self.board.copy()
        solution = solve(initial_board.copy())
        if solution:
            # prepare for animation
            self.solution_board = solution
            # reset to puzzle state
            self.board = initial_board
            # start incremental animation
            self._animate_solution()
        else:
            self.status_label.configure(text="No solution found.")
            self.gen_btn.configure(state="normal")
            self.solve_btn.configure(state="normal")

    # Animation of AI filling cells iteratively
    def _animate_solution(self, idx=0, cells=None):
        if cells is None:
            # list of empty cells in row-major order
            cells = [(r, c) for r in range(9) for c in range(9) if (r, c) not in self.initial_cells]
        if idx >= len(cells):
            # animation complete; stop timer and show elapsed
            elapsed = self.timer.stop()
            self.status_label.configure(text=f"Solved in {elapsed:.3f} s")
            self.gen_btn.configure(state="normal")
            self.solve_btn.configure(state="normal")
            return
        r, c = cells[idx]
        val = self.solution_board.grid[r][c]
        # place value on board and draw
        self.board.set(r, c, val)
        x = c * self.cell_size + self.cell_size / 2
        y = r * self.cell_size + self.cell_size / 2
        item = self.canvas.create_text(
            x, y, text=str(val), font=("Arial", int(self.cell_size / 2)), fill="black"
        )
        self.number_items[(r, c)] = item
        # latency for solving animation (in ms)
        delay = random.randint(25, 100)
        self.after(delay, lambda idx=idx, cells=cells: self._animate_solution(idx+1, cells))
