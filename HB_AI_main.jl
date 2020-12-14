#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
=#
#using Combinatorics
#using Iterators
using Printf

x = 1+2;
if x == 2
    println("Hello")
else
    println("Hi")
end
println(x != 2 ? "hELLO" : "hI")
rand(1:6);

function get_solutions(clrs, atmp_size)
    #all_pairs = Iterators.product(fill(clrs,atmp_size)...);
    all_sols_array = String[]
    #println(typeof(all_sols_array))
    for pair in Iterators.product(fill(clrs,atmp_size)...)
        #println(typeof(pair))
        pair_str = tuple2str(pair)
        append!(all_sols_array, [pair_str])
    end
    return all_sols_array
end

function tuple2str(tuple)
    return_str = ""
    #println(typeof(return_str))
    for c in tuple
        return_str *= c # Concatenate
    end
    return return_str
end

colors6 = "cgprwy";
guess_size = 4;
all_sols_array = get_solutions(colors6, guess_size)
#= for thing in all_sols_array
    println(thing)
end =#
println(length(all_sols_array))
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
