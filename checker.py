"""The judge: decides whether a filled box is a valid solution.

It shares no code with the search on purpose. It only knows the output
format: a flat list of piece numbers, cell (x, y, z) at index
x + nx * y + nx * ny * z, and 0 for an empty cell.
"""

from collections import defaultdict

PIECE_SIZE = 5


def coords(i, dims):
    nx, ny, _ = dims
    return (i % nx, (i // nx) % ny, i // (nx * ny))


def is_y(cells):
    """True if the 5 cells form a Y: 4 cells in a row, and a fifth one
    stuck sideways on the 2nd or the 3rd cell of the row."""
    cells = set(cells)
    if len(cells) != PIECE_SIZE:
        return False
    for axis in range(3):
        others = [a for a in range(3) if a != axis]
        rows = defaultdict(list)
        for c in cells:
            rows[tuple(c[a] for a in others)].append(c)
        for row in rows.values():
            if len(row) != 4:
                continue
            row.sort(key=lambda c: c[axis])
            values = [c[axis] for c in row]
            if values != list(range(values[0], values[0] + 4)):
                continue
            (extra,) = cells - set(row)
            for anchor in (row[1], row[2]):
                diff = [abs(extra[a] - anchor[a]) for a in range(3)]
                if diff[axis] == 0 and sum(diff) == 1:
                    return True
    return False


def check(cells, dims):
    """Return the list of everything wrong with this solution, empty if it
    is valid."""
    nx, ny, nz = dims
    size = nx * ny * nz
    if len(cells) != size:
        return [f"expected {size} cells, got {len(cells)}"]
    errors = []

    groups = defaultdict(list)
    for i, number in enumerate(cells):
        if number == 0:
            errors.append(f"cell {coords(i, dims)} is empty")
        else:
            groups[number].append(coords(i, dims))

    if size % PIECE_SIZE:
        errors.append(f"{size} cells cannot be split into pieces of {PIECE_SIZE}")
    expected = list(range(1, size // PIECE_SIZE + 1))
    if sorted(groups) != expected:
        errors.append(f"piece numbers should be 1 to {len(expected)}, got {sorted(groups)}")

    for number in sorted(groups):
        group = groups[number]
        if len(group) != PIECE_SIZE:
            errors.append(f"piece {number} has {len(group)} cells")
        elif not is_y(group):
            errors.append(f"piece {number} is not a Y: {sorted(group)}")
    return errors
