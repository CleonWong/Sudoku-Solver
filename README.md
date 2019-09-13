# Sudoku Solver

In this exercise, I attempt to tackle the problem of solving every sudoku puzzle. This is a personal project that serves as an opportunity to hone my problem-solving skills, refine my logical thinking frameworks and test my understanding of the Python language - all while having a little fun.

## About Sudoku
**Sudoku** is one of the most popular logic-based number-placement puzzle. The objective is to fill a square grid of size 'n' with digits 1 through 'n'. The digits must be placed such that each row, each column and each of the nine 3x3 subgrids contain only one instance of each digit.

The most common Sudoku puzzles uses a 9x9 grid, which is what is used in this exercise.

*For more information about Sudoku, check out its Wikipedia page [here](https://en.wikipedia.org/wiki/Sudoku).*

## Third-party libraries
- [Pandas](https://pandas.pydata.org/) (for reading the .csv file of quizzes)

## Dataset
- 1M games from a Kaggle dataset (``sudoku.csv``) that can be found [here](https://www.kaggle.com/bryanpark/sudoku#sudoku.csv)

## Approach

### Notation
- Each puzzle is a 9x9 **_grid_** with 81 **_cells_**.
- Some cells are pre-populated with **_digits_**; these digits are referred to as **_givens_**.
- A **_row_** is well, a row.
- A **_column_** is a column.
- A **_subgrid_** is a 3x3 grid that lies within the 9x9 grid (there are 9 specific subgrids in  a 9x9 grid)
- Rows, columns and subgrids are referred to as **_units_**.


### Importing frameworks
```python
import pandas as pd
import time
```


### Preparing the grids to solve
A Sudoku grid is often presented as an 81-digit string. In this format, the digit ``0`` denotes an empty cell. For the sake of clarity, every string representing a grid is called a **_grid-string_**. For example:

```python
gridstring = '004300209005009001070060043006002087190007400050083000600000105003508690042910300'
```

The function ``parse_gridstring()`` is used to parse each grid-string into a single list (representing the whole grid) of 9 lists (each representing one row), where each list contains 9 digits (either `0`s or givens).

```python
def parse_gridstring(gridstring):
    gridtemp = [int(i) for i in gridstring]
    grid = [gridtemp[i:i+9] for i in range(0, 81, 9)]
    return grid
```

Calling the ``parse_gridstring`` function on the example above, this should return:

```python
>>> [[0, 0, 4, 3, 0, 0, 2, 0, 9],
      [0, 0, 5, 0, 0, 9, 0, 0, 1],
      [0, 7, 0, 0, 6, 0, 0, 4, 3],
      [0, 0, 6, 0, 0, 2, 0, 8, 7],
      [1, 9, 0, 0, 0, 7, 4, 0, 0],
      [0, 5, 0, 0, 8, 3, 0, 0, 0],
      [6, 0, 0, 0, 0, 0, 1, 0, 5],
      [0, 0, 3, 5, 0, 8, 6, 9, 0],
      [0, 4, 2, 9, 1, 0, 3, 0, 0]]
```

We then use Pandas to read and iterate through each line of the ``sudoku.csv`` dataset to return a list (``grid_all``) of all grids that we are going to solve. As an example, I will only use the first 10,000 grids. (Note that the data set contains both the unsolved grids and their solutions. We will only be using the unsolved grids and not the solutions.)

```python
df_grids = pd.read_csv('sudoku.csv', nrows = 10000)

for row in df_grids.itertuples():
    gridstring = row.quizzes
    grid = parse_gridstring(gridstring)
    grid_all.append(grid)
```

### Step 1: Finding the possible digits for every empty cell

For each empty cell, we use set theory together with Python's ability to process sets to check through all its units before arriving at its set of possible digits. Note that every cell belongs to exactly 3 units (its row, column and subgrid).

First, we define a set of digits 1 to 9 as the ``full_set``. This is the set that we will be comparing to when checking across units.
```python
full_set = {1,2,3,4,5,6,7,8,9}
```

The 4 functions below will help us check through the 3 units of an empty cell ``grid[i][j]`` (where ``i`` denotes its row and ``j`` denotes its column) and then return a set of possible digits for that empty cell.

```python
def check_unit_row(i, j):
    possible_row = full_set - set(grid[i])
    return possible_row

def check_unit_col(i, j):
    possible_col = full_set - set([grid[x][j] for x in range(9)])
    return possible_col

def check_unit_subgrid(i, j):
    first = [0,1,2]
    second = [3,4,5]
    third = [6,7,8]
    find_subgrid = [first, second, third]

    row = [x in find_subgrid if i in x]
    for x in find_box:
        if i in x:
            row = x
        if j in x:
            col = x

    possible_subgrid = full_set - set(grid[i][j] for i in row for j in col])
    return possible_subgrid

def get_poss_digits(i, j):
    possible_digits = check_unit_row(i, j) & check_unit_col(i, j) & check_unit_subgrid(i, j)
    return possible_digits
```
What happens here is that calling each of the 3 functions ``check_unit_row``, ``check_unit_col`` and ``check_unit_subgrid`` on an empty cell returns a set of possible digits when looking through its row, column or subgrid respectively. The function ``get_poss_digits`` then finds the intersection of the 3 sets (``possible_row``, ``possible_col`` and ``possible_subgrid``) and returns a final set (``possible_digits``) that contains the possible digits for that empty cell.

Using the top left cell ``grid[0][0]`` from the example grid above, we see that the only possible digit for that cell is 8:

```python
check_unit_row(0,0)
  >>> {1, 5, 6, 7, 8}
check_unit_col(0,0)
  >>> {2, 3, 4, 5, 7, 8, 9}
check_unit_subgrid(0,0)
  >>> {1, 2, 3, 6, 8, 9}

get_poss_digits(0,0)
  >>> {8}
```


### Step 2: Lone single and constraint propagation

A **_Lone Single_** happens when an empty cell has only one possible digit. When a Lone Single happens, all we have to do is to fill that cell with its single possible value. However, most of the time, it doesn't stop there. In most cases, filling a cell will eliminate the possible digits for other empty cells, making it possible to fill a second cell. This then shrinks the set of possible digits for the rest of the empty cells, and so on. This process is called **_constraint propagation_**.

This is how it looks like in code:

```python
def lone_single(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                possible_digits = get_poss_digits(i, j)
                if len(possible_digits) == 1:
                    grid[i][j] = list(possible_digits)[0]
                    lone_single(grid)
    return grid
```





## Acknowledgements
