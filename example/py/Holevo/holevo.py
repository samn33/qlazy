import random
import cmath
import numpy as np
import pandas as pd
from qlazy import QState, DensOp

MIN_DOUBLE = 0.000001

def classical_joint_entropy(A,B):

    code_num_A = max(A) + 1
    code_num_B = max(B) + 1

    prob = np.zeros((code_num_A,code_num_B))
    for i in range(len(A)):
        prob[A[i]][B[i]] += 1
    prob = prob / sum(map(sum, prob))

    ent = 0.0
    for i in range(code_num_A):
        for j in range(code_num_B):
            if abs(prob[i][j]) < MIN_DOUBLE:
                ent -= 0.0
            else:
                ent -= prob[i][j] * np.log2(prob[i][j])

    return ent
    
def classical_entropy(A):

    code_num = max(A) + 1

    prob = np.zeros(code_num)
    for a in A:
        prob[a] += 1.0
    prob = prob / sum(prob)

    ent = 0.0
    for p in prob:
        if abs(p) < MIN_DOUBLE:
            ent -= 0.0
        else:
            ent -= p * np.log2(p)

    return ent

def classical_mutual_information(A,B):

    ent_A = classical_entropy(A)
    ent_B = classical_entropy(B)
    ent_AB = classical_joint_entropy(A,B)

    return ent_A + ent_B - ent_AB
    
def holevo_quantity(X,de):

    samp_num = len(X)
    code_num = len(de)

    prob = np.zeros(code_num)
    for x in X:
        prob[x] += 1.0
    prob = prob / sum(prob)
    
    de_total = DensOp.mix(densop=de, prob=prob)

    holevo = de_total.entropy()
    for i in range(code_num):
        holevo -= prob[i]*de[i].entropy()

    # de_total.free()
    
    return holevo

def transmit(X,de,povm):

    samp_num = len(X)
    dim_X = len(de)
    dim_Y = len(povm)

    Y = np.array([0]*samp_num)
    
    prob_list = [None]*len(X)
    for i in range(samp_num):
        prob_list[i] = de[X[i]].probability(povm=povm)
        r = random.random()
        p = 0.0
        mes = dim_Y - 1
        for k in range(dim_Y-1):
            p += prob_list[i][k]
            if r < p:
                mes = k
                break
        Y[i] = mes
        
    return Y

def make_densop(basis):

    qs = [QState(vector=b) for b in basis]
    de = [DensOp(qstate=[q], prob=[1.0]) for q in qs]

    # for n in range(len(qs)):
    #     qs[n].free()
    
    return de
    
def make_povm(vec):

    return [np.outer(v,v.conjugate())/2.0 for v in vec]

def random_sample(code_num,samp_num):

    return np.array([random.randint(0,code_num-1) for _ in range(samp_num)])

if __name__ == '__main__':

    SQRT1      = cmath.sqrt(1/3)
    SQRT2      = cmath.sqrt(2/3)
    EXT2       = cmath.exp(2*cmath.pi*1j/3)
    EXT4       = cmath.exp(4*cmath.pi*1j/3)

    basis      = [np.array([1.0, 0.0]),
                  np.array([SQRT1, SQRT2]),
                  np.array([SQRT1, SQRT2*EXT2]),
                  np.array([SQRT1, SQRT2*EXT4])]
    
    basis_orth = [np.array([0.0, 1.0]),
                  np.array([SQRT2, -SQRT1]),
                  np.array([SQRT2, -SQRT1*EXT2]),
                  np.array([SQRT2, -SQRT1*EXT4])]

    de = make_densop(basis)

    code_num = 4
    samp_num = 100
    trial = 100

    povm_name  = ['#1','#2']
    povm_basis = [basis, basis_orth]
    
    for b in povm_basis:

        povm = make_povm(b)
    
        mutual = []
        holevo = []
        for _ in range(trial):
    
            X = random_sample(code_num,samp_num)
            Y = transmit(X, de, povm)

            mutual.append(classical_mutual_information(X,Y))
            holevo.append(holevo_quantity(X,de))

        df = pd.DataFrame({'holevo quantity':holevo,'mutual information':mutual})
        holevo_mean = df['holevo quantity'].mean()
        holevo_std  = df['holevo quantity'].std()
        mutual_mean = df['mutual information'].mean()
        mutual_std  = df['mutual information'].std()

        print("== povm: {:} ==".format(povm_name.pop(0)))
        print("[holevo quantity]")
        print("- mean = {0:.4f} (std = {1:.4f})".format(holevo_mean, holevo_std))
        print("[mutual information]")
        print("- mean = {0:.4f} (std = {1:.4f})".format(mutual_mean, mutual_std))
        print()
        
    # for n in range(len(de)):
    #     de[n].free()
