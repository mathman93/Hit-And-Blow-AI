#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
=#
#using Combinatorics
#using Iterators

x = 1+2;
if x == 2
    println("Hello")
else
    println("Hi")
end
println(x != 2 ? "hELLO" : "hI")
rand(1:6);

colors6 = "cgprwy";
attempt_length = 2;
all_pairs = Iterators.product(fill(colors6,attempt_length)...);
for pair in all_pairs
    #println(join(pair, ""))
    println(pair)
end
println(length(all_pairs))

println("Guess #1: ")
attempt = readline()
println(typeof(attempt))
println("Your attempt is $attempt.")
