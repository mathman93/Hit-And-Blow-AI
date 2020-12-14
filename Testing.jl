# Testing.jl
using Printf
#= 
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
=#

# a^p + b^p = x = c^p + d^p; c>a>=b>d
n = Int128(250001)
N = Int128(250001)
p = 5
println("Starting...")
#f = 0
#cnt = 0
@time begin
for c in n:1:N
    @printf("Checking c = %d...\n", c)
    min_a = Int128(ceil(((c^p)/2)^(1/p)))
    for a in min_a:1:c-1
        if a % 100 == 0
            @printf("  Checking a = %d...\n", a)
        end
        min_b = Int128(ceil((c^p - a^p)^(1/p)))
        for b in min_b:1:a
            x1 = a^p + b^p
            min_d = Int128(floor((x1 - c^p)^(1/p)))
            for d in min_d:1:b-1
                #cnt += 1
                x2 = c^p + d^p
                if x2 < x1
                    continue
                elseif x2 > x1
                    break
                else
                    #f += 1
                    println(x1)
                    #println(typeof(x1))
                    @printf("%d, %d, %d, %d\n",a,b,c,d)
                end
            end
        end
    end
end
end
#print(f/cnt)