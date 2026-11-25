"""Every way a piece can cover a given cell, computed once.

A candidate is one orientation of the piece, laid so that one of its 5 cubes
(the anchor) sits on the cell. Only candidates that stay inside the box are
kept; collisions with other pieces are the search's business.
"""

from dataclasses import dataclass

from geometry import ORIENTATIONS


@dataclass(frozen=True)
class Candidate:
    orientation: int  # index in ORIENTATIONS
    anchor: int       # which cube of the shape sits on the cell
    cells: tuple      # the 5 cell indices it covers, sorted


def candidates_for(box, cell):
    """Every candidate covering this cell that stays inside the box."""
    cx, cy, cz = box.coords(cell)
    found = []
    for k, shape in enumerate(ORIENTATIONS):
        for j, (ax, ay, az) in enumerate(shape):
            moved = [(cx + x - ax, cy + y - ay, cz + z - az) for x, y, z in shape]
            if all(box.contains(*c) for c in moved):
                cells = tuple(sorted(box.index(*c) for c in moved))
                found.append(Candidate(k, j, cells))
    return found


def build_table(box):
    """One list of candidates per cell, in cell order."""
    return [candidates_for(box, cell) for cell in range(box.size)]
