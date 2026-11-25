import unittest

from board import Board
from candidates import build_table
from checker import check
from geometry import Box
from search import Stats, solve


def run(box):
    board = Board(box)
    stats = Stats()
    found = solve(board, build_table(box), stats)
    return found, board, stats


class SmallBoxes(unittest.TestCase):
    def test_the_10_by_5_rectangle_is_filled(self):
        box = Box(10, 5, 1)
        found, board, stats = run(box)
        self.assertTrue(found)
        self.assertEqual(check(board.cells, (10, 5, 1)), [])
        self.assertEqual(stats.placed - stats.removed, 10)

    def test_the_5_by_5_square_cannot_be_filled(self):
        box = Box(5, 5, 1)
        found, board, stats = run(box)
        self.assertFalse(found)
        self.assertEqual(board.cells, [0] * 25)
        self.assertEqual(stats.placed, stats.removed)

    def test_a_box_that_is_not_a_multiple_of_5(self):
        found, board, _ = run(Box(4, 2, 1))
        self.assertFalse(found)
        self.assertEqual(board.stack, [])

    def test_a_row_of_5_is_not_a_y(self):
        found, _, stats = run(Box(5, 1, 1))
        self.assertFalse(found)
        self.assertEqual(stats.placed, 0)
        self.assertEqual(stats.dead_ends, 1)


class Report(unittest.TestCase):
    def test_called_every_n_pieces(self):
        calls = []
        box = Box(5, 5, 1)
        stats = Stats(report=lambda s, b: calls.append(s.placed), every=10)
        solve(Board(box), build_table(box), stats)
        self.assertEqual(calls, list(range(10, stats.placed + 1, 10)))


if __name__ == "__main__":
    unittest.main()
