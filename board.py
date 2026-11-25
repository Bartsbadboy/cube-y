"""The state of the box while the search runs.

`cells` holds one piece number per cell (0 = empty), in the same order as
`Box.index`: it is both what the search works on and what gets displayed.
`stack` holds the candidates laid so far, in order: piece n is stack[n - 1].

Laying and lifting a piece are the only two ways to change the board, and
each is the exact mirror of the other.
"""


class Board:
    def __init__(self, box):
        self.box = box
        self.cells = [0] * box.size
        self.stack = []

    def first_empty(self):
        """The smallest empty cell, or None when the box is full."""
        try:
            return self.cells.index(0)
        except ValueError:
            return None

    def fits(self, candidate):
        """True if none of the candidate's cells is taken."""
        return all(self.cells[i] == 0 for i in candidate.cells)

    def place(self, candidate):
        """Lay a piece and return its number."""
        if not self.fits(candidate):
            raise ValueError(f"{candidate} overlaps a piece already laid")
        self.stack.append(candidate)
        number = len(self.stack)
        for i in candidate.cells:
            self.cells[i] = number
        return number

    def remove(self):
        """Lift the last piece laid and return it."""
        if not self.stack:
            raise ValueError("no piece to remove")
        candidate = self.stack.pop()
        for i in candidate.cells:
            self.cells[i] = 0
        return candidate
