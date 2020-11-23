'''HB_AI_main.py
A simple AI for playing Hit & Blow (Mastermind).
Basic Idea: Create all possible solutions, and use attempts to
reduce possible solutions down to just one.
To Do:
	- Improve Hit/Blow counter for duplicate solutions
	- Create game options at start
	- Create player option to play again
	- Generate possible solutions after each attempt
	- Have AI pick randomly from possible solutions
By: Timothy Anglea
'''

import itertools
import random

def get_attempt(num, all_sol):
	while True:
		try:
			# Get user attempt
			attempt = list(input("Guess #{0}: ".format(num)).lower())
			# Data validation
			if len(attempt) != 4: # If guess is not the right length...
				print("Attempt must be 4 colors. Try again.")
				continue
			if attempt not in all_sol:
				print("Not a valid attempt. Try again.")
				continue
			break
		except ValueError:
			print("Not a valid attempt. Please try again.")
			continue
	
	print(attempt) # Include for debugging
	return attempt

def check_attempt(attempt, the_sol):
	# Check attempt - Determine hits and blows
	h = 0
	b = 0
	# Works for unique color combos; won't work for duplicate color combos
	for i in range(4):
		if attempt[i] in the_sol:
			if attempt[i] == the_sol[i]:
				h += 1 # Attempt matches solutions at position i
			else:
				b += 1
	return [h, b]

colors6 = "cgprwy" # 6 colors for the game (cyan, green, pink, red, white, yellow)
#colors7 = "cgprwyk" # Adds the color black

# Game Setup - Create all possible solutions
#all_solutions = itertools.product(colors6, repeat=4) # All possible permutations of colors
all_solutions = itertools.permutations(colors6, 4) # All permutations with unique colors
# Create list object from all solutions
all_solutions_list = []
for sol in all_solutions:
	all_solutions_list.append(list(sol))
	#print(list(sol)) # Include for debugging
#print(len(all_solutions_list)) # Include for debugging

# Pseudo Solution - Have the program pick a solution
the_solution = all_solutions_list[random.randint(0,len(all_solutions_list)-1)]
#print(the_solution)

# Game Instructions
print("Welcome to Hit & Blow.")
print("Available colors are {0}.".format(colors6))

# User Attempts
attmpt_num = 1 # Initialize attempt number for first guess
while True:
	if attmpt_num > 8:
		print("Too many guesses. Sorry.")
		sol_str = ""
		print("Actual solution: {0}".format(sol_str.join(the_solution)))
		break
	attempt = get_attempt(attmpt_num, all_solutions_list)
	[hits,blows] = check_attempt(attempt, the_solution)
	print("Hits: {0}; Blows: {1}".format(hits,blows))
	if hits == 4: # Win Condition
		print("Congratulations! You win!")
		break
	attmpt_num += 1

pause = input("Thanks for playing my game!")

