import json
from typing import List
from nonogram.line_patterns import generate_line_patterns, filter_patterns, forced_cells, UNKNOWN

def transpose(grid: List[List[str]]) -> List[List[str]]:
    return [list(col) for col in zip(*grid)]

def solve_once(grid: List[List[str]], row_clues: List[List[int]], col_clues: List[List[int]]) -> bool:
    """
    Run one full pass over rows and columns.
    Returns True if it changed anything.
    """
    changed = False
    h, w = len(grid), len(grid[0])

    # Rows
    for r in range(h):
        known = "".join(grid[r])
        pats = filter_patterns(generate_line_patterns(w, row_clues[r]), known)
        if not pats:
            raise ValueError(f"Contradiction in row {r}")
        forced = forced_cells(pats)
        for c in range(w):
            if grid[r][c] == UNKNOWN and forced[c] != UNKNOWN:
                grid[r][c] = forced[c]
                changed = True

    # Columns
    grid_t = transpose(grid)
    for c in range(w):
        known = "".join(grid_t[c])
        pats = filter_patterns(generate_line_patterns(h, col_clues[c]), known)
        if not pats:
            raise ValueError(f"Contradiction in col {c}")
        forced = forced_cells(pats)
        for r in range(h):
            if grid[r][c] == UNKNOWN and forced[r] != UNKNOWN:
                grid[r][c] = forced[r]
                changed = True

    return changed

def solve_logic(grid, rows, cols, max_iters=1000):
    for _ in range(max_iters):
        if not solve_once(grid, rows, cols):
            break
    return grid

def load_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    w, h = data["width"], data["height"]
    rows, cols = data["rows"], data["cols"]
    grid = [[UNKNOWN for _ in range(w)] for _ in range(h)]
    return grid, rows, cols

def pretty_print(grid):
    for row in grid:
        print(" ".join(row))

if __name__ == "__main__":
    grid, rows, cols = load_json("data/example_5x5.json")
    solve_logic(grid, rows, cols)
    pretty_print(grid)

