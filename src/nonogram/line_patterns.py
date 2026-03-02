def generate_patterns(length, clue):
    if clue == []:
        return ["." * length]

    patterns = []

    def helper(i, pos, current):
        if i == len(clue):
            patterns.append(current + "." * (length - pos))
            return

        block = clue[i]
        remaining = clue[i:]
        min_needed = sum(remaining) + (len(remaining) - 1)
        max_start = length - min_needed

        for start in range(pos, max_start + 1):
            s = current
            s += "." * (start - pos)
            s += "#" * block
            new_pos = start + block

            if i < len(clue) - 1:
                s += "."
                new_pos += 1

            helper(i + 1, new_pos, s)

    helper(0, 0, "")
    return patterns


def filter_patterns(patterns, line):
    keep = []
    for p in patterns:
        ok = True
        for j, cell in enumerate(line):
            if cell != '?' and cell != p[j]:
                ok = False
                break
        if ok:
            keep.append(p)
    return keep


def force_from_patterns(patterns):
    length = len(patterns[0])
    forced = []
    for j in range(length):
        col = {p[j] for p in patterns}
        if col == {'#'}:
            forced.append('#')
        elif col == {'.'}:
            forced.append('.')
        else:
            forced.append('?')
    return forced
