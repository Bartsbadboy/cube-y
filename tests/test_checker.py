import unittest

from checker import check, is_y

# A 10 x 5 rectangle filled with 10 Y, one row of text per y.
RECTANGLE = """
 1  2  2  2  2  3  4  4  4  4
 1  1  2  5  3  3  3  3  4  6
 1  5  5  5  5  7  7  7  7  6
 1  8  9  9  9  9  7 10  6  6
 8  8  8  8  9 10 10 10 10  6
"""
DIMS = (10, 5, 1)


def parse(text):
    return [int(n) for n in text.split()]


class IsY(unittest.TestCase):
    def test_flat_y(self):
        self.assertTrue(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (1, 1, 0)]))

    def test_bump_on_the_third_cube(self):
        self.assertTrue(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (2, 0, 1)]))

    def test_standing_y(self):
        self.assertTrue(is_y([(4, 4, 1), (4, 4, 2), (4, 4, 3), (4, 4, 4), (3, 4, 2)]))

    def test_bump_on_the_end_is_an_l(self):
        self.assertFalse(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0)]))

    def test_five_in_a_row_is_an_i(self):
        self.assertFalse(is_y([(i, 0, 0) for i in range(5)]))

    def test_gap_in_the_row(self):
        self.assertFalse(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (4, 0, 0), (1, 1, 0)]))

    def test_bump_not_touching(self):
        self.assertFalse(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (1, 2, 0)]))

    def test_bump_on_a_diagonal(self):
        self.assertFalse(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (1, 1, 1)]))

    def test_four_cells(self):
        self.assertFalse(is_y([(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0)]))


class Check(unittest.TestCase):
    def test_valid_rectangle(self):
        self.assertEqual(check(parse(RECTANGLE), DIMS), [])

    def test_empty_cell(self):
        cells = parse(RECTANGLE)
        cells[0] = 0
        self.assertTrue(any("empty" in e for e in check(cells, DIMS)))

    def test_two_pieces_swapped_cell(self):
        cells = parse(RECTANGLE)
        cells[1] = 1  # piece 1 gets a cell of piece 2
        errors = check(cells, DIMS)
        self.assertTrue(any("piece 1 has 6 cells" in e for e in errors))
        self.assertTrue(any("piece 2 has 4 cells" in e for e in errors))

    def test_wrong_shape(self):
        # Pieces 1 and 8 keep 5 cells each but swap one: neither is a Y.
        cells = parse(RECTANGLE)
        cells[10] = 8   # (0, 1) moves from piece 1 to piece 8
        cells[44] = 1   # (4, 4) moves from piece 8 to piece 1
        errors = check(cells, DIMS)
        self.assertTrue(any("piece 1 is not a Y" in e for e in errors))

    def test_missing_number(self):
        cells = [n if n != 10 else 11 for n in parse(RECTANGLE)]
        self.assertTrue(any("numbers" in e for e in check(cells, DIMS)))

    def test_wrong_length(self):
        self.assertEqual(len(check([1] * 49, DIMS)), 1)


if __name__ == "__main__":
    unittest.main()
