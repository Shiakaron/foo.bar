"""
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit of sabotage while you're at it - so you took the job gladly.

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time.

The fuel control mechanisms have three operations:

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution('15')
Output:
    5
"""
def solution(str):
    """
    Starting from the integer argument, we traverse the tree of possibilities (via BFS) by:
        1. dividing by 2 when we have an even number
        2. adding and subtracting 1 when we have an odd number
    We use a dictionary (could use list) to keep track which node is visited more than once so that we can ignore it. The function returns the minimum number of steps required to reach 1.
    """
    visited = {}
    found = False
    mincount = None
    gen = 0
    queue = []
    nextgen = [int(str)]
    while(not found):
        queue = nextgen[:]
        queue.sort()
        nextgen *= 0
        while(queue):
            x = queue.pop(0)
            if x==1:
                found = True
                mincount = gen
                break
            elif x not in visited:
                if x%2==0:
                    if x//2 not in visited:
                        nextgen.append(x//2)
                else:
                    if x-1 not in visited:
                        nextgen.append(x-1)
                    if x+1 not in visited:
                        nextgen.append(x+1)
                visited[x] = gen
        gen += 1
        if(gen > 3000):
            break
    return mincount
