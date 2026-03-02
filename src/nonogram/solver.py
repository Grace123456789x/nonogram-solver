from nonogram.line_patterns import generate_patterns, filter_patterns, force_from_patterns


def make_grid(H, W):
    return [['?' for _ in range(W)] for _ in range(H)]


def get_col(grid, c):
    col = []
    for r in range(len(grid)):
        col.append(grid[r][c])
    return col


def update_line(line, forced):
    new_line = line[:]
    changed = False

    for j in range(len(line)):
        if forced[j] != '?' and line[j] == '?':
            new_line[j] = forced[j]
            changed = True

    return new_line, changed


def propagate(grid, row_clues, col_clues):
    H = len(grid)
    W = len(grid[0])
    changed = False

    # rows
    for r in range(H):
        line = grid[r]
        patterns = generate_patterns(W, row_clues[r])
        patterns = filter_patterns(patterns, line)

        if patterns == []:
            return grid, changed, False

        forced = force_from_patterns(patterns)
        new_row, row_changed = update_line(line, forced)
        grid[r] = new_row

        if row_changed:
            changed = True

    # columns
    for c in range(W):
        line = get_col(grid, c)
        patterns = generate_patterns(H, col_clues[c])
        patterns = filter_patterns(patterns, line)

        if patterns == []:
            return grid, changed, False

        forced = force_from_patterns(patterns)
        new_col, col_changed = update_line(line, forced)

        for r in range(H):
            grid[r][c] = new_col[r]

        if col_changed:
            changed = True

    return grid, changed, True


def logic_solve(grid, row_clues, col_clues):
    while True:
        grid, changed, ok = propagate(grid, row_clues, col_clues)

        if not ok:
            return None

        if not changed:
            return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))
