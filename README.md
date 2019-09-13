# Sudoku-Solver

In this exercise, I attempt to tackle the problem of solving every sudoku puzzle. This is a personal project that serves as an opportunity to hone my problem-solving skills, refine my logical thinking frameworks and test my understanding of the Python language - all while having a little fun.

## About Sudoku
**Sudoku** is one of the most popular logic-based number-placement puzzle. The objective is to fill a square grid of size 'n' with digits 1 through 'n'. The digits must be placed such that each row, each column and each of the nine 3x3 subgrids contain only one instance of each digit.

The most common Sudoku puzzles uses a 9x9 grid, which is what is used in this exercise.

*For more information about Sudoku, check out its Wikipedia page [here](https://en.wikipedia.org/wiki/Sudoku).*

## Third-party libraries
- [Pandas](https://pandas.pydata.org/) (for reading the .csv file of quizzes)
- [NumPy](https://numpy.org/) (for its data structures)

## Dataset
- 1M games from a Kaggle dataset (``sudoku.csv``) that can be found [here](https://www.kaggle.com/bryanpark/sudoku#sudoku.csv)

## Approach

#### Notation
- Each puzzle is a 9x9 **_grid_** with 81 **_cells_**.
- Some cells are pre-populated with **_digits_**; these digits are referred to as **_givens_**.
- A **_row_** is well, a row.
- A **_column_** is a column.
- A **_subgrid_** is a 3x3 grid that lies within the 9x9 grid (there are 9 specific subgrids in  a 9x9 grid)
- Rows, columns and subgrids are referred to as **_units_**.

#### Preparing the grid
A Sudoku grid is often presented as an 81-digit string. In this format, the digit ``0`` denotes an empty cell. For the sake of clarity, each string is called a **_grid-string_**. For example:

``004300209005009001070060043006002087190007400050083000600000105003508690042910300``

The function ``parse_gridstring()`` is used to parse each grid-string into a single list (the grid) of 9 lists (each row), where each list contains 9 digits (either `0`s or givens).

```python
def parse_gridstring(gridstring):
    grid = []
    board.append(gridstring[i:i+9] for i in range(0, 81, 9))
    return board
```


## Acknowledgements
