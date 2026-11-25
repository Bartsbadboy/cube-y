"""What you read and what you build from.

The box is shown one layer at a time, from the bottom (z = 0) up. In each
layer, the top row is y = 0 and the left column is x = 0. Every cell shows
the number of its piece, on two digits, or `.` when it is still empty.

The same text is what gets saved to a file, and `parse` reads it back, so a
saved solution can always be judged again.
"""

EMPTY = "."


def layers(cells, box):
    width = max(2, len(str(max(cells, default=0))))
    lines = []
    for z in range(box.nz):
        lines.append(f"Couche {z + 1} (z = {z})")
        for y in range(box.ny):
            row = []
            for x in range(box.nx):
                n = cells[box.index(x, y, z)]
                row.append(str(n).zfill(width) if n else EMPTY.rjust(width))
            lines.append(" ".join(row))
        lines.append("")
    return "\n".join(lines)


def parse(text, box):
    """Read back the text written by `layers`."""
    rows = [line.split() for line in text.splitlines()
            if line.strip() and not line.startswith("Couche")]
    if len(rows) != box.ny * box.nz or any(len(r) != box.nx for r in rows):
        raise ValueError(f"expected {box.nz} layers of {box.ny} rows of {box.nx} cells")
    cells = [0] * box.size
    for r, row in enumerate(rows):
        z, y = divmod(r, box.ny)
        for x, token in enumerate(row):
            cells[box.index(x, y, z)] = 0 if token == EMPTY else int(token)
    return cells
