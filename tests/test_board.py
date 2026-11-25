import unittest

from board import Board
from candidates import build_table
from checker import check
from geometry import Box
from tests.test_checker import DIMS, RECTANGLE, parse

CUBE = Box(5, 5, 5)
TABLE = build_table(CUBE)


def first_fitting(board, cell):
    return next(c for c in TABLE[cell] if board.fits(c))


class LayAndLift(unittest.TestCase):
    def test_starts_empty(self):
        board = Board(CUBE)
        self.assertEqual(board.cells, [0] * 125)
        self.assertEqual(board.stack, [])
        self.assertEqual(board.first_empty(), 0)

    def test_place_marks_five_cells_with_the_piece_number(self):
        board = Board(CUBE)
        c = TABLE[0][0]
        self.assertEqual(board.place(c), 1)
        self.assertEqual([i for i, n in enumerate(board.cells) if n == 1], list(c.cells))
        self.assertEqual(board.cells.count(0), 120)

    def test_pieces_are_numbered_in_laying_order(self):
        board = Board(CUBE)
        board.place(first_fitting(board, 0))
        self.assertEqual(board.place(first_fitting(board, board.first_empty())), 2)

    def test_first_empty_moves_on(self):
        board = Board(CUBE)
        board.place(first_fitting(board, 0))
        cell = board.first_empty()
        self.assertTrue(all(n != 0 for n in board.cells[:cell]))
        self.assertEqual(board.cells[cell], 0)

    def test_fits_refuses_an_overlap(self):
        board = Board(CUBE)
        c = TABLE[0][0]
        board.place(c)
        self.assertFalse(board.fits(c))
        with self.assertRaises(ValueError):
            board.place(c)

    def test_remove_undoes_place_exactly(self):
        board = Board(CUBE)
        snapshots = []
        for _ in range(6):
            snapshots.append((list(board.cells), list(board.stack)))
            board.place(first_fitting(board, board.first_empty()))
        for cells, stack in reversed(snapshots):
            board.remove()
            self.assertEqual(board.cells, cells)
            self.assertEqual(board.stack, stack)

    def test_remove_on_an_empty_board(self):
        with self.assertRaises(ValueError):
            Board(CUBE).remove()


class FullRectangle(unittest.TestCase):
    def test_laying_the_known_rectangle(self):
        # Lay the judge's rectangle piece by piece, through the table.
        box = Box(*DIMS)
        table = build_table(box)
        expected = parse(RECTANGLE)
        board = Board(box)
        for number in range(1, 11):
            cells = tuple(i for i, n in enumerate(expected) if n == number)
            candidate = next(c for c in table[cells[0]] if c.cells == cells)
            board.place(candidate)
        self.assertIsNone(board.first_empty())
        self.assertEqual(board.cells, expected)
        self.assertEqual(check(board.cells, DIMS), [])


if __name__ == "__main__":
    unittest.main()
