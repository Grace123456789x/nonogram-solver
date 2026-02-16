from nonogram.line_patterns import (
    generate_line_patterns,
    filter_patterns,
    forced_cells
)

def test_generate_line_patterns_single_block():
    assert generate_line_patterns(5, [3]) == ["###..", ".###.", "..###"]

def test_generate_line_patterns_empty_clue():
    assert generate_line_patterns(4, []) == ["...."]

def test_filter_patterns_respects_known_cells():
    pats = generate_line_patterns(5, [3])
    # known has a forced filled in the middle
    filtered = filter_patterns(pats, "??#??")
    assert filtered == ["###..", ".###.", "..###"]  # all have middle '#'

    # known says last cell must be filled -> only '..###' survives
    filtered2 = filter_patterns(pats, "????#")
    assert filtered2 == ["..###"]

def test_forced_cells_overlap():
    pats = generate_line_patterns(5, [3])  # ###.. .###. ..###
    # overlap forces the middle cell to '#'
    assert forced_cells(pats) == "??#??"

