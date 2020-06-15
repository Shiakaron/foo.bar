"""
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've identified and destroy them at the same time.

But there's a few catches. First, the bombs self-replicate via one of two distinct processes:
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs. The replication process can be changed each cycle.

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, and the device might survive. Too many, and you might overload the mass capacitors and create a singularity at the heart of the space station - not good!

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!)

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP. Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string) that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done! M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would need to pass, so the solution would be "1". However, if M = "2" and F = "4", it would not be possible.

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution('4', '7')
Output:
    4

Input:
solution.solution('2', '1')
Output:
    1
"""
def solution(x,y):
    """
    Starting from the needed configuration we will tracerse backward by continuously subtracting the smallest of the arguments from the other until they are equal. If equality occurs at (1,1) then the configuration is possible and the number of operations gives the generations needed. If equality occurs at a number greater than 1 then the configuration is "impossible"
    Notes:
        a. if either x or y get reduced to 1 then a solution is possible
        b. we speed the search when x and y are very different by using the modulo operator
    """
    M = int(x)
    F = int(y)
    equality = False
    gen = 0
    while(not equality):
        genplus = 0
        if M >= F:
            if M%F != 0:
                genplus = M//F
                M %= F
            elif F == 1:
                genplus = M-1
                M = 1
                equality = True
            else:
                return "impossible"
        elif F > M:
            if F%M != 0:
                genplus = F//M
                F %= M
            elif M == 1:
                genplus = F-1
                F = 1
                equality = True
            else:
                return "impossible"
        gen += genplus
    return str(gen)
