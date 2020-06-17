def get_n_matrix(m, N, unstable):
    """
    """
    n = []
    for i in range(N):
        n.append(m[i][:])
        if unstable[i] == 0: # i.e. stable
            n[i][i] = 1
    return n

def get_T_matrix(n, sums, N):
    """
    """
    T = []
    for i in range(N):
        temp = 1
        for j in range(N):
            if j!=i:
                temp *= sums[j]
        copy = n[i][:]
        for j in range(N):
            copy[j] *= temp
        T.append(copy)
    return T

def vector_matrix_multiplication(list1, listoflists2):
    """
    """
    x = []
    for i in range(len(list1)):
        y = 0
        for j in range(len(listoflists2)):
            y += list1[j]*listoflists2[j][i]
        x.append(y)
    return x

def find_gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

def solution(m):
    """
    """
    N = len(m) # size of m matrix
    m_rowsums = [sum(m[i]) for i in range(N)] # holds the sum of each row in m matrix

    unstable = [] # 1,0 list. 1=unstable, 0=stable
    count_stable_states = 0
    for i in range(N):
        if m_rowsums[i] == 0:
            unstable.append(0) # false
            count_stable_states += 1
        else:
            unstable.append(1) # true

    if count_stable_states == 1:
        return [1, 1]

    n = get_n_matrix(m, N, unstable)
    n_rowsums = [sum(n[i]) for i in range(N)]

    T = get_T_matrix(n, n_rowsums, N)
    print("T:", T)
    composition = [1]+[0]*(N-1)

    history = []
    finished = False
    while(not finished):
        composition = vector_matrix_multiplication(composition[:], T)

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

        for i in range(len(ret)):
            ret[i] = ret[i]//gcd

        finished = True
        for i in range(1,N):
            if unstable[i] and composition[i] != 0:
                finished = False

        for i in range(len(history)):
            if ret == history[i]:
                finished = True
                break

        if ret[-1] > 2147483647:
            break

        print(ret)
        history.append(ret)
    return history[-1]

solution([
[1, 1, 1],
[1, 0, 1],
[0, 0, 0]])

solution([
[1, 1, 1, 1],
[1, 2, 1, 1],
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
[0, 1, 1, 0, 0, 1],
[4, 0, 0, 3, 2, 0],
[0, 4, 1, 0, 5, 6],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0]])
