# **Solving Sudoku Puzzles with AI** 

Intelligent agent written in Python that can solve any 9x9 regular and diagonal sudoku puzzles using Constraint Propagation and Depth-First Search.

A diagonal sudoku is like a regular sudoku, except for these additional constraints: among the two main diagonals, the numbers 1 to 9 should all appear exactly once.

All the details about the steps I took to complete this project can be found in this [Jupyter Notebook](https://github.com/vinny-palumbo/SudokuSolver/blob/master/notebook.ipynb)

### Code to solve a sudoku and visualize its solution

```sh
from sudokusolver import display,solve

"""
Write the sudoku as the concatenation of all the readings of the digits in the rows, 
taking the rows from top to bottom. Use a . as a placeholder for an empty box
"""
sudoku = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

"""
The display() function will print the sudoku solution in the console. If Pygame is installed,
a window will open, visualizing each step the AI agent took to solve the sudoku puzzle.
"""
display(solve(sudoku)) # add is_diagonal=True as a second argument to solve() for diagonal sudokus
```

![alt text][image1]

### Visualize the solution with Pygame

If you want to visualize the sudoku solution steps, install Pygame [here](http://www.pygame.org/download.shtml).

### Environment

Here is my [environment file](https://github.com/vinny-palumbo/SudokuSolver/blob/master/environment.yaml), which includes Pygame. To clone my environment execute: `conda env create -f environment.yaml`


[//]: # (Image References)
[image1]: ./images/pygame-steps.gif "Pygame Steps"