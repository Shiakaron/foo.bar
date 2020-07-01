"""
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and broken the bunnies out of Lambda's prison - and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6
and 6/6, but the final solution remains the same.)

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
Output:
    6

Input:
solution.solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    16
"""
def solution(entrances, exits, paths):
    """
    """
    total_flow = 0
    remaining = paths[:]

    prev_flow = -1

    while prev_flow != total_flow:
        prev_flow = total_flow

        for j in entrances:
            node = j
            visited = []
            path = []
            while True:
                # if node is an exit find the bottleneck flow through the path and update the remaining capacity
                if node in exits:
                    path.append(node)
                    bottleneck = 2000001
                    for ind in range(len(path)-1):
                        bottleneck = min(remaining[path[ind]][path[ind+1]], bottleneck)
                    total_flow += bottleneck
                    for ind in range(len(path)-1):
                        remaining[path[ind]][path[ind+1]] -= bottleneck
                        remaining[path[ind+1]][path[ind]] += bottleneck
                    break

                found = False
                visited.append(node)
                # let's get greedy
                maximum = 0
                index = 0
                for ind, val in enumerate(remaining[node]):
                    if ind not in visited and val>maximum:
                        maximum = val
                        index = ind
                        found = True

                # if theres an unvisited neighbour, append path with current node and set the next node to expore
                if found:
                    path.append(node)
                    node = index
                # else, if theres no unexplored neighbour and the path is empty then there is no path from this source
                elif not path:
                    break
                # else, backtrack
                else:
                    node = path.pop()

    return total_flow
