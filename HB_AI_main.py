'''HB_AI_main.py
A simple AI for playing Hit & Blow (Mastermind).
Basic Idea: Create all possible solutions, and use attempts to
reduce possible solutions down to just one.
To Do:
	- Reprogram in Julia
By: Timothy Anglea
'''

import itertools
import random

def get_attempt(num, all_sol, gsize):
	while True:
		try:
			# Get user attempt
			attempt = input("Guess #{0}: ".format(num)).lower() # String of lowercase letters
			# Data validation
			if len(attempt) != gsize: # If guess is not the right length...
				print("Attempt must be {0} colors. Try again.".format(gsize))
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

def check_attempt(attempt, the_sol, gsize):
	# Check attempt - Determine hits and blows
	h = 0
	b = 0
	hit_check = [] # indices for the_sol that have been accounted for.
	for i1 in range(gsize): # for each color in attempt
		for i2 in range(gsize): # for each color in the_sol
			if i2 in hit_check: # If that color in the_sol is already checked
				continue # Go to next color in the_sol
			# End if
			if attempt[i1] == the_sol[i2]: # If the colors match...
				if i1 == i2: # If its in the same position
					h += 1 # It's a hit.
				else: # Otherwise
					b += 1 # It's a blow.
				# End if
				hit_check.append(i2) # the_sol[i2] has now been accounted for.
				break # Move to next color in attempt
			# End if
		# End for i2
	# End for i1
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

def get_solutions(lvl, clrs, gsize):
	if lvl % 2 == 0: # (2, 4, 6, & 8)
		# Use all possible combinations of colors
		all_sols = itertools.product(clrs, repeat=gsize)
	else: # (1, 3, 5, & 7)
		# Use only permutations with unique colors
		all_sols = itertools.permutations(clrs, gsize) 
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

def find_possible(all_poss,attempt,h,b,gsize):
	# Find remaining valid solutions based on current attempt.
	#sol_remove = [] # list of solutions to remove; they're invalid
	valid = [] # List of solutions that are still valid
	for possible in all_poss: # For each possible solution
		[hp,bp] = check_attempt(attempt, possible, gsize) # find hits,blows for the attempt if possible is the solution
		if hp == h and bp == b: # If the hits,blows match...
			valid.append(possible) # possible is still a valid solution
			#continue # possible is still a valid solution
		# End if
		#sol_remove.append(possible) # Otherwise, it will be removed
	# End for
	#for x in sol_remove: # For each solution to remove
	#	possible_solutions.remove(x) # Remove it from the valid solutions
	# End for
	return valid

def get_nexttry(possible_solutions,gsize):
	num_poss = len(possible_solutions)
	print("Thinking...")
	poss_select = random.sample(possible_solutions,k=num_poss) if num_poss<21 else random.sample(possible_solutions,k=20)
	vlen_array = []
	maybe_sol_list = possible_solutions[:] if num_poss<101 else random.sample(possible_solutions,k=100)
	for i1 in range(len(poss_select)):
		poss_attmpt = poss_select[i1]
		vlen_array.append(0)
		# if poss_attmpt is next attempt, find remaining valid solutions
		for maybe_sol in maybe_sol_list: # Assume a solution from remaining possible solutions
			[h_poss,b_poss] = check_attempt(poss_attmpt,maybe_sol,gsize) # find hits/blows
			valid_sols = find_possible(maybe_sol_list,poss_attmpt,h_poss,b_poss,gsize)
			# Save len(valid_sols); repeat for each possible solution
			vlen_array[i1] += len(valid_sols)
		# End for
		#print("{0}: {1}".format(poss_attmpt, vlen_array[i1])) # Include for debugging
	# End for
	return poss_select[vlen_array.index(min(vlen_array))]

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
	guess_size = 4
	## Play the game
	all_solutions_list = get_solutions(game_lvl, colors, guess_size)
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
			attempt = get_attempt(attmpt_num, all_solutions_list, guess_size)
			[hits,blows] = check_attempt(attempt, the_solution, guess_size)
			print("Hits: {0}; Blows: {1}".format(hits,blows))
			if hits == guess_size: # Win Condition
				print("Congratulations! You win!")
				break
			# End if
			if game_mode == 2: # Provide assistance on remaining valid solutions
				possible_solutions = find_possible(possible_solutions,attempt,hits,blows,guess_size)
				#num_poss = len(possible_solutions)
				# Include for assistance
				print("Possible solutions left: {0}".format(len(possible_solutions)))
				next_try = get_nexttry(possible_solutions,guess_size)
				print("Try {0}.".format(next_try))
				#if num_poss < 11: # Include for debugging
				#	print("; ".join(["".join([x for x in s]) for s in possible_solutions]))
				# End if
			# End if
			# Continue to next attempt
			attmpt_num += 1
		# End while
	elif game_mode in [3]:
		# User Attempts
		attmpt_num = 1 # Initialize attempt number for first guess
		possible_solutions = reset_possible(all_solutions_list)
		while True:
			if attmpt_num > 8:
				print("Too many guesses. Sorry.")
				break
			# End if
			attempt = get_attempt(attmpt_num, all_solutions_list, guess_size)
			# Ask for number of hits/blows; validate response
			while True:
				try:
					hits = int(input("How many hits? "))
					blows = int(input("How many blows? "))
					if hits < 0 or hits > guess_size or blows < 0 or blows > guess_size or (hits+blows) > guess_size:
						print("Not a valid number of hits & blows. Please try again.")
						continue
					# End if
					valid_solutions = find_possible(possible_solutions,attempt,hits,blows,guess_size)
					if len(valid_solutions) == 0:
						print("Something went wrong. No valid solutions exist. \nEnter the number of hits & blows again.")
						continue
					possible_solutions = valid_solutions
					break
				except ValueError:
					print("Not a valid number entry. Try again.")
					continue
			# End while
			if hits == guess_size: # Win Condition
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
			attempt = next_try if attmpt_num > 1 else random.choice(possible_solutions)
			print("Guess #{0}: {1}".format(attmpt_num, attempt))
			[hits,blows] = check_attempt(attempt, the_solution, guess_size)
			print("Hits: {0}; Blows: {1}".format(hits,blows))
			if hits == guess_size: # Win Condition
				print("Congratulations! You win!")
				break
			# End if
			possible_solutions = find_possible(possible_solutions,attempt,hits,blows,guess_size)
			# Include for assistance
			print("Possible solutions left: {0}".format(len(possible_solutions)))
			next_try = get_nexttry(possible_solutions,guess_size)
			# Continue to next attempt
			attmpt_num += 1
		# End while
	# End if
	repeat = input("Would you like to play again? ").lower()
	if repeat in ["yes","y"]:
		continue # Go back to beginning of while loop
	# End if
	break # if no repeat, break while loop
# End while

pause = input("Thanks for playing my game! (Press Enter to exit.)")
