'''HB_AI_main.py
A simple AI for playing Hit & Blow (Mastermind).
Basic Idea: Create all possible solutions, and use attempts to
reduce possible solutions down to just one.
To Do:
	- Have AI suggest next attempt
	- Validate hit/blow in manual mode
By: Timothy Anglea
'''

import itertools
import random
import os

def get_attempt(num, all_sol):
	while True:
		try:
			# Get user attempt
			attempt = input("Guess #{0}: ".format(num)).lower() # String of lowercase letters
			# Data validation
			if len(attempt) != 4: # If guess is not the right length...
				print("Attempt must be 4 colors. Try again.")
				continue
			# End if
			if attempt not in all_sol: # Only guess possible solutions
				print("Not a valid attempt. Try again.")
				continue
			# End if
			break
		except ValueError: # Probably won't see this.
			print("Not a valid attempt. Please try again.")
			continue
	# End while
	#print(attempt) # Include for debugging
	return attempt

def check_attempt(attempt, the_sol):
	# Check attempt - Determine hits and blows
	h = 0
	b = 0
	sol_copy = list(the_sol) # Copy for use in function
	hit_check = []
	for i in range(4): # Iterate over the attempt
		# First, find hits.
		if attempt[i] == sol_copy[i]: # If attempt and solution match...
			h += 1 # Attempt matches solution at position i
			sol_copy[i] = " " # Clear solution color; it's been accounted for
			hit_check.append(i)
			continue # Continue to next position
		# End if
	# End for
	# Then, find blows.
	for i1 in range(4): #Iterate over the attempt
		if i1 in hit_check:
			continue
		for i2 in range(4): #Iterate over the solution
			if attempt[i1] == sol_copy[i2]: # if the color is in the solution
				b += 1 # Attempt matches a color in the solution
				sol_copy[i2] = " " # Clear solution color; it's been accounted for
				break # End iteration over solution; continue to next attempt color
			# End if
		# End for
	# End for
	return [h, b]

def get_level():
	c6 = "cgprwy" # 6 colors for the game (cyan, green, pink, red, white, yellow)
	c7 = "cgprwyk" # Adds the color black
	c8 = "cgprwyko" # Adds the color orange
	nums = "0123456789" # Make it really abstract with numbers.
	while True:
		try:
			lvl = int(input("Choose a difficulty level (1-8): "))
			if lvl > 8 or lvl < 0:
				print("Not a valid difficulty level. Try again.")
				continue
			# End if
			if lvl == 0: # Reserved for computer playing itself.
				print("It's a secret to everyone.")
			# End if
			if lvl > 6: # (7 & 8)
				clrs = nums # Use decimal symbols
			elif lvl > 4: # (5 & 6)
				clrs = c8 # Use even more colors
			elif lvl > 2: # (3 & 4)
				clrs = c7 # Use more colors
			else: # (1 & 2)
				clrs = c6 # Use standard colors
			# End if
			break # Continue; game parameters are set
		except ValueError:
			print("Not a valid difficulty level. Please select a number.")
			continue
	# End while
	return [lvl, clrs]

def get_solutions(lvl, clrs):
	if lvl % 2 == 0: # (2, 4, 6, & 8)
		# Use all possible combinations of colors
		all_sols = itertools.product(clrs, repeat=4)
	else: # (1, 3, 5, & 7)
		# Use only permutations with unique colors
		all_sols = itertools.permutations(clrs, 4) 
	# End if
	# Create list object from all solutions
	sols_list = []
	for sol in all_sols:
		sols_list.append("".join(x for x in list(sol)))
		#print("".join(x for x in list(sol))) # Include for debugging
	#print(len(sols_list)) # Include for debugging
	return sols_list

def reset_possible(sols_list):
	return sols_list[:] # Copy list of available solutions

def set_mode():
	while True:
		try:
			print("Which mode would you like to use?")
			#print("Mode 0 -> CPU play against itself")
			print("Mode: 1 -> Play against CPU")
			print("Mode: 2 -> Mode 1 with CPU assist")
			print("Mode: 3 -> Manual play with CPU assist")
			g_mode = int(input("Mode: "))
			if g_mode < 0 or g_mode > 3:
				print("Not a valid game mode. Please select from the available modes.")
				continue
			# End if
			break
		except ValueError:
			print("Not a valid game mode. Please enter an number.")
			continue
	# End while
	return g_mode

