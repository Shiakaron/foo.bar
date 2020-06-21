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

def combine_vetices(a, b, g):
    """
    returns the graph after combining the two vertices a,b
    """
    N = len(g)
    ret = []
    if (a > b):
        temp = a
        a = b
        b = temp

    for i in range(N-1):
        temp = []
        for j in range(N-1):
            if i<b:
                if i!=a:
                    if j < b:
                        if j!=a:
                            temp.append(g[i][j])
                        else: # j=a
                            temp.append(g[i][a]+g[i][b])
                    else: # j>=b
                        temp.append(g[i][j+1])
                else: # i=a
                    if j < b:
                        if j!= a:
                            temp.append(g[a][j] + g[b][j])
                        else: #j=a => leave the diagonal zero
                            temp.append(0)
                    else: # j>=b
                        temp.append(g[a][j+1] + g[b][j+1])
            else: # i>=b
                if j < b:
                    if j!=a:
                        temp.append(g[i+1][j])
                    else: # j=a
                        temp.append(g[i+1][a]+g[i+1][b])
                else: # j>=b
                    temp.append(g[i+1][j+1])
        ret.append(temp)
    return ret

def deep_copy(lsl):
    copy = []
    for ls in lsl:
        rowcopy = ls[:]
        copy.append(ls)
    return copy

def fix_ordering(graph, source_row, sink_row):
    """
    changes the ordering of the graph such that the source is the 1st row and the sink is the last
    """
    N = len(graph)
    if (source_row==0 and sink_row==N-1):
        return graph

    ret = []
    order = [source_row]
    for i in range(N):
        if i != source_row and i != sink_row:
            order.append(i)
    order.append(sink_row)
    print(order)
    for i in order:
        temp = []
        for j in order:
            temp.append(graph[i][j])
        ret.append(temp)
    return ret

def get_graph(entrances, exits, paths):
    """
    1. We ignore any outgoing edges from the sinks (exits), any ingoing edges to sources (entrances) and any edges (paths) connecting back to the same vertex (room)
    2. We want to combine entrances (and exits) to a single mega-entrance (and mega-exit)
    3. Order the rows in the graph such that the first is the source and the last is the sink
    """
    N = len(paths)
    graph = []
    for ind, val in enumerate(paths):
        temp = val[:]
        if ind in exits:
            temp = [0]*N
        else:
            for j in entrances:
                temp[j] = 0
        temp[ind] = 0
        graph.append(temp)

    sources = entrances[:]
    sinks = exits[:]
    sources.sort()
    sinks.sort()

    while(len(sources)>1):
        graph = combine_vetices(sources[0],sources[-1],deep_copy(graph))
        source_row = sources.pop(-1)
        for ind, sink_row in enumerate(sinks):
            if sink_row>source_row:
                sinks[ind] -= 1

    while(len(sinks)>1):
        graph = combine_vetices(sinks[0],sinks[-1],deep_copy(graph))
        sink_row = sinks.pop(-1)
        if sources[0]>sink_row:
            sources[0] -= 1

    graph =  fix_ordering(graph, sources[0], sinks[0])

    return graph

def zero_lsl(siz):
    ret = []
    for i in range(N):
        ret.append([0]*N)
    return ret

def identify_levels(g):
    """
    identify levels - distance from source - using bfs
    In the case that there is no path to the sink vertex then we return an empty list
    The source and sink technically shouldnt be assigned a level so I will "tag" them by setting source = 0 and the sink = N, where N=len(g).
    """
    N = len(g)
    ret = [0]*N # holds the level of each vertex(row). Initialised to zero for all vertices.
    explored = []
    level = 0
    queue = [0]
    while(len(queue)>0):
        newbreadth = []
        for val in queue:
            if val not in explored:
                vertex = g[val]
                for ind, e in enumerate(vertex):
                    if e>0:
                        newbreadth.append(ind)
                explored.append(val)
                ret[val] = level
        queue = newbreadth[:]
        level += 1

    if ret[-1] == 0:
        ret = []
    else:
        ret[-1] = N

    return ret

def dfs_source_to_sink(c, ls):
    """
    dfs to find possible path from source to sink. the minimum capacity of an edge will determine the augmenting flow
    """
    N = len(c)
    path = [0]
    stack = [] # to explore
    dead_ends = []
    capacities = []
    level = 1
    while(len(path)>0):
        vertex = path[-1]
        row = c[vertex]
        if vertex == N-1:
            break

        wayforward = False
        for ind, val in enumerate(row):
            if (val>0 and ind not in dead_ends and (ls[ind] == level or ind == (N-1))):
                wayforward = True
                if ind not in stack:
                    stack.append(ind)

        if wayforward:
            next = stack.pop()
            path.append(next)
            capacities.append(row[next])
            level += 1
        else:
            dead_ends.append(path.pop())
            if capacities != []:
                capacities.pop()
            level -= 1

    if path == []:
        return [], 0
    else:
        return path, min(capacities)

