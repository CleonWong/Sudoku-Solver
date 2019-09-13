# Sudoku-Solver

In this exercise, I attempt to tackle the problem of solving every sudoku puzzle. This is a personal project that serves as an opportunity to hone my problem-solving skills, refine my logical thinking frameworks and test my understanding of the Python language - all while having fun.

## About Sudoku
**Sudoku** is one of the most popular logic-based number-placement puzzle. The objective is to fill a square grid of size 'n' with digits 1 through 'n'. The digits must be placed such that each row, each column and each of the nine 3x3 subgrids contain only one instance of each digit.

The most common Sudoku puzzles uses a 9x9 grid, which is what is used in this exercise.

For more information about Sudoku, check out its Wikipedia page [here](https://en.wikipedia.org/wiki/Sudoku).

## Third-party libraries
- [Pandas](https://pandas.pydata.org/) (for reading the .csv file of quizzes)
- [NumPy](https://numpy.org/) (for its data structures)

## Dataset
- 1M games from a Kaggle dataset (``sudoku.csv``) that can be found [here](https://www.kaggle.com/bryanpark/sudoku#sudoku.csv)

## Approach

###### Notation
- Each puzzle is a 9x9 *grid* with 81 *cells*.
- Some cells are already populated with *digits*; these digits are referred to as *givens*.
- A *row* is well, a row. A *column* is a column. A *subgrid* is a 3x3 grid that lies within the 9x9 grid; rows, columns and subgrids are referred to as *units*.


## Acknowledgements
