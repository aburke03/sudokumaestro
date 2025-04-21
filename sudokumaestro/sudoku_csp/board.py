from typing import List, Optional

class Board:
    def __init__(self, grid: Optional[List[List[int]]] = None):
        self.grid = grid if grid else [[0 for _ in range(9)] for _ in range(9)]
        # Check if placing val at (row, col) is valid
    def is_valid_move(self, row: int, col: int, val: int) -> bool:
        
        # Check row
        for i in range(9):
            if self.grid[row][i] == val:
                return False
        # Check column
        for i in range(9):
            if self.grid[i][col] == val:
                return False
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == val:
                    return False
        return True

    def copy(self) -> "Board":
        # Return a deep copy of the board
        new_grid = [row.copy() for row in self.grid]
        return Board(new_grid)

    def __str__(self) -> str:
        # String representation of the board for debugging
        rows = []
        for r in self.grid:
            rows.append(" ".join(str(v) for v in r))
        return "\n".join(rows)

    def is_complete(self) -> bool:
        # Return True if the board is completely filled (no zeros)
        return all(v != 0 for row in self.grid for v in row)

    def next_empty_cell(self):
        # Return the (row, col) of the next empty cell or None if full
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def possible_values(self, row: int, col: int) -> List[int]:
        # Return a list of valid values for the cell at (row, col)
        if self.grid[row][col] != 0:
            return []
        values = []
        for v in range(1, 10):
            if self.is_valid_move(row, col, v):
                values.append(v)
        return values

    def set(self, row: int, col: int, val: int) -> None:
        # Set the cell at (row, col) to val
        self.grid[row][col] = val
