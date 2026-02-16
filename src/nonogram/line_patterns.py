from __future__ import annotations
from typing import List

FILLED = "#"
EMPTY = "."
UNKNOWN = "?"

def generate_line_patterns(length: int, clue: List[int]) -> List[str]:
    """
    Generate all valid patterns for a line of given length that satisfy the clue.
    Pattern is a string of '#' (filled) and '.' (empty).

    Example: length=5, clue=[3] -> ['###..', '.###.', '..###']
    """
    if length < 0:
        raise ValueError("length must be non-negative")

    # Empty clue -> all empty
    if not clue:
        return [EMPTY * length]

    results: List[str] = []

    def backtrack(pos: int, clue_idx: int, line: List[str]) -> None:
        if clue_idx == len(clue):
            # Fill remainder with empty and record
            for k in range(pos, length):
                line[k] = EMPTY
            results.append("".join(line))
            return

        block = clue[clue_idx]

        # Minimum cells needed for remaining blocks including separators
        remaining = clue[clue_idx:]
        min_needed = sum(remaining) + (len(remaining) - 1)
        latest_start = length - min_needed

        for start in range(pos, latest_start + 1):
            # empties before block
            for k in range(pos, start):
                line[k] = EMPTY

            # place block
            for k in range(start, start + block):
                line[k] = FILLED

            next_pos = start + block

            if clue_idx < len(clue) - 1:
                # need separator empty if more blocks remain
                if next_pos < length:
                    line[next_pos] = EMPTY
                backtrack(next_pos + 1, clue_idx + 1, line)
            else:
                backtrack(next_pos, clue_idx + 1, line)

    backtrack(0, 0, [EMPTY] * length)
    return results

def filter_patterns(patterns: List[str], known: str) -> List[str]:
    """
    Remove patterns that contradict known cells.
    known is a string of length n made of '#', '.', '?'
    """
    out: List[str] = []
    for p in patterns:
        ok = True
        for pc, kc in zip(p, known):
            if kc != UNKNOWN and pc != kc:
                ok = False
                break
        if ok:
            out.append(p)
    return out

def forced_cells(patterns: List[str]) -> str:
    """
    Given remaining valid patterns for a line, return a string of forced cells:
    - '#' if all patterns have '#'
    - '.' if all patterns have '.'
    - '?' otherwise
    """
    if not patterns:
        raise ValueError("forced_cells called with empty pattern list")

    n = len(patterns[0])
    forced = []
    for i in range(n):
        col = {p[i] for p in patterns}
        if col == {FILLED}:
            forced.append(FILLED)
        elif col == {EMPTY}:
            forced.append(EMPTY)
        else:
            forced.append(UNKNOWN)
    return "".join(forced)

