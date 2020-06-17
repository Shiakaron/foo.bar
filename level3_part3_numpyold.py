"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is [0, 3, 2, 9, 14].

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({
{0, 1, 0, 0, 0, 1},
{4, 0, 0, 3, 2, 0},
{0, 0, 0, 0, 0, 0},
{0, 0, 0, 0, 0, 0},
{0, 0, 0, 0, 0, 0},
{0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([
[0, 2, 1, 0, 0],
[0, 0, 0, 3, 4],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]
"""
import numpy as np

def get_n_matrix(m, N, unstable):
    """
    """
    e = []
    for i in range(N):
        a = [0]*N
        if unstable[i] == 0:
            a[i] = 1
        e.append(a)
    e = np.array(e)
    return np.array(m) + e

def get_sigma_matrix(sums, N):
    """
    """
    sigma = np.eye(N, dtype=int)
    for i in range(N):
        temp = sums[i]*np.eye(N, dtype=int)
        temp[i,i] = 1

        sigma *= temp
    return sigma

def get_unit_array(i,siz):
    """
    return an array with size=siz and all zeros except the element in the ith position to be 1
    """
    x = np.array([0]*siz)
    x[i] = 1
    return x

def find_gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

def solution(m):
    """
    Starting from a composition with only the 0-th state, I will evolve the composition using a matrix algebra where the new composition c' = c*T (T - transformation matrix, c - initial composition). The calculation will be such that we have a common factor outside. The matrix will be given as T = Sigma*n, where n and Sigma are both matrices we need to compute from the m matrix.

    Step 1: Identify which states are unstable which are stable by computing the sums of each row of the m matrix

    Step 2:
        n = m + e
        where for each unstable state
        example for N=5 and s0 and s1 are unstable
        e = [
        0:  [0, 0, 0, 0, 0]
        1:  [0, 0, 0, 0, 0]
        2:  [0, 0, 1, 0, 0]
        3:  [0, 0, 0, 1, 0]
        4:  [0, 0, 0, 0, 1]
            ]

    Step 3:
        we compute the sum of each row of n and we construct a matrix to literally deal with taking out the factor sum[0]*sum[1]*...*sum[N] in the denominator. The ith element on the diagonal of Sigma is the product of the sums devided by sum[i]
        example for N=5 and s0 and s1 and s2 are unstable
        Note : sum[3]=sum[4]=1
        Sigma = [
                [sum[1]sum[2], 0, 0, 0, 0]
                [0, sum[0]sum[2], 0, 0, 0]
                [0, 0, sum[0]sum[1], 0, 0]
                [0, 0, 0, sum[0]sum[1]sum[2], 0]
                [0, 0, 0, 0, sum[0]sum[1]sum[2]]
                ]
        This matrix can be created my multiplying N matrices together

    Step 4:
        Compute the transformation matrix T and start updating the composition.

    Step 5:
        Recognise when to end the loop:
            a. There's only the 0th unstable component left (or no unstable components at all)
            c. ??

    Step 6:
        After the loop ends we take the stable products and the denominator, find their greatest common denominator to simplify them and we return the appropriate array

    """
    N = len(m) # size of m matrix
    unstable = [] # 1,0 list. 1=unstable, 0=stable
    m_rowsums = [sum(m[i]) for i in range(N)] # holds the sum of each row in m matrix

    for i in range(N):
        if m_rowsums[i] == 0:
            unstable.append(0) # false
        else:
            unstable.append(1) # true

    n = get_n_matrix(m, N, unstable)

    n_list = n.tolist()
    n_rowsums = [sum(n_list[i]) for i in range(N)]

    sigma = get_sigma_matrix(n_rowsums, N)

    T = sigma@n


    composition = get_unit_array(0,N) # initial composition
    history = []

    finished = False
    while(not finished):
        history.append(composition)
        newcomposition = composition@T
        composition = newcomposition
        
        finished = True
        for i in range(1,N):
            if unstable[i] and composition[i] != 0:
                finished = False

    ret = []
    for i in range(1,N):
        if not unstable[i]:
            ret.append(composition[i])
    ret.append(sum(ret))

    num1 = ret[0]
    num2 = ret[1]
    gcd = find_gcd(num1, num2)
    for i in range(2, len(ret)):
        gcd = find_gcd(gcd, ret[i])
    ret = np.array(ret)//gcd
    return ret.tolist()



solution([
[0, 2, 1, 0, 0],
[0, 0, 0, 3, 4],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0]])

solution([
[0, 1, 0, 0, 0, 1],
[4, 0, 0, 3, 2, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0]])
