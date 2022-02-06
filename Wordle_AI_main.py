'''Wordle_AI_main.py
A simple AI for playing and assisting in Wordle.
Basic Idea: From all possible solutions, choose word that
reduces possible solutions the most until one remains.
May eventually implement in Julia
By: Timothy Anglea
'''

import itertools
import random

wordlistA = open("wordle-answers-alphabetical.txt","r").read().split()
wordlistB = open("wordle-allowed-guesses.txt","r").read().split()
wordlist = wordlistA + wordlistB # Combined word list
wordlist.sort() # Sort wordlist for reasons

# Get wordguess input from user
# Check if wordguess is in wordlist
# Compare wordguess to solution
# Give proper clue for wordguess based on solution
# Check which other words in wordlist give the same clue

# Develop algorithm to find best wordguess given remaining possible words

pause = input("Thanks for playing my game! (Press Enter to exit.)")
