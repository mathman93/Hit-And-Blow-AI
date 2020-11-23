'''HB_AI_main.py
A simple AI for playing Hit & Blow (Mastermind).
Basic Idea: Create all possible solutions, and use attempts to
reduce possible solutions down to just one.
By: Timothy Anglea
'''

import itertools
import math

colors6 = "rcgypw" # 6 colors for the game (red, cyan, green, yellow, pink, white)
#colors7 = "rcgypwk" # Add the color "black"

# Create all possible solutions
#all_solutions = itertools.product(colors6, repeat=4) # All possible permutations of colors
all_solutions = itertools.permutations(colors6, 4) # All permutations with unique colors
# Create list object from all solutions
all_solutions_list = []
for sol in all_solutions:
	all_solutions_list.append(list(sol))
	#print(list(sol)) # Include for debugging
#print(len(all_solutions_list)) # Include for debugging

attmpt_num = 1 # Initialize attempt number for first guess
while True:
	try:
		attempt = input("Guess #{0}: ".format(attmpt_num)).lower()
		if len(attempt) != 4:
			print("Attempt must be 4 colors. Try again.")
			continue
		if list(attempt) not in all_solutions_list:
			print("Not a valid attempt. Try again.")
			continue
		break
	except ValueError:
		print("Not a valid attempt. Please try again.")
		continue

print(list(attempt))
