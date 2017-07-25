assignments = []

# create labels of the boxes
cols = '123456789'
rows = 'ABCDEFGHI'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
boxes = cross(rows, cols)

# create a dictionary containing a list of the 3, 4 or 5 units associated to each box
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
        ['A1','B2','C3','D4','E5','F6','G7','H8','I9'],
        ['I1','H2','G3','F4','E5','D6','C7','B8','A9']
    ]
unitlist = row_units + column_units + square_units
unitlist_diagonal = unitlist + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
units_diagonal = dict((s, [u for u in unitlist_diagonal if s in u]) for s in boxes)

# create a dictionary containing a list of the 20, 26 or 32 peers associated to each box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
peers_diagonal = dict((s, set(sum(units_diagonal[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for unit in unitlist:
        # Find boxes in the unit with two possible values
        boxes_with_two_possible_values = [box for box in unit if len(values[box])==2]
        for b in boxes_with_two_possible_values:
            # Find if each of those boxes have a twin
            b_twin = [box for box in boxes_with_two_possible_values if values[box] == values[b] and box != b]
            if b_twin:
                # Eliminate the naked twins as possibilities for their peers
                digits_twins = values[b]
                for digit in digits_twins:
                    for peer in unit:
                        if peer not in [b,b_twin[0]]:
                            values[peer] = values[peer].replace(digit,'')
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """    
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, is_diagonal=False):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    if is_diagonal:
        peers_f = peers_diagonal
    else:
        peers_f = peers

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers_f[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values, is_diagonal=False):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    if is_diagonal:
        unitlist_f = unitlist_diagonal
    else:
        unitlist_f = unitlist

    for unit in unitlist_f:
        for digit in '123456789':
            # dplaces is a list of boxes from the current unit with 'digit' as one of its possible values
            dplaces = [box for box in unit if digit in values[box]]
            # if only one box from the current unit with 'digit' as one of its possible values, assign it the value of 'digit'
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values, is_diagonal=False):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values, is_diagonal)
        # Use the Only Choice Strategy
        values = only_choice(values, is_diagonal)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values, is_diagonal=False):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, is_diagonal)
    if values is False:
        return False ## Failed earlier
    if all(len(values[box]) == 1 for box in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid, is_diagonal=False):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    if search(values, is_diagonal):
        return search(values, is_diagonal)
    else:
        return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid,is_diagonal=True))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
