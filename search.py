"""The search: fill the box cell by cell.

Take the first empty cell. Every cell before it is full, so the only question
is which piece covers it. Try each candidate of that cell that fits: lay it,
and start again from the new first empty cell. If nothing fits, this branch
is a dead end: lift the last piece and try its next candidate.

Only the current branch is kept, never the tree: at most one piece per
level, as many levels as there are pieces.
"""

import time
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class Stats:
    placed: int = 0      # pieces laid
    removed: int = 0     # pieces lifted again
    dead_ends: int = 0   # first empty cells that no candidate could cover
    deepest: int = 0     # most pieces on the board at once
    started: float = field(default_factory=time.perf_counter)
    report: Optional[Callable] = None  # called as report(stats, board)
    every: int = 100_000               # ... every this many pieces laid

    @property
    def elapsed(self):
        return time.perf_counter() - self.started


def solve(board, table, stats):
    """Fill the board. Return True with the board full, or False with the
    board as it was given, once every branch has been tried."""
    cell = board.first_empty()
    if cell is None:
        return True
    tried = False
    for candidate in table[cell]:
        if not board.fits(candidate):
            continue
        tried = True
        board.place(candidate)
        stats.placed += 1
        stats.deepest = max(stats.deepest, len(board.stack))
        if stats.report and stats.placed % stats.every == 0:
            stats.report(stats, board)
        if solve(board, table, stats):
            return True
        board.remove()
        stats.removed += 1
    if not tried:
        stats.dead_ends += 1
    return False
