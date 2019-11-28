import random
import math
import numpy as np
from scipy.stats import unitary_group
from qlazypy import QState, DensOp

import sys

def computational_basis(dim):

    basis = np.array([[1 if j==i else 0 for j in range(dim)] for i in range(dim)])

    return basis

def normalized_random_list(dim):

    rand_list = np.array([random.random() for _ in range(dim)])
    #rand_list = np.array([1.0 for _ in range(dim)])
    norm = sum(rand_list)
    rand_list = rand_list / norm

    return rand_list

if __name__ == '__main__':

    qnum_A = 2 # NG
    #qnum_A = 3 # OK
    qnum_B = 4 # OK

    id_A = list(range(qnum_A))
    id_B = [i+qnum_A for i in range(qnum_B)]
    print(id_A,id_B)

    mixed_num = 2
    
    dim_A = 2**qnum_A
    dim_B = mixed_num * dim_A
    dim_AB = dim_A * dim_B
    
    basis_A = computational_basis(dim_A)
    basis_B = computational_basis(dim_B)

    #print(basis_A)
    #print(basis_B)

    coef = normalized_random_list(dim_A)
    prob = normalized_random_list(mixed_num)

    #print("dim_A = ", dim_A)
    #print("mixed_num = ", mixed_num)
    #print("coef =",coef)
    #print("prob =",prob)
    
    basis_AB = [None]*mixed_num
    for i in range(mixed_num):
        basis_AB[i] = np.zeros(dim_A*dim_B)
        for j in range(dim_A):
            basis_AB[i] = basis_AB[i] + \
                math.sqrt(coef[j]) * np.kron(basis_A[j],basis_B[i*dim_A+j])
        #print(basis_AB[i])

    mat = np.zeros((dim_AB,dim_AB))
    for i in range(mixed_num):
        mat = mat + prob[i] * np.outer(basis_AB[i],basis_AB[i])

    #print(mat)

    de = DensOp(matrix=mat)

    ent_AB = de.entropy()
    ent_A = de.entropy(id_A)
    ent_B = de.entropy(id_B)

    print("** S(A,B)   :", ent_AB)
    print("** S(A)     :", ent_A)
    print("** S(B)     :", ent_B)
    print("** S(B)-S(A):", ent_B-ent_A)

    de.free()
