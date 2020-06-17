from fractions import Fraction

def get_standard_form(m, N):
    m_rowsums = [sum(m[i]) for i in range(N)]
    stable = []
    unstable = []
    count_stable_states = 0
    for i in range(N):
        if m_rowsums[i] == 0:
            stable.append(i)
            count_stable_states += 1
        else:
            unstable.append(i)
    order = stable + unstable
    n = []
    for i in order:
        add = []
        for j in order:
            if i == j and i in stable:
                add.append(1)
            else:
                add.append(m[i][j])
        n.append(add)
    n_rowsums = [sum(n[i]) for i in range(N)]
    p = []
    for i in range(N):
        temp = 1
        for j in range(N):
            if j!=i:
                temp *= n_rowsums[j]
        copy = n[i][:]
        for j in range(N):
            copy[j] *= temp
        p.append(copy)
    denom = 1
    for i in range(N):
        denom *= n_rowsums[i]
    return p, count_stable_states, denom

def get_R_Q_matrices(p, stablecount, N):
    R = []
    Q = []
    for i in range(stablecount,N):
        addR = []
        addQ = []
        for j in range(stablecount):
            addR.append(p[i][j])
        for j in range(stablecount,N):
            addQ.append(p[i][j])
        R.append(addR)
        Q.append(addQ)
    return R, Q

def get_F_matrix(Q, denom):
    siz = len(Q)
    A = []
    for i in range(siz):
        add = []
        for j in range(siz):
            if i==j:
                add.append(1-Q[i][j]/denom)
            else:
                add.append(-Q[i][j]/denom)
        A.append(add)
    return getMatrixInverse(A)

def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
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
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def matrix_multiplication(x,y,denom):
    p = len(x)
    q = len(y[0])
    N = len(y)
    ans = []
    for i in range(p): # row
        row = []
        for j in range(q): # column
            val = 0
            for k in range(N):
                val += x[i][k]*y[k][j]/denom
            row.append(val)
        ans.append(row)
    return ans

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
    """
    Order the matrix so that rows start with terminal states first.

    Now that you have done that you know how to find R and Q.

    Calculate F=(I-Q)⁻¹.

    Calculate FR.

    Get the first line of FR and then you have your probabilities.

    Find the common denominator and return the int array how the specification has asked it to be formatted.
    """
    N = len(m) # size of m matrix

    p, count_stable_states, denom = get_standard_form(m, N);
    if count_stable_states == 1:
        return [1, 1]

    R, Q = get_R_Q_matrices(p, count_stable_states, N)

    F = get_F_matrix(Q, denom)

    FR = matrix_multiplication(F,R,denom)

    a = FR[0]+[1]
    b = [Fraction(i).limit_denominator() for i in a]
    denoms = [frac.denominator for frac in b]
    num1 = denoms[0]
    num2 = denoms[1]
    lcm = find_lcm(num1, num2)
    for i in range(2, len(denoms)):
        lcm = find_lcm(lcm, denoms[i])
    factors = [lcm//denoms[i] for i in range(len(denoms))]
    answer = [b[i].numerator*factors[i] for i in range(len(denoms))]
    print(answer)
    ret = [int(answer[i]) for i in range(len(answer))]
    print(ret)
    return ret



solution([
[1, 2, 3, 4],
[5, 6, 7, 8],
[0, 0, 0, 0],
[0, 0, 0, 0]])

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

solution([
  [0,1,0,0,0,1,2,3,2,1],
  [4,0,0,3,2,0,9,2,2,3],
  [1,0,0,1,0,0,0,0,0,0],
  [0,1,0,0,1,0,0,0,0,0],
  [0,1,0,0,0,0,0,2,0,0],
  [0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,3,0,0,0,0,0],
  [0,0,4,0,0,3,0,0,0,0],
  [0,0,0,0,0,10,2,0,0,0],
  [0,0,0,0,0,0,0,0,0,0]])
