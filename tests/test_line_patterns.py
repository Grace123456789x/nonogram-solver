from nonogram.line_patterns import generate_patterns, filter_patterns, force_from_patterns


def test_generate_patterns():
    assert generate_patterns(5, [3]) == ["###..", ".###.", "..###"]


def test_filter_patterns():
    patterns = ["###..", ".###.", "..###"]
    line = ['?', '.', '?', '?', '?']
    assert filter_patterns(patterns, line) == [".###.", "..###"]


def test_force_from_patterns():
    patterns = ["###..", "###.."]
    assert force_from_patterns(patterns) == ['#', '#', '#', '.', '.']
