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
