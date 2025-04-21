import random
from typing import List
from .board import Board

def generate_full_board() -> Board:
    # Generate a full solved Sudoku board 
    board = Board()
    def fill():
        cell = board.next_empty_cell()
        if not cell:
            return True
        r, c = cell
        for v in random.sample(range(1, 10), 9):
            if board.is_valid_move(r, c, v):
                board.set(r, c, v)
                if fill():
                    return True
                board.set(r, c, 0)
        return False
    fill()
    return board

    # 52 represents the number of empty cells in the board
def puzzle_from_full(board: Board, holes: int = 52) -> Board:
    # Remove `holes` cells to create a puzzle
    puzzle = board.copy()
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:holes]:
        puzzle.set(r, c, 0)
    return puzzle
