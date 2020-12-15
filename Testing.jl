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

#=
# a^p + b^p = x = c^p + d^p; c>a>=b>d
n = Int128(1001)
N = Int128(1500)
p = 4
println("Starting...")
sols = Tuple{Int128,Int128,Int128,Int128,Int128}[] # Empty array of solutions
@time begin
for c in n:1:N
    @printf("Checking c = %d...\n", c)
    min_a = Int128(ceil(((c^p)/2)^(1/p)))
    for a in min_a:1:c-1
        if a % 100 == min_a % 100
            @printf("  Checking a = %d...\n", a)
        end
        min_b = Int128(ceil((c^p - a^p)^(1/p)))
        for b in min_b:1:a
            x1 = a^p + b^p
            min_d = Int128(floor((x1 - c^p)^(1/p)))
            for d in min_d:1:b-1
                x2 = c^p + d^p
                if x2 < x1
                    continue # go to next d value
                elseif x2 > x1
                    break # go to next b value
                else
                    append!(sols, [(a,b,c,d,x1)]) # Save solution
                end
            end # for d
        end # for b
    end # for a
end # for c
end # @time
for thing in sols # For each solution, display result nicely
    a1 = thing[1]; b1 = thing[2]; c1 = thing[3]; d1 = thing[4]; x = thing[5]
    @printf("%d^%d + %d^%d = %d^%d + %d^%d = %d\n",a1,p,b1,p,c1,p,d1,p,x)
end
println(length(sols))
#print(f/cnt)
=# 
#
function scopetest()
    local thing
    while true
        try
            print("Enter a number (or not): ")
            thing = parse(Int, readline()) # Give thing scope outside of while loop.
            if thing > 10 || thing < 0
                println("Number is outside of range. Try again.")
                continue
            end
            break
        catch err
            println("Not an integer. Try again.")
            continue
        end
    end
    return thing
    @printf("Your number is %d.",thing)
end

stuff = scopetest()
println("The number is ", stuff, ".")
#
#=
mystring = "abcde"
println(mystring[3])
mystring[3] = "f" # Not valid; strings are immutable
println(mystring)
=#