import itertools
import sys

sys.setrecursionlimit(10**6) 

example = [
	[0,8,0,0,3,0,0,0,2],
	[7,0,0,0,5,0,9,0,0],
	[0,0,9,7,6,2,0,0,8],
	[0,0,0,6,0,0,5,8,0],
	[0,5,0,0,0,0,0,4,0],
	[0,7,4,0,0,3,0,0,0],
	[3,0,0,1,4,6,7,0,0],
	[0,0,7,0,9,0,0,0,3],
	[1,0,0,0,7,0,0,9,0]]

# example = [
#     [0, 0, 0, 2, 6, 0, 7, 0, 1],
#     [6, 8, 0, 0, 7, 0, 0, 9, 0],
#     [1, 9, 0, 0, 0, 4, 5, 0, 0],
#     [8, 2, 0, 1, 0, 0, 0, 4, 0],
#     [0, 0, 4, 6, 0, 2, 9, 0, 0],
#     [0, 5, 0, 0, 0, 3, 0, 2, 8],
#     [0, 0, 9, 3, 0, 0, 0, 7, 4],
#     [0, 4, 0, 0, 5, 0, 0, 3, 6],
#     [7, 0, 3, 0, 1, 8, 0, 0, 0]
# ]

options = '123456789'

def print_sudoku(puzzle):
	'''Print out the sudoku, with the dividing lines'''
	for i in range(len(puzzle)):
		if i % 3 == 0 and i != 0:
			print('- ' * (len(puzzle)+2))
		for j in range(len(puzzle[i])):
			if j % 3 == 0 and j != 0:
				print('| ', end='')

			if j == 8:
				print(puzzle[i][j])
			else:
				print(str(puzzle[i][j]) + ' ', end ='')
	print()
	print()

def create_elimination_grid():
	rows = list(range(9))
	cols = list(range(9))
	pairing = list(itertools.product(rows, cols))
	elimination_dict = dict.fromkeys(pairing, options)
	return elimination_dict

def assign(elim_dict,elim_pos,number):
	elim_row, elim_col = elim_pos
	elim_dict[(elim_row,elim_col)] = str(number)

def eliminate(elim_dict,neighbors,number):
	for neighbor in neighbors:
		if len(elim_dict[neighbor]) == 1:
			continue
		if neighbor in elim_dict:
			elim_dict[neighbor] = elim_dict[neighbor].replace(number,'')
		else:
			continue

def find_all_neighbors(puzzle,checking_pos):
	'''Finds all surrounding neighbors, in the same row, column and square'''
	neighbors = list()
	checking_row, checking_column = checking_pos
	# Add row neighbors
	for i in range(len(puzzle[checking_row])):
		if (checking_row,i) in neighbors:
			continue
		elif i == checking_column:
			continue
		else:
			neighbors.append((checking_row,i))
	# Add column neighbors
	for i in range(len(puzzle)):
		if (i,checking_column) in neighbors:
			continue
		elif i == checking_row:
			continue
		else:
			neighbors.append((i,checking_column))
	# Add square neighbors
	box_row = checking_row // 3
	box_column = checking_column // 3
	for i in range(box_row * 3, box_row * 3 + 3):
		for j in range(box_column * 3, box_column * 3 + 3):
			if (i,j) in neighbors:
				continue
			elif (i,j) == checking_pos:
				continue
			else:
				neighbors.append((i,j))
	return neighbors

def find_next_empty_square(puzzle):
	'''Finds all available unsolved squares'''
	for row in range(len(puzzle)):
		for column in range(len(puzzle[row])):
			if puzzle[row][column] == 0:
				return (row,column)
	return None

def solve(puzzle, elim_dict):
	next_empty = find_next_empty_square(puzzle)
	if next_empty == None:
		return True
	else:
		row, col = next_empty
		possible_numbers_str = list(elim_dict[(row,col)])
	
	for num in possible_numbers_str:
		if check_valid(puzzle, num,(row,col)):
			puzzle[row][col] = num
			
			if solve(puzzle, elim_dict) == True:
				return True
			
			#if its invalid, reset.
			puzzle[row][col] = 0

	return False



def find_occupied_squares(puzzle):
	'''Finds all occupied solved squares'''
	all_occupied_cells_and_values = list()
	for row in range(len(puzzle)):
		for column in range(len(puzzle[row])):
			if puzzle[row][column] != 0:
				all_occupied_cells_and_values.append((row,column,puzzle[row][column]))
	return all_occupied_cells_and_values

def check_valid(puzzle, number, checking_pos):
	'''Check if the given number is valid in the given (row, column) checking position'''
	if check_valid_row(puzzle, number, checking_pos) \
		and check_valid_column(puzzle, number, checking_pos) \
		and check_square(puzzle, number, checking_pos):
		return True
	return False

def check_valid_row(puzzle, number, checking_pos):
	'''Checks to see if the given number is already in the checking row'''
	checking_row, checking_column = checking_pos
	for i in range(9):
		if puzzle[checking_row][i] == number and i != checking_column:
			return False
	return True

def check_valid_column(puzzle, number, checking_pos):
	'''Checks to see if the given number is already in the checking column'''
	checking_row, checking_column = checking_pos
	for i in range(9):
		if puzzle[i][checking_column] == number and i != checking_row:
			return False
	return True

def check_square(puzzle, number, checking_pos):
	'''Checks to see if the given number is already in the checking square'''
	checking_row, checking_column = checking_pos
	box_row = checking_row // 3
	box_column = checking_column // 3
	for i in range(box_row * 3, box_row * 3 + 3):
		for j in range(box_column * 3, box_column * 3 + 3):
			if puzzle[i][j] == number and (i,j) != checking_pos:
				return False
	return True

print('Unsolved Puzzle:')
print_sudoku(example)
# print(find_empty_squares(example))
# print()
# # print(find_occupied_squares(example))
example_grid = create_elimination_grid()
for row,col,number in find_occupied_squares(example):
	assign(example_grid,(row,col),number)
	eliminate(example_grid,find_all_neighbors(example,(row,col)),str(number))

solve(example,example_grid)
print('Solved Puzzle:')
print_sudoku(example)


