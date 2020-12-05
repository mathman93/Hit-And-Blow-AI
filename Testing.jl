# Testing.jl
using Printf
function func(num)
    result = 0
    term = 1
    result += term
    for i1 in 1:100
        term = (term * num) / i1
        result += term
    end
    return result
end

for x in -2:0.5:2
    @printf("f(%.1f) = %.9f \n", x, func(x))
end
println(func(complex(0,3.1415926)))