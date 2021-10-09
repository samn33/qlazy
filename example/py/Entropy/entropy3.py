import random
import math
import numpy as np
from qlazy import QState, DensOp

def computational_basis(dim,rank):

    return np.array([[1 if j==i else 0 for j in range(dim)] for i in range(rank)])

def normalized_random_list(dim):

    rand_list = np.array([random.random() for _ in range(dim)])
    return rand_list / sum(rand_list)

def is_power_of_2(N):

    if math.log2(N) == int(math.log2(N)):
        return True
    else:
        return False
    
if __name__ == '__main__':

    # settings
    mixed_num = 3  # mixed number of pure states
    qnum_A = 2     # qubit number of system A

    # system A
    dim_A = 2**qnum_A
    rank = dim_A
    id_A = list(range(qnum_A))

    # system B
    dim_B = mixed_num*rank
    if is_power_of_2(dim_B):
        qnum_B = int(math.log2(dim_B))
    else:
        qnum_B = int(math.log2(dim_B)) + 1
        dim_B = 2**qnum_B
    id_B = [i+qnum_A for i in range(qnum_B)]

    # basis of system A,B
    basis_A = computational_basis(dim_A, rank)
    basis_B = computational_basis(dim_B, mixed_num*rank)

    # random schmidt coefficients
    coef = normalized_random_list(rank)

    # random probabilities for mixing the pure states
    prob = normalized_random_list(mixed_num)

    # basis for system A+B
    dim_AB = dim_A * dim_B
    basis_AB = [None]*mixed_num
    for i in range(mixed_num):
        basis_AB[i] = np.zeros(dim_AB)
        for j in range(dim_A):
            basis_AB[i] = basis_AB[i] + \
                math.sqrt(coef[j]) * np.kron(basis_A[j],basis_B[i*dim_A+j])

    # construct the density operator
    matrix = np.zeros((dim_AB,dim_AB))
    for i in range(mixed_num):
        matrix = matrix + prob[i] * np.outer(basis_AB[i],basis_AB[i])
    de = DensOp(matrix=matrix)

    # calculate the entropies
    ent = de.entropy()
    ent_A = de.entropy(id_A)
    ent_B = de.entropy(id_B)

    print("** S(A,B)    = {:.4f}".format(ent))
    print("** S(A)      = {:.4f}".format(ent_A))
    print("** S(B)      = {:.4f}".format(ent_B))
    print("** S(B)-S(A) = {:.4f}".format(ent_B-ent_A))
