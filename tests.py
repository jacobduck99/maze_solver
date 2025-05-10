import unittest
from maze import Maze
from cell import Cell

class Tests(unittest.TestCase):

    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        # outer list is columns
        self.assertEqual(len(m1._cells), num_cols)
        # each column‐list holds num_rows cells
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_new_maze(self):
        num_cols = 10
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_cells_coordinates(self):
        num_rows    = 6
        num_cols    = 5
        origin_x    = 5
        origin_y    = 5
        cell_width  = 5
        cell_height = 5

        m1 = Maze(origin_x, origin_y, num_rows, num_cols, cell_width, cell_height)

        # shape checks (column-major)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

        # pick one cell at col=2, row=3
        col, row = 2, 3
        cell = m1._cells[col][row]

        # expected coordinates
        expected_x1 = origin_x + col  * cell_width   # 5 + 2*5 = 15
        expected_y1 = origin_y + row  * cell_height  # 5 + 3*5 = 20
        expected_x2 = expected_x1 + cell_width       # 15 + 5 = 20
        expected_y2 = expected_y1 + cell_height      # 20 + 5 = 25

        # trigger the draw so the cell records its corners
        cell.draw(expected_x1, expected_y1, expected_x2, expected_y2)

        # assert that draw() set the values correctly
        self.assertEqual(cell._x1, expected_x1)
        self.assertEqual(cell._y1, expected_y1)
        self.assertEqual(cell._x2, expected_x2)
        self.assertEqual(cell._y2, expected_y2)


    def test_entrance_break_and_exit(self):
        num_rows  = 6
        num_cols  = 5

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        m1._break_entrance_and_exit()

        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

        self.assertFalse(m1._cells[0][0].has_top_wall)



        

if __name__ == "__main__":
    unittest.main()
