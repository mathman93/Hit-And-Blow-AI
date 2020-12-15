#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
Still need to implement "get_nexttry" and Modes 0 & 3.
=#
using Combinatorics

function get_attempt(num, all_sol, atmp_size)
    local attmpt
    while true
        try
            print("Guess #", num, ": ")
            attmpt = lowercase(readline())
            if length(attmpt) != atmp_size
                println("Attempt must be ", atmp_size, " colors. Try again.")
                continue
            end
            if attmpt in all_sol
                break
            else
                println("Not a valid attempt. Try again.")
                continue
            end
        catch str_error
            println("We've had an error. Try again.")
            continue
        end # try
    end # while
    return attmpt
end

function check_attempt(attmpt, the_sol, atmp_size)
    local h = 0; local b = 0;
    #local atmpt_check = {Int}[];
    local sol_check = Int[];
    #=for i in 1:atmp_size
        if attempt[i] == sol_copy[i]
            h += 1
            # Clear solution color
            push!(atmpt_check, i)
            push!(sol_check, i)
        end
    end=#
    # check each character in attempt against each character in the_sol
    for i1 in 1:atmp_size # attempt[i1]
        #if i1 in atmpt_check # If already checked
        #    continue # already checked it.
        #end # if
        for i2 in 1:atmp_size # the_sol[i2]
            if i2 in sol_check
                continue
            end # if
            if attmpt[i1] == the_sol[i2] # If there's a match
                if i1 == i2 # If it's in the same position
                    h += 1 # it's a hit
                else # If it's not in the same position
                    b += 1 # it's a blow
                end
                #push!(atmpt_check, i1)
                push!(sol_check, i2) # Don't need to check that position in the solution again.
                break # Go to next attempt position
            end # if
        end # for i2
    end # for i1
    return h, b
end

function get_level()
    local lvl; local clrs;
    local c6 = "cgprwy"; local c7 = c6*"k"; local c8 = c7*"o"; local c10 = "0123456789"
    while true
        try
            print("Choose a difficulty level (1-8): ")
            lvl = parse(Int, readline())
            if lvl > 8 || lvl < 1
                println("Not a valid difficulty level. Try again.")
                continue
            end
            if lvl > 6 # (7 & 8)
                clrs = c10 # Numbers
            elseif lvl > 4 # (5 & 6)
                clrs = c8 # 8 colors
            elseif lvl > 2 # (3 & 4)
                clrs = c7 # 7 colors
            else # (1 & 2)
                clrs = c6 # 6 colors
            end
            break
        catch num_error
            println("Not a valid difficulty level. Please select a number.")
            continue
        end # try
    end # while
    return lvl, clrs
end # function

function get_solutions(lvl, clrs, atmp_size)
    if lvl % 2 == 0
        all_sols = Iterators.product(fill(clrs, atmp_size)...);
    else
        all_sols = permutations(clrs, atmp_size)    
    end
    all_solsarray = String[]
    #println(typeof(all_solsarray))
    for pair in all_sols
        pair_str = ""
        for c in pair
            pair_str *= c # Concatenate
        end
        append!(all_solsarray, [pair_str])
    end
    return all_solsarray
end

function set_mode()
    local g_mode
    while true
        try
            println("Which mode would you like to use?")
			#println("Mode 0 -> CPU play against itself")
			println("Mode: 1 -> Play against CPU")
			println("Mode: 2 -> Mode 1 with CPU assist")
            println("Mode: 3 -> Manual play with CPU assist")
            print("Mode: ")
            g_mode = parse(Int, readline())
            if g_mode > 3 || g_mode < 0
                println("Not a valid game mode. Please select from the available modes.")
                continue
            end
            break
        catch num_error
            println("Not a valid game mode. Please enter an integer.")
            continue
        end # try
    end # while
    return g_mode
end

function find_possible(all_poss, attmpt, h, b, atmp_size)
    local valid = String[] # Empty
    for possible in all_poss # assume possible is the solution
        hp, bp = check_attempt(attmpt, possible, atmp_size)
        if hp == h && bp == b # If the hits/blows match...
            push!(valid, possible) # possible is still valid
        end
    end
    return valid
end

function get_nexttry(all_poss, atmp_size)
    num_poss = length(all_poss)
    println("Thinking... ")
    #poss_select = 
end

println("Welcome to Hit & Blow - Julia Edition")
global mode_select = true; global affirm = ["yes", "y"];

while true
    #= Select game mode =#
    while true
        if mode_select == false
            print("Do you want to play the same mode? ")
            modeset = lowercase(readline())
            if modeset in affirm
                break
            end
        end
        global game_mode = set_mode()
        global mode_select = false
        global level_select = true
        break
    end
    #= Select game level =#
    while true
        if level_select == false
            print("Do you want to play the same level? ")
            levelset = lowercase(readline())
            if levelset in affirm
                break
            end
        end
        global game_lvl, colors = get_level()
        global level_select = false
        break
    end
    #= Game instructions =#
    if game_lvl % 2 == 1
        println("Available colors are ", colors, ". Duplicates are not allowed.")
    else
        println("Available colors are ", colors, ". Duplicates are allowed.")
    end
    global guess_size = 4
    #= Play the game =#
    global all_sols_array = get_solutions(game_lvl, colors, guess_size)
    if game_mode == 1 || game_mode == 2 # Against CPU
        # Have CPU pick random solution
        the_solution = all_sols_array[rand(1:length(all_sols_array))]
        println("The Solution: ", the_solution) # Include for debugging

        # User attempts
        attmpt_num = 1 # Initial attempt number (first attempt)
        possible_solutions = copy(all_sols_array)
        while true
            if attmpt_num > 8 # Fail condition
                println("Too many guesses. Sorry.")
                println("Actual solution: ", the_solution)
                break
            end
            attempt = get_attempt(attmpt_num, all_sols_array, guess_size)
            hits, blows = check_attempt(attempt, the_solution, guess_size)
            println("Hits: ", hits, "; Blows: ", blows)
            if hits == guess_size # Win condition
                println("Congratulations! You win!")
                break
            end
            if game_mode == 2 # Provide assistance
                # find possible remaining get_solutions
                possible_solutions = find_possible(possible_solutions, attempt, hits, blows, guess_size)
                num_poss = length(possible_solutions)
                println("Possible solutions left: ", num_poss)
                #next_try = get_nexttry()
                #println("Try ", next_try,".")
                #= Include for debugging
                if num_poss < 11
                    for sol in possible_solutions
                        print(sol, "; ")
                    end
                    print("\n")
                end =#
            end
            # Continue to next attempt
            attmpt_num += 1
        end # while
    elseif game_mode == 3 # Manual mode
        println("Mode not yet implemented.")
        # Stuff goes here
    else # game_mode == 0
        println("Nothing to see here. Move along.")
        # Stuff goes here
    end
    print("Would you like to play again? ")
    playagain = lowercase(readline())
    if playagain in affirm
        continue # Go back to the beginning of main while loop
    end
    break # If not playing again, end the loop.
end

print("Thanks for playing my game! (Press Enter to exit.)")
pause = readline()
