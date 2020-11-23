'''HB_AI_main.py
A simple AI for playing Hit & Blow (Mastermind).
Basic Idea: Create all possible solutions, and use attempts to
reduce possible solutions down to just one.
To Do:
	- Create game options at start
	- Create player option to play again
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
	
	#print(attempt) # Include for debugging
	return attempt

def check_attempt(attempt, the_sol):
	# Check attempt - Determine hits and blows
	h = 0
	b = 0
	sol_copy = the_sol[:] # Copy for use in function
	hit_check = [] # list of indices of colors marked as a hit
	# First, find hits
	for i in range(4):
		if attempt[i] == sol_copy[i]:
			h += 1 # Attempt matches solution at position i
			sol_copy[i] = " " # Clear solution color; it's been accounted for
			hit_check.append(i) # add color at index i to checked list
	# Then, find blows
	for i1 in range(4): #iterate over attempt
		if i1 in hit_check:
			continue # Already counted that one as a hit
		for i2 in range(4): #iterate over solution
			if attempt[i1] == sol_copy[i2]: # if the color is in the solution
				b += 1
				sol_copy[i2] = " " # Clear solution color; it's been accounted for
				break # end iteration over solution; continue to next attempt color
	return [h, b]

# Game Setup - Create all possible solutions
colors6 = "cgprwy" # 6 colors for the game (cyan, green, pink, red, white, yellow)
colors7 = "cgprwyk" # Adds the color black
colors8 = "cgprwykm" # Adds the color magenta
while True:
	try:
		lvl = int(input("Choose a difficulty level (1-6): "))
		if lvl > 6 or lvl < 0:
			print("Not a valid difficulty level. Try again.")
			continue
		# End if
		if lvl == 0: # Reserved for computer playing itself.
			print("It's a secret to everyone.")
		# End if
		if lvl > 4: # (5 & 6)
			colors = colors8 # Use even more colors
		elif lvl > 2: # (3 & 4)
			colors = colors7 # Use more colors
		else: # (1 & 2)
			colors = colors6 # Use standard colors
		# End if
		if lvl % 2 == 0: # (2 & 4)
			# Use all possible combinations of colors
			all_solutions = itertools.product(colors, repeat=4)
		else: # (1 & 3)
			# Use only permutations with unique colors
			all_solutions = itertools.permutations(colors, 4) 
		# End if
		break # Continue; game parameters are set
	except ValueError:
		print("Not a valid difficulty level. Please select a number.")
		continue

# Create list object from all solutions
all_solutions_list = []
for sol in all_solutions:
	all_solutions_list.append(list(sol))
	#print(list(sol)) # Include for debugging
#print(len(all_solutions_list)) # Include for debugging
possible_solutions = all_solutions_list[:] # Copy available solutions

# Pseudo Solution - Have the program pick a solution
the_solution = all_solutions_list[random.randint(0,len(all_solutions_list)-1)]
#print("The Solution: {0}".format(the_solution))

# Game Instructions
print("Welcome to Hit & Blow.")
print("Available colors are {0}.".format(colors))

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
	# Find remaining valid solutions based on current attempt.
	sol_remove = [] # list of solutions to remove; they're invalid
	for possible in possible_solutions: # For each possible solution
		[hp,bp] = check_attempt(attempt, possible) # find hits,blows for the attempt if possible is the solution
		if hp == hits and bp == blows: # If the hits,blows match...
			continue # possible is still a valid solution
		sol_remove.append(possible) # Otherwise, it will be removed
	for x in sol_remove: # For each solution to remove
		possible_solutions.remove(x) # Remove it from the valid solutions
	
	# Include for assistance
	#print("Possible solutions left: {0}".format(len(possible_solutions)))
	#if len(possible_solutions) < 11:
	#	print(possible_solutions)
	
	# Continue to next attempt
	attmpt_num += 1

pause = input("Thanks for playing my game! (Press Enter to exit.)")
