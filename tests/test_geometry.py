import unittest

from checker import is_y
from geometry import Box, ORIENTATIONS, PIECE, normalize, turn_x, turn_y


class BoxIndex(unittest.TestCase):
    def test_round_trip(self):
        box = Box(5, 5, 5)
        for i in range(box.size):
            self.assertEqual(box.index(*box.coords(i)), i)

    def test_reading_order(self):
        box = Box(5, 5, 5)
        self.assertEqual(box.index(1, 0, 0), 1)
        self.assertEqual(box.index(0, 1, 0), 5)
        self.assertEqual(box.index(0, 0, 1), 25)

    def test_contains(self):
        box = Box(10, 5, 1)
        self.assertTrue(box.contains(9, 4, 0))
        self.assertFalse(box.contains(10, 0, 0))
        self.assertFalse(box.contains(0, 0, 1))
        self.assertFalse(box.contains(-1, 0, 0))


class Orientations(unittest.TestCase):
    def test_the_piece_is_a_y(self):
        self.assertTrue(is_y(PIECE))

    def test_twenty_four(self):
        self.assertEqual(len(ORIENTATIONS), 24)

    def test_all_different(self):
        self.assertEqual(len(set(ORIENTATIONS)), len(ORIENTATIONS))

    def test_all_are_y(self):
        for shape in ORIENTATIONS:
            self.assertTrue(is_y(shape), shape)

    def test_all_in_the_corner(self):
        for shape in ORIENTATIONS:
            for axis in range(3):
                self.assertEqual(min(c[axis] for c in shape), 0)

    def test_four_quarter_turns_come_back(self):
        for shape in ORIENTATIONS:
            for turn in (turn_x, turn_y):
                s = shape
                for _ in range(4):
                    s = turn(s)
                self.assertEqual(s, shape)

    def test_closed_under_turns(self):
        for shape in ORIENTATIONS:
            self.assertIn(turn_x(shape), ORIENTATIONS)
            self.assertIn(turn_y(shape), ORIENTATIONS)

    def test_the_mirror_is_not_a_new_shape(self):
        # The piece is flat: flipping it over is a half turn, not a new piece.
        mirror = normalize([(-x, y, z) for x, y, z in PIECE])
        self.assertIn(mirror, ORIENTATIONS)


if __name__ == "__main__":
    unittest.main()
