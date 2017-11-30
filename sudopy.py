# Mon 24 Mar 2014 11:12:47 PM EDT


class Sudoku:
    """
    An exercise in building a python class.

    Sudoku
    ******

    Generate solutions of sudoku puzzles from string and list inputs.
    Totally unoptimized at this point!

    solve() : Attempt to find solution to sudoku puzzle using basic
    recursive backtracking algorithm. Return a new Sudoku instance of
    the solved puzzle.

    _from_string(puzzle_str) : Parse sudoku puzzle from string
    reading left to right into list of list. The first nine characters
    of the string correspond to the first row of the sudoku puzzle. Use
    numbers 1-9 to represent values in the puzzle and a '.' to indicate
    an empty grid point.

    """

    def __init__(self, puzzle=None):
        self.input_grid = ''

        # leave as empty if no input provided
        if isinstance(puzzle, str):
            self.from_string(puzzle)
        elif isinstance(puzzle, list):
            self.from_list(puzzle)
        else:
            self.puzzle = None

    def __str__(self):
        if isinstance(self.puzzle, type(None)):
            return repr(self)
        else:
            # output = '+-----+-----+-----+\n'
            output = '+' + ('-' * 7 + '+') * 3 + '\n'
            for i, row in enumerate(self.puzzle):
                output += '| {0} {1} {2} '.format(self._is_zero(row[0]),
                                                  self._is_zero(row[1]),
                                                  self._is_zero(row[2]))
                output += '| {0} {1} {2} '.format(self._is_zero(row[3]),
                                                  self._is_zero(row[4]),
                                                  self._is_zero(row[5]))
                output += '| {0} {1} {2} |'.format(self._is_zero(row[6]),
                                                   self._is_zero(row[7]),
                                                   self._is_zero(row[8]))
                output += '\n'

                if (i + 1) % 3 == 0:
                    output += '+' + ('-' * 7 + '+') * 3 + '\n'

        return output

    # initial declarations and problem parameters
    _NROWS = 9
    _NCOLS = 9

    def _is_zero(self, value):
        if value:
            return value
        else:
            return '.'

    def _from_list(self, puzzle_lst):
        # ensure proper conversion if input is list or list of lists
        if all(isinstance(sublist, list) for sublist in puzzle_lst):
            return puzzle_lst
        # build list of list if input is flat
        elif all(isinstance(val, int) for val in puzzle_lst):
            return [puzzle_lst[i * 9: i * 9 + 9] for i in range(self._NROWS)]
        else:
            raise ValueError('incorrect input puzzle')

    def _from_string(self, puzzle_str):
        # converts string to list since read_from_list is workhorse
        p = []
        for i in range(self._NROWS):
            row = puzzle_str[i * 9: i * 9 + 9]
            p.append([int(val) if val != '.' else 0 for val in row])

        return p

    def _copy(self):
        """ make deep copy of puzzle """
        return [[val for val in lst] for lst in self.puzzle]

    def _col(self, col):
        """ return column from sudoku puzzle """
        return [row[col] for row in self.puzzle]

    def _along_row(self, pos_val):
        """ check if move valid in row """
        if pos_val[2] in (self.puzzle[pos_val[0]][:pos_val[1]] +
                          self.puzzle[pos_val[0]][pos_val[1] + 1:]):
            return False
        else:
            return True

    def _along_col(self, pos_val):
        """ check if move valid in column """
        col = self._col(pos_val[1])
        if pos_val[2] in (col[:pos_val[0]] + col[pos_val[0] + 1:]):
            return False
        else:
            return True

    def _in_box(self, pos_val):
        """ check if move valid in sub box """
        block_row = pos_val[0] // 3 * 3
        block_col = pos_val[1] // 3 * 3

        block = [self.puzzle[r][c] for r in range(block_row, block_row + 3)
                 for c in range(block_col, block_col + 3)
                 if r != pos_val[0] or c != pos_val[1]]

        if pos_val[2] in block:
            return False
        else:
            return True

    def _check_move(self, pos_val):
        return (self._along_row(pos_val) and self._along_col(pos_val) and self._in_box(pos_val))

    # def _set_initial_state(self):
    #     init_state = set()
    #     for r in range(self._NROWS):
    #         for c in range(self._NCOLS):
    #             if self.puzzle[r][c]:
    #                 init_state.add((r, c))
    #     return init_state

    def _candidates(self, r, c):
        candidates = []
        for i in range(1, 10):
            if self._check_move((r, c, i)):
                candidates.append(i)
        return candidates

    def _unassigned(self, grid):
        for r in range(self._NROWS):
            for c in range(self._NCOLS):
                if not grid[r][c]:
                    return (r, c)
        return (-1, -1)

    def _unassigned_with_least_candidates(self, grid):
        min = (10, 10, 10)  # impossible values... think of more pythonic way
        for r in range(self._NROWS):
            for c in range(self._NCOLS):
                if not grid[r][c]:
                    n = len(self._candidates(r, c))

                    if n == 1:
                        return (r, c)

                    if n < min[2]:
                        min = (r, c, n)

        if min != (10, 10, 10):
            return min[:2]
        else:
            return (-1, -1)

    def _next(self, grid, r, c):
        for i in range(1, 10):
            if self._check_move((r, c, i)):
                grid[r][c] = i
                if self._solve(grid):
                    return True
                grid[r][c] = 0

        return False

    def _solve(self, grid):
        """ use backtracking to solve sudoku """
        r, c = self._unassigned_with_least_candidates(grid)
        if r == -1 and c == -1:
            return True

        return self._next(grid, r, c)

    def from_list(self, puzzle_lst):
        self.puzzle = self._from_list(puzzle_lst)

    def from_string(self, puzzle_str):
        self.puzzle = self._from_string(puzzle_str)
        self.input_grid = puzzle_str

    def show(self):
        print(self)

    def is_valid(self, grid):
        # check sudoku validity
        for r in range(self._NROWS):
            for c in range(self._NCOLS):
                if grid[r][c]:
                    if not self._check_move((r, c, grid[r][c])):
                        return False
        return True

    def solve(self):
        # make a copy
        original = self._copy()

        if self._solve(self.puzzle):
            solution = Sudoku(self.puzzle)
            self.puzzle = original
            return solution
        else:
            print('no solution')
