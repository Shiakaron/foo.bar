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
from fractions import *

def standard_form(m, N):
    m_rowsums = [sum(m[i]) for i in range(N)]
    stable = []
    unstable = []
    for ind, row in enumerate(m):
        if m_rowsums[ind] == 0:
            stable.append(ind)
        else:
            unstable.append(ind)
    order = stable + unstable
    p = []
    n = 0
    for i in stable:
        p.append(m[i][:])
        p[n][n] = 1
        n += 1
    for i in unstable:
        temp = []
        for j in order:
            temp.append(Fraction(m[i][j], m_rowsums[i]))
        p.append(temp)
    return p, len(stable)

def R_Q_matrices(p, stablecount, N):
    R, Q = [], []
    for i in range(stablecount,N):
        addR, addQ = [], []
        for j in range(stablecount):
            addR.append(p[i][j])
        for j in range(stablecount,N):
            addQ.append(p[i][j])
        R.append(addR)
        Q.append(addQ)
    return R, Q

def F_matrix(Q):
    siz = len(Q)
    A = []
    for i in range(siz):
        add = []
        for j in range(siz):
            if i==j:
                add.append(1-Q[i][j])
            else:
                add.append(-Q[i][j])
        A.append(add)
    return getMatrixInverse(A)

def lcmm(l):
		return reduce(lambda x, y: lcm(x, y), l)

def matmult(a,b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]

def transposeMatrix(m):
    t = []
    for r in range(len(m)):
        tRow = []
        for c in range(len(m[r])):
            if c == r:
                tRow.append(m[r][c])
            else:
                tRow.append(m[c][r])
        t.append(tRow)
    return t

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeterminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeterminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def list_lcm(lis):
    num1 = lis[0]
    num2 = lis[1]
    lcm = find_lcm(num1, num2)
    for i in range(2, len(lis)):
        lcm = find_lcm(lcm, lis[i])
    return lcm

def find_lcm(num1, num2):
    if(num1>num2):
        num = num1
        den = num2
    else:
        num = num2
        den = num1
    rem = num % den
    while(rem != 0):
        num = den
        den = rem
        rem = num % den
    gcd = den
    lcm = int(int(num1 * num2)/int(gcd))
    return lcm

def solution(m):
    N = len(m) # size of m matrix

    if N == 1:
        return [1,1]

    p, stablecount = standard_form(m, N)

    if stablecount == 1:
        return [1,1]

    R, Q = R_Q_matrices(p, stablecount, N)

    F = F_matrix(Q)

    FR = matmult(F,R)

    enums, denoms = [], []
    for frac in FR[0]:
        enums.append(frac.numerator)
        denoms. append(frac.denominator)

    lcm = list_lcm(denoms)

    answer = [val*lcm//denoms[ind] for ind, val in enumerate(enums)]
    answer.append(sum(answer))
    return(answer)
