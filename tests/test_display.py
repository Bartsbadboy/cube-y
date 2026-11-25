import unittest

from board import Board
from candidates import build_table
from display import layers, parse
from geometry import Box
from tests.test_checker import DIMS, RECTANGLE, parse as parse_fixture

RECT = Box(*DIMS)


class Layers(unittest.TestCase):
    def test_rectangle(self):
        text = layers(parse_fixture(RECTANGLE), RECT)
        self.assertEqual(text.splitlines(), [
            "Couche 1 (z = 0)",
            "01 02 02 02 02 03 04 04 04 04",
            "01 01 02 05 03 03 03 03 04 06",
            "01 05 05 05 05 07 07 07 07 06",
            "01 08 09 09 09 09 07 10 06 06",
            "08 08 08 08 09 10 10 10 10 06",
        ])

    def test_one_block_per_layer_from_the_bottom(self):
        box = Box(2, 2, 3)
        cells = [0] * box.size
        cells[box.index(1, 0, 2)] = 7
        lines = layers(cells, box).splitlines()
        self.assertEqual(lines[0], "Couche 1 (z = 0)")
        self.assertEqual(lines[8], "Couche 3 (z = 2)")
        self.assertEqual(lines[9], " . 07")

    def test_empty_cells(self):
        box = Box(5, 5, 5)
        text = layers([0] * box.size, box)
        self.assertEqual(text.splitlines()[1], " .  .  .  .  .")


class Parse(unittest.TestCase):
    def test_round_trip_full(self):
        cells = parse_fixture(RECTANGLE)
        self.assertEqual(parse(layers(cells, RECT), RECT), cells)

    def test_round_trip_partial_cube(self):
        box = Box(5, 5, 5)
        table = build_table(box)
        board = Board(box)
        for _ in range(4):
            board.place(next(c for c in table[board.first_empty()] if board.fits(c)))
        self.assertEqual(parse(layers(board.cells, box), box), board.cells)

    def test_wrong_size(self):
        with self.assertRaises(ValueError):
            parse(layers(parse_fixture(RECTANGLE), RECT), Box(5, 5, 5))


if __name__ == "__main__":
    unittest.main()