print("Welcome to Hit & Blow (aka Mastermind).")
mode_select = True
affirm = ["yes","y"]
while True:
	## Select game mode
	while True:
		if mode_select == False:
			modeset = input("Do you want to play the same mode? ").lower()
			if modeset in affirm:
				break # Exit while loop
			# End if
		# End if
		game_mode = set_mode()
		mode_select = False
		level_select = True
		break
	# End while
	## Select game level
	while True:
		if level_select == False:
			levelset = input("Do you want to play the same level? ").lower()
			if levelset in affirm:
				break # Exit while loop
			# End if
		# End if
		[game_lvl, colors] = get_level()
		level_select = False
		break
	# End while
	# Game Instructions
	if game_lvl % 2 == 1:
		print("Available colors are {0}. Duplicates are not allowed.".format(colors))
	else:
		print("Available colors are {0}. Duplicates are allowed.".format(colors))
	# End if
	## Play the game
	all_solutions_list = get_solutions(game_lvl, colors)
	if game_mode in [1,2]: # If playing against CPU...
		# Pseudo Solution - Have the CPU pick a solution
		the_solution = all_solutions_list[random.randint(0,len(all_solutions_list)-1)]
		#print("The Solution: {0}".format(the_solution))
		
		# User Attempts
		attmpt_num = 1 # Initialize attempt number for first guess
		possible_solutions = reset_possible(all_solutions_list)
		while True:
			if attmpt_num > 8:
				print("Too many guesses. Sorry.")
				print("Actual solution: {0}".format("".join(the_solution)))
				break
			# End if
			attempt = get_attempt(attmpt_num, all_solutions_list)
			[hits,blows] = check_attempt(attempt, the_solution)
			print("Hits: {0}; Blows: {1}".format(hits,blows))
			if hits == 4: # Win Condition
				print("Congratulations! You win!")
				break
			# End if
			if game_mode == 2:
				# Find remaining valid solutions based on current attempt.
				sol_remove = [] # list of solutions to remove; they're invalid
				for possible in possible_solutions: # For each possible solution
					[hp,bp] = check_attempt(attempt, possible) # find hits,blows for the attempt if possible is the solution
					if hp == hits and bp == blows: # If the hits,blows match...
						continue # possible is still a valid solution
					# End if
					sol_remove.append(possible) # Otherwise, it will be removed
				# End for
				for x in sol_remove: # For each solution to remove
					possible_solutions.remove(x) # Remove it from the valid solutions
				# End for
			
				# Include for assistance
				print("Possible solutions left: {0}".format(len(possible_solutions)))
				if len(possible_solutions) < 21:
					print("; ".join(["".join([x for x in s]) for s in possible_solutions]))
				# End if
			# End if
			# Continue to next attempt
			attmpt_num += 1
		# End while
	elif game_mode in [3]:
		print("This mode is still in beta.")
		# User Attempts
		attmpt_num = 1 # Initialize attempt number for first guess
		possible_solutions = reset_possible(all_solutions_list)
		while True:
			if attmpt_num > 8:
				print("Too many guesses. Sorry.")
				#print("Actual solution: {0}".format("".join(the_solution)))
				break
			# End if
			attempt = get_attempt(attmpt_num, all_solutions_list)
			################
			# Ask for number of hits/blows; validate response
			hits = int(input("How many hits? "))
			blows = int(input("How many blows? "))
			#[hits,blows] = check_attempt(attempt, the_solution)
			#print("Hits: {0}; Blows: {1}".format(hits,blows))
			
			# Find remaining valid solutions based on current attempt.
			sol_remove = [] # list of solutions to remove; they're invalid
			for possible in possible_solutions: # For each possible solution
				[hp,bp] = check_attempt(attempt, possible) # find hits,blows for the attempt if possible is the solution
				if hp == hits and bp == blows: # If the hits,blows match...
					continue # possible is still a valid solution
				# End if
				sol_remove.append(possible) # Otherwise, it will be removed
			# End for
			for x in sol_remove: # For each solution to remove
				possible_solutions.remove(x) # Remove it from the valid solutions
			# End for
			###################
			if hits == 4: # Win Condition
				print("Congratulations! You win!")
				break
			# End if
			
			# Include for assistance
			print("Possible solutions left: {0}".format(len(possible_solutions)))
			if len(possible_solutions) < 21:
				print("; ".join(["".join([x for x in s]) for s in possible_solutions]))
			# End if
			# Continue to next attempt
			attmpt_num += 1
		# End while
	else: #game_mode in [0]
		print("This is a secret to everyone.")
	# End if
	repeat = input("Would you like to play again? ").lower()
	if repeat in ["yes","y"]:
		continue # Go back to beginning of while loop
	# End if
	break # if no repeat, break while loop
# End while

pause = input("Thanks for playing my game! (Press Enter to exit.)")
