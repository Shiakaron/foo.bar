"""

Distract the Guards
===================

The time for the mass escape has come, and you need to distract the guards so that the bunny prisoners can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the guards are fond of bananas. And gambling. And thumb wrestling.

The guards, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two guards will pair off to thumb wrestle. The guard with fewer bananas will bet all their bananas, and the other guard will match the bet. The winner will receive all of the bet bananas. You don't pair off guards with the same number of bananas (you will see why, shortly). You know enough guard psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of guards will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to guarding the prisoners, and you don't want THAT to happen!

For example, if the two guards that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to guarding.

How is all this useful to distract the guards? Notice that if the guards had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the guards in such a way that the maximum number of guards go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each guard starts with, returns the fewest possible number of guards that will be left to watch the prisoners. Element i of the list will be the number of bananas that guard i (counting from 0) starts with.

The number of guards will be at least 1 and not more than 100, and the number of bananas each guard starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(1,1)
Output:
    2

Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0
"""

def get_gcd(a, b):
    while b:
        a, b = b, a%b
    return a


def valid_pair(x, y):
    """
    return true of the pair will be stuck in an infinite loop
    """
    equal = False
    if x == y:
        equal = True
    while(not equal):
        gcd = get_gcd(x, y)
        x //= gcd
        y //= gcd
        if (x+y)%2 != 0:
            return True
        if x > y:
            temp = y
            x -= temp
            y += temp
        else:
            temp = x
            x += temp
            y -= temp
        if x == y:
            equal = True
    return False

def find_pair(count, map):
    """
    returns the pair, which when severed from the graph, will leave the graph with the most edges behind.
    i.e. the pair will remove the least edges from the overall graph when disconnected.
    This hopefully will ensure that the best solution is reached
    """
    N = len(map)
    edges_severed = []
    pairs = []
    for key in map:
        neighbs = map[key]
        min_edges = 2*N-3 # edges severed from a maximally connected graph is 2N-4
        k = key
        for neighb in neighbs:
            tot_edges = count[neighb]+count[key]-2
            if min_edges > tot_edges:
                min_edges = tot_edges
                k = neighb
        edges_severed.append(min_edges)
        pairs.append((key,k))
    min_index = edges_severed.index(min(edges_severed))
    pair = pairs[min_index]
    return pair[0], pair[1]

def solution(banana_list):
    N = len(banana_list)
    if N == 1:
        return 1


    paircount = [] # keeps the number of pairs possible for ith guard
    pairmap = {} # map where key=ith guard and val=list of valid pairs
    guardsplaying = 0
    for ind, val in enumerate(banana_list):
        pairs = []
        for i in range(N):
            if valid_pair(val, banana_list[i]):
                pairs.append(i)
        if pairs != []:
            pairmap[ind] = pairs
            paircount.append(len(pairs))

    while(len(pairmap) > 1):
        A, B = find_pair(paircount, pairmap)
        del pairmap[A]
        del pairmap[B]

        del_from_map = []

        for key in pairmap:
            pairs = pairmap[key]
            for val in reversed(pairs):
                if val == A or val == B:
                    pairs.pop(pairs.index(val))
                    paircount[key] -= 1
            if pairs == []:
                del_from_map.append(key)

        for key in del_from_map:
            del pairmap[key]


        paircount[A] = N
        paircount[B] = N
        guardsplaying += 2

    return N - guardsplaying
