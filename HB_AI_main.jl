#= HB_AI_main.jl
(will be) Same as HB_AI_main.py, but in Julia
By: Timothy Anglea
=#
x = 1+1
if x == 2
    println("Hello")
else
    println("Hi")
end
println(x != 2 ? "hELLO" : "hI")
rand(1:6)