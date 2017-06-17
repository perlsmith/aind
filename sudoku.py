import sys
import re
import pdb
from utils import display

rows = 'ABCDEFGHI'
cols = '123456789'

def cross( a, b) :
	return [s+t for s in a for t in b]

boxes = cross( rows, cols )
row_units = [ cross( r, cols) for r in rows ]
col_units = [ cross( rows, c) for c in cols ]	

def grid_values(  p_str ) :
	g_v = dict( zip( boxes, p_str ) )
	for k, v in g_v.items() :
		if v == '.' :
			g_v[k] = '123456789'
	return g_v	# where p_str is the puzzle in string form..
	
square_units = [ cross( r, c ) for r in ( 'ABC', 'DEF', 'GHI') for c in ('123', '456', '789' ) ]

unitlist = row_units + col_units + square_units

puzzle = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def eliminate( grid ) :

	"""Eliminate values from peers of each box with a single value.

	Go through all the boxes, and whenever there is a box with a single value,
	eliminate this value from the set of values of all its peers.

	Args:
	values: Sudoku in dictionary form.
	Returns:
	Resulting Sudoku in dictionary form after eliminating values.
	"""

	for box in boxes :
		if 1 == len( grid[box] ) :	# then, need to hit the peers - all 20 of them...
			# print( box )
			for unit in unitlist :
				if box in unit :
					# pdb.set_trace()
					for cell in unit :
						if not cell == box :
							grid[cell] = re.sub( grid[box] , '' , grid[cell] )
	return grid

def only_choice(grid):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in grid[box]]
            if len(dplaces) == 1:
                grid[dplaces[0]] = digit
    return grid

def reduce_puzzle(grid):
	stalled = False
	while not stalled:
		# Check how many boxes have a determined value
		total_choices_before = len( ''.join( grid.values() ) )

		grid = eliminate( grid )
		grid = only_choice( grid )

		# Your code here: Use the Only Choice Strategy

		# Check how many boxes have a determined value, to compare
		total_choices_after = len( ''.join( grid.values() ) )
		# If no new values were added, stop the loop.
		stalled = total_choices_before == total_choices_after
		# Sanity check, return False if there is a box with zero available values:
		if len([box for box in grid.keys() if len(grid[box]) == 0]):
			return False
	return grid


sudoku = grid_values( puzzle )
su = eliminate( sudoku )
su = only_choice( su )
	
display( reduce_puzzle( su ) )
	
pdb.set_trace()
