# Testing.jl
using Printf
function func(num)
    result = big(0.0)
    term = big(1.0)
    result += term
    for i1 in 1:400
        term = (term * num) / i1
        result += term
    end
    return result
end

for x in -2:0.5:2
    @printf("f(%.1f) = %.9f \n", x, func(big(x)))
end
println(func(70.0))
println(exp(70.0))
println(func(complex(0,3.1415926)))
println(func(complex(0,pi)))
println(exp(complex(0,pi)))