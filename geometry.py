"""The box and the piece.

A cell is (x, y, z). A shape is a sorted tuple of cells, moved so that its
smallest x, y and z are all 0: two shapes are the same piece in the same
orientation exactly when their tuples are equal.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    nx: int
    ny: int
    nz: int

    @property
    def size(self):
        return self.nx * self.ny * self.nz

    def index(self, x, y, z):
        return x + self.nx * y + self.nx * self.ny * z

    def coords(self, i):
        return (i % self.nx, (i // self.nx) % self.ny, i // (self.nx * self.ny))

    def contains(self, x, y, z):
        return 0 <= x < self.nx and 0 <= y < self.ny and 0 <= z < self.nz


# The Y lying flat: four cubes along x, a fifth on the second one.
#   . # . .
#   # # # #
PIECE = ((0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (1, 1, 0))


def normalize(shape):
    """Move the shape into the corner and sort its cells."""
    mx = min(c[0] for c in shape)
    my = min(c[1] for c in shape)
    mz = min(c[2] for c in shape)
    return tuple(sorted((x - mx, y - my, z - mz) for x, y, z in shape))


def turn_x(shape):
    """A quarter turn around the x axis."""
    return normalize([(x, -z, y) for x, y, z in shape])


def turn_y(shape):
    """A quarter turn around the y axis."""
    return normalize([(z, y, -x) for x, y, z in shape])


def orientations(piece):
    """Every shape the piece can take by turning it: keep applying both
    quarter turns until no new shape appears."""
    start = normalize(piece)
    seen = {start}
    todo = [start]
    while todo:
        shape = todo.pop()
        for turned in (turn_x(shape), turn_y(shape)):
            if turned not in seen:
                seen.add(turned)
                todo.append(turned)
    return sorted(seen)


ORIENTATIONS = orientations(PIECE)
