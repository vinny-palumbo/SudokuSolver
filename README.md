# **Solving Sudoku Puzzles with AI** 

Intelligent agent written in Python that can solve any 9x9 regular and diagonal sudoku puzzles using Constraint Propagation and Depth-First Search.

A diagonal sudoku is like a regular sudoku, except for these additional constraints: among the two main diagonals, the numbers 1 to 9 should all appear exactly once.

All the details about the steps I took to complete this project can be found in this [Jupyter Notebook](https://github.com/vinny-palumbo/SudokuSolver/blob/master/notebook.ipynb)

### Code to solve a sudoku

```sh
from sudokusolver import display,solve
"""
Write the sudoku as the concatenation of all the readings of the digits in the rows, taking the rows from top to bottom. Use a . as a placeholder for an empty box
"""
sudoku='2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
display(solve(sudoku)) # add is_diagonal=True to solve() for diagonal sudokus
```

### Visualize the solution with Pygame

You can also install pygame if you want to see your visualization. You can see how to download pygame [here](http://www.pygame.org/download.shtml).

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Environment

Here is my [environment file](https://github.com/vinny-palumbo/SudokuSolver/blob/master/environment.yaml). To clone my environment execute: 'conda env create -f environment.yaml'

