#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
=#
using Combinatorics
using Iterators
using Printf

function get_attempt(num, all_sol, atmp_size)
    local attempt
    while true
        try
            print("Guess #", num, ": ")
            attempt = lowercase(readline())
            if length(attempt) != atmp_size
                println("Attempt must be ", atmp_size, " colors. Try again.")
                continue
            end
            if attempt not in all_sol
                println("Not a valid attempt. Try again.")
                continue
            end
            break
        catch str_error
            println("We've had an error. Try again.")
            continue
        end # try
    end # while
    return attempt
end

function check_attempt(attempt, the_sol, atmp_size)
    local h = 0; local b = 0;
    #local atmpt_check = {Int}[];
    local sol_check = {Int}[];
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
            if attempt[i1] == the_sol[i2] # If there's a match
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
        all_sols = product(fill(clrs, atmp_size)...);
    else
        all_sols = permutations(clrs, atmp_size)    
    end
    all_sols_array = String[]
    #println(typeof(all_sols_array))
    for pair in all_sols
        pair_str = ""
        for c in pair
            pair_str *= c # Concatenate
        end
        append!(all_sols_array, [pair_str])
    end
    return all_sols_array
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

level = 1;
colors6 = "cgprwy";
guess_size = 4;
all_sols_array = get_solutions(level, colors6, guess_size)
#= for thing in all_sols_array
    println(thing)
end =#
#println(length(all_sols_array))
#
print("Guess #1: ")
attempt = readline()
#println(typeof(attempt))
if attempt in all_sols_array
    @printf("Your attempt is %s.", attempt)
else
    println("Not a valid attempt.")
end
#