def update_rem_cap(rem_cap, path, bottleneck):
    """
    given the possible path and the bottleneck, we update the remaining capacity of the graph
    """
    P = len(path)
    for n in range(P-1):
        v0 = path[n]
        v1 = path[n+1]
        rem_cap[v0][v1] -= bottleneck
        rem_cap[v1][v0] += bottleneck
    return rem_cap

def solution(entrances, exits, paths):
    """
    Will implement Dinic's algorithm to identify the maximum flow from the sources (entrances) to the sinks (exits). The reaosn I chose this algorithm instead of the simplier Ford-Fulkerson is because of the high possible values of flow (corridor capacity) and the small number of vertices (rooms).
    """
    if exits == [] or entrances == [] or paths == []:
        return 0

    graph = get_graph(entrances, exits, paths) # process the input before beginning the algorithm
    N = len(graph)
    flow = 0
    remaining_capacity = deep_copy(graph)

    while(True):
        levels = identify_levels(remaining_capacity)
        if levels == []:
            break

        while(True):
            possible_path, bottleneck = dfs_source_to_sink(remaining_capacity, levels)
            if possible_path == []:
                break
            else:
                flow += bottleneck
                remaining_capacity = update_rem_cap(remaining_capacity[:], possible_path, bottleneck)
    return flow

def print_lsl(X):
    print("X:")
    for ind, row in enumerate(X):
        print(ind, row)

# foo_bar visible tests
# solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])

# check 4: passed. total flow is 11
# solution([0],[5],[[0,6,5,0,0,0],[0,0,0,0,0,10],[0,4,0,3,0,0],[0,0,0,0,2,0],[0,0,0,0,0,1],[0,0,0,0,0,0]])
# x=[[0,6,5,0,0,0],[0,0,0,0,0,10],[0,4,0,3,0,0],[0,0,0,0,2,0],[0,0,0,0,0,1],[0,0,0,0,0,0]]
# levels = identify_levels(x)
# print(levels)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# levels = identify_levels(x)
# print(levels)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# levels = identify_levels(x)
# print(levels)


# check 3: passed. total flow is 4000000
# solution([0],[3],[[0,2000000,2000000,0],[0,0,1,2000000],[0,0,0,2000000],[0,0,0,0]])
#
# check 2: passed. total flow is 19
# solution([0],[5],[[0,10,10,0,0,0],[0,0,2,4,8,0],[0,0,0,0,9,0],[0,0,0,0,0,10],[0,0,0,6,0,10],[0,0,0,0,0,0]])
# x = [
# [0,10,10,0,0,0],
# [0,0,2,4,8,0],
# [0,0,0,0,9,0],
# [0,0,0,0,0,10],
# [0,0,0,6,0,10],
# [0,0,0,0,0,0]]
# levels = identify_levels(x)
# print(levels)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# levels = identify_levels(x)
# print(levels)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)

# check 1: passed. total flow is 30
# solution([0],[10],[[0,5,10,15,0,0,0,0,0,0,0],[0,0,0,0,10,0,0,0,0,0,0],[0,15,0,0,0,20,0,0,0,0,0],[0,0,0,0,0,0,25,0,0,0,0],[0,0,0,0,0,25,0,10,0,0,0],[0,0,0,5,0,0,0,0,30,0,0],[0,0,0,0,0,0,0,0,20,10,0],[0,0,0,0,0,0,0,0,0,0,5],[0,0,0,0,15,0,0,0,0,15,15],[0,0,0,0,0,0,0,0,0,0,10],[0,0,0,0,0,0,0,0,0,0,0]])
# x = [
# [0,5,10,15,0,0,0,0,0,0,0],
# [0,0,0,0,10,0,0,0,0,0,0],
# [0,15,0,0,0,20,0,0,0,0,0],
# [0,0,0,0,0,0,25,0,0,0,0],
# [0,0,0,0,0,25,0,10,0,0,0],
# [0,0,0,5,0,0,0,0,30,0,0],
# [0,0,0,0,0,0,0,0,20,10,0],
# [0,0,0,0,0,0,0,0,0,0,5],
# [0,0,0,0,15,0,0,0,0,15,15],
# [0,0,0,0,0,0,0,0,0,0,10],
# [0,0,0,0,0,0,0,0,0,0,0]]
# levels = identify_levels(x)
# print(levels)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# x = update_rem_cap(x[:], possible_path, bottleneck)
# print_lsl(x)
# possible_path, bottleneck = dfs_source_to_sink(x, levels)
# print(possible_path, bottleneck)
# # levels = identify_levels(x)
# # print(levels)
