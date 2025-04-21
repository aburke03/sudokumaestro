# Sudoku Maestro

A python AI Sudoku solver with a CustomTkinter GUI. Uses a CSP (Constraint Satisfaction Problem), backtracking, forward-checking, and incremental animations. ~Developed by Austin Burke for CSC4444 at LSU.

## GitHub Repository

Clone the repo and enter its directory:
```bash
git clone https://github.com/aburke03/sudokumaestro.git
cd sudokumaestro
```

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

In /sudokumaestro, run the application:
```bash
python main.py
```

---

## Questions & Answers

**1. Explain the task the AI performs.**  
The AI generates and solves Sudoku randomly generated Sudoku puzzles. It first builds a full valid board using randomized backtracking (`generate_full_board`), then removes a set number of cells (`puzzle_from_full`) to create the puzzle. The solver (`solve`) uses CSP with backtracking and forward‑checking to assign values to empty cells. The GUI iteratively animates each assignment in `gui._animate_solution`.

**2. What was your motivation behind building this AI?**  
To showcase how an AI algorithm can solve a complex logic puzzle (Sudoku) much faster than any human while also providing an interactive demonstration of CSP techniques.

**3. Describe your overall approach and why.**  
- **Board model:** `Board` class contains state and constraint checks in (`is_valid_move`).  
- **Generator:** Randomized backtracking ensures a valid full solution.  
- **Puzzle creation:** Create empty cells while preserving solvability.  
- **Solver:** Recursive backtracking with forward-checking prunes invalid paths early.  
- **Animation:** `CustomTkinter` GUI updates each cell iteratively with randomized delays to simulate behavior.

**4. Describe your operational environment.**  
- **Language:** Python 3.13  
- **Libraries:** `customtkinter>=5.2.2`, `tkinter`, `time`, `random`, `typing`  
- **Tools:** PowerShell, VSCode  
- **Platform:** Windows/macOS/Linux

**5. Describe how your AI system works.**  
```
function solve(board):
    if board.is_complete():
        return board
    (r,c) = board.next_empty_cell()
    for v in board.possible_values(r,c):
        if board.is_valid_move(r,c,v):
            board.set(r,c,v)
            if forward_check(board):
                result = solve(board)
                if result:
                    return result
            board.set(r,c,0)
    return None
```
Forward-checking ensures no empty cell has an empty domain. GUI animation calls this solver, then iterates empty cells to display each value.

**6. Describe the outcome of your AI system.**  
- **Performance:** Solves puzzles in ~0.01–0.05 s (algorithmic), plus animated fill with 25–100 ms per cell (3-5s total)
- **Accuracy:** 100% on valid puzzles; detects unsolvable inputs.  
- **UX:** Animated, color‑coded grid: red for initial clues, black for AI‑filled cells.  

---
