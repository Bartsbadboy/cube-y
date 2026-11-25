import unittest

from candidates import build_table
from checker import is_y
from geometry import Box, ORIENTATIONS, normalize

CUBE = Box(5, 5, 5)
RECTANGLE = Box(10, 5, 1)


def placements(table):
    """The distinct sets of 5 cells found anywhere in the table."""
    return {c.cells for cell_list in table for c in cell_list}


class Table(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = build_table(CUBE)

    def test_one_list_per_cell(self):
        self.assertEqual(len(self.table), CUBE.size)

    def test_every_candidate_covers_its_cell(self):
        for cell, cell_list in enumerate(self.table):
            for c in cell_list:
                self.assertIn(cell, c.cells)

    def test_orientation_and_anchor_match_the_cells(self):
        for cell, cell_list in enumerate(self.table):
            for c in cell_list:
                coords = [CUBE.coords(i) for i in c.cells]
                # The cells, moved into the corner, are the announced shape...
                self.assertEqual(normalize(coords), ORIENTATIONS[c.orientation])
                # ...and the anchor cube of that shape lands on the cell.
                corner = tuple(min(p[a] for p in coords) for a in range(3))
                anchor = ORIENTATIONS[c.orientation][c.anchor]
                landed = tuple(corner[a] + anchor[a] for a in range(3))
                self.assertEqual(landed, CUBE.coords(cell))

    def test_every_candidate_is_a_y_inside_the_box(self):
        for cell_list in self.table:
            for c in cell_list:
                self.assertEqual(len(set(c.cells)), 5)
                self.assertTrue(all(0 <= i < CUBE.size for i in c.cells))
                self.assertTrue(is_y([CUBE.coords(i) for i in c.cells]), c)

    def test_at_most_120_per_cell(self):
        for cell_list in self.table:
            self.assertLessEqual(len(cell_list), 24 * 5)

    def test_no_duplicate_in_a_cell(self):
        for cell_list in self.table:
            self.assertEqual(len({c.cells for c in cell_list}), len(cell_list))

    def test_960_placements_in_the_cube(self):
        # Every shape fits in a 4 x 2 x 1 block, in some order of the axes.
        # Such a block slides (5-4+1) * (5-2+1) * (5-1+1) = 2 * 4 * 5 = 40
        # ways in the cube, whatever the order: 24 shapes * 40 = 960.
        self.assertEqual(len(placements(self.table)), 960)

    def test_each_placement_is_listed_under_each_of_its_cells(self):
        # A placement covers 5 cells, so it appears in exactly 5 lists.
        self.assertEqual(sum(len(cell_list) for cell_list in self.table), 960 * 5)


class Rectangle(unittest.TestCase):
    def test_184_placements(self):
        # Only the 8 flat shapes fit in one layer. 4 lie along x in a 4 x 2
        # block: (10-4+1) * (5-2+1) = 28 positions each. 4 lie along y in a
        # 2 x 4 block: (10-2+1) * (5-4+1) = 18 each. 4*28 + 4*18 = 184.
        table = build_table(RECTANGLE)
        self.assertEqual(len(placements(table)), 184)


if __name__ == "__main__":
    unittest.main()
