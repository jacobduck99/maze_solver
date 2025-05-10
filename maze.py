import time
import random
from cell import Cell

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        # column-first grid
        for col in range(self._num_cols):
            col_cells = []
            for row in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        # initial draw so we see the empty grid
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        # i = column → X, j = row → Y
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # open top wall at entrance
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        # open bottom wall at exit
        c, r = self._num_cols - 1, self._num_rows - 1
        self._cells[c][r].has_bottom_wall = False
        self._draw_cell(c, r)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

    # Keep carving until this cell has no unvisited neighbors
        while True:
        # 1) Gather all unvisited neighbors
            nexts = []
            if i > 0 and not self._cells[i-1][j].visited:
                nexts.append((i-1, j, "left"))
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                nexts.append((i+1, j, "right"))
            if j > 0 and not self._cells[i][j-1].visited:
                nexts.append((i, j-1, "up"))
            if j < self._num_rows-1 and not self._cells[i][j+1].visited:
                nexts.append((i, j+1, "down"))

        # 2) If none left, draw and backtrack
            if not nexts:
                self._draw_cell(i, j)
                return

        # 3) Otherwise pick one at random
            ni, nj, direction = random.choice(nexts)
            neigh = self._cells[ni][nj]

        # 4) Knock down the walls
            if direction == "left":
                current.has_left_wall   = False
                neigh.has_right_wall    = False
            elif direction == "right":
                current.has_right_wall  = False
                neigh.has_left_wall     = False
            elif direction == "up":
                current.has_top_wall    = False
                neigh.has_bottom_wall   = False
            else:  # down
                current.has_bottom_wall = False
                neigh.has_top_wall      = False

        # 5) Redraw both cells so you see the wall go away
            self._draw_cell(i, j)
            self._draw_cell(ni, nj)

        # 6) Recurse into that neighbor, then -- **critically** -- 
        #    when that returns you loop around and carve *other* neighbors too
            self._break_walls_r(ni, nj)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True

        # base case: reached exit?
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # try each direction in fixed order
        # left, right, up, down
        for di, dj, direction in [(-1,0,"left"), (1,0,"right"), (0,-1,"up"), (0,1,"down")]:
            ni, nj = i + di, j + dj
            # bounds check
            if not (0 <= ni < self._num_cols and 0 <= nj < self._num_rows):
                continue

            neighbour = self._cells[ni][nj]
            # no wall and unvisited?
            if (
                direction == "left"  and not current.has_left_wall   and not neighbour.has_right_wall  and not neighbour.visited
                or direction == "right" and not current.has_right_wall  and not neighbour.has_left_wall   and not neighbour.visited
                or direction == "up"    and not current.has_top_wall    and not neighbour.has_bottom_wall and not neighbour.visited
                or direction == "down"  and not current.has_bottom_wall and not neighbour.has_top_wall    and not neighbour.visited
            ):
                # draw forward
                current.draw_move(neighbour)
                self._animate()
                if self._solve_r(ni, nj):
                    return True
                # undo/backtrack
                current.draw_move(neighbour, True)
                self._animate()

        return False

    def solve(self):
        return self._solve_r(0, 0)
