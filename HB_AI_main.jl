#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
Still need to improve"get_nexttry".
=#
using Combinatorics
using Random

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
    local sol_check = Int[];
    for i1 in 1:atmp_size # attempt[i1]
        for i2 in 1:atmp_size # the_sol[i2]
            if i2 in sol_check
                continue
            end # if
            if attmpt[i1] == the_sol[i2] # If there's a match
                if i1 == i2 # If it's in the same position
                    h += 1 # it's a hit
                else # If it's not in the same position
                    b += 1 # it's a blow
                end # if
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

function get_nexttry(all_poss, all_sols, atmp_size)
    num_poss = length(all_poss)
    print("Thinking... ")
    if num_poss < 20 # Take all of them
        poss_select = copy(all_poss)
        # Plus a few extra random ones, to check full solution space more quickly.
        append!(poss_select, randsubseq(all_sols, (20-num_poss)/length(all_sols)))
    else # some random subset
        poss_select = randsubseq(all_poss, 20/length(all_poss))
    end
    local vlen_array = zeros(Int, length(poss_select)) # same length as poss_select
    if num_poss < 200 # Take all of them
        maybe_sol_array = copy(all_poss)
    else # some random subset
        maybe_sol_array = randsubseq(all_poss, 200/length(all_poss))
    end
    for i1 in 1:length(poss_select)
        poss_attmpt = poss_select[i1]
        for maybe_sol in maybe_sol_array
            hp, bp = check_attempt(poss_attmpt, maybe_sol, atmp_size)
            valid_sols = find_possible(maybe_sol_array, poss_attmpt, hp, bp, atmp_size)
            vlen_array[i1] += length(valid_sols)
        end
        #print(poss_attmpt, ": ", vlen_array[i1], "; ") # Include for debugging
    end
    return poss_select[argmin(vlen_array)]
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
        #println("The Solution: ", the_solution) # Include for debugging

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
                next_try = get_nexttry(possible_solutions, all_sols_array, guess_size)
                println("Try ", next_try,".")
                #= #Include for debugging
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
        #println("Mode not yet implemented.")
        attmpt_num = 1
        possible_solutions = copy(all_sols_array)
        while true
            if attmpt_num > 8
                println("Too many guesses. Sorry.")
                break
            end
            attempt = get_attempt(attmpt_num, all_sols_array, guess_size)
            local hits;
            while true
                try
                    print("How many hits? ")
                    hits = parse(Int, readline())
                    print("How many blows? ")
                    blows = parse(Int, readline())
                    if hits < 0 || hits > guess_size || blows < 0 || blows > guess_size || (hits+blows) > guess_size
                        println("Not a valid number of hits & blows. Please try again.")
                        continue
                    end
                    valid_solutions = find_possible(possible_solutions, attempt, hits, blows, guess_size)
                    if length(valid_solutions) == 0
                        println("Something went wrong. No valid solutions exist.\nEnter the number of hits & blows again.")
                        continue
                    end
                    possible_solutions = valid_solutions
                    break
                catch num_error
                    println("Not a valid number entry. Try again.")
                    continue
                end # try
            end # while
            if hits == guess_size # Win condition
                println("Congratulations! You win!")
                break
            end # if
            println("Possible solutions left: ", length(possible_solutions))
            if length(possible_solutions) < 21
                for sol in possible_solutions
                    print(sol, "; ")
                end
                print("\n")
            end # if
            # Continue to next attempt
            attmpt_num += 1
        end # while
    else # game_mode == 0
        println("This is a secret to everyone.")
        the_solution = all_sols_array[rand(1:length(all_sols_array))]
        #println("The Solution: ", the_solution) # Include for debugging

        attmpt_num = 1 # Initial attempt number (first attempt)
        possible_solutions = copy(all_sols_array)
        while true
            if attmpt_num > 8 # Fail condition
                println("Too many guesses. Sorry.")
                println("Actual solution: ", the_solution)
                break
            end
            if attmpt_num > 1
                attempt = get_nexttry(possible_solutions,all_sols_array, guess_size)
            else
                attempt = possible_solutions[rand(1:length(possible_solutions))]
            end
            println("Guess #", attmpt_num, ": ", attempt)
            hits, blows = check_attempt(attempt, the_solution, guess_size)
            println("Hits: ", hits, "; Blows: ", blows)
            if hits == guess_size # Win condition
                println("Congratulations! You win!")
                break
            end
            possible_solutions = find_possible(possible_solutions, attempt, hits, blows, guess_size)
            num_poss = length(possible_solutions)
            println("Possible solutions left: ", num_poss)
            #=if num_poss < 20
                for sol in possible_solutions
                    print(sol, "; ")
                end
                print("\n")
            end # if =#
            # Continue to next attempt
            attmpt_num += 1
        end # while
    end
    print("Would you like to play again? ")
    playagain = lowercase(readline())
    if playagain in affirm
        continue # Go back to the beginning of main while loop
    end
    break # If not playing again, end the loop.
end

print("Thanks for playing my game! (Press Enter to exit.)")
pause = readline();
