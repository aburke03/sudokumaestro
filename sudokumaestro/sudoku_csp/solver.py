from typing import Optional
from .board import Board


def forward_check(board: Board) -> bool:
    # Return True if no cell has an empty domain after last assignment
    for r in range(9):
        for c in range(9):
            if board.grid[r][c] == 0 and not board.possible_values(r, c):
                return False
    return True


def solve(board: Board) -> Optional[Board]:
# Solve the board using backtracking + forward-checking
    if board.is_complete():
        return board

    cell = board.next_empty_cell()
    if not cell:
        return board
    r, c = cell

    for v in board.possible_values(r, c):
        if board.is_valid_move(r, c, v):
            board.set(r, c, v)
            if forward_check(board):
                result = solve(board)
                if result:
                    return result
            board.set(r, c, 0)
    return None
