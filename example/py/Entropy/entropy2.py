import random
import math
import numpy as np
from scipy.stats import unitary_group
from collections import Counter
from qlazy import QState, DensOp

def random_qstate(qnum):  # random pure state

    dim = 2**qnum
    vec = np.array([0.0]*dim)
    vec[0] = 1.0
    mat = unitary_group.rvs(dim)
    vec = np.dot(mat, vec)
    qs = QState(vector=vec)

    return qs

def random_qstate_schmidt(qnum_A,qnum_B):  # random pure state (schmidt decomp.)

    dim_A = 2**qnum_A
    dim_B = 2**qnum_B
    dim_AB = dim_A*dim_B
    dim_min = min(dim_A,dim_B)

    coef = np.array([random.random() for _ in range(dim_min)])
    norm = math.sqrt(np.dot(coef,coef))
    coef = coef/norm

    vec = np.array([0.0]*dim_AB)
    for i in range(dim_min):
        idx = i + i*dim_B
        vec[idx] = coef[i]

    qs = QState(vector=vec)

    return qs

def entropy_from_qstate(qstate=None,id_A=[],id_B=[],shots=10):

    vec_samp = [str(list(qstate.get_amp(id_A))) for _ in range(shots)]
    freq = list(Counter(vec_samp).values())
    total = sum(freq)
    prob = [x/total for x in freq]

    ent = 0.0
    for p in prob:
        ent -= (p*np.log2(p))
        
    return ent
    
if __name__ == '__main__':

    qnum_A = 2
    qnum_B = 3

    id_A = list(range(qnum_A))
    id_B = [i+qnum_A for i in range(qnum_B)]

    ## simple random pure state
    #qs = random_qstate(qnum_A+qnum_B)

    # random pure state represented by schmidt decomposition
    qs = random_qstate_schmidt(qnum_A,qnum_B)

    # density operator for the pure state
    de = DensOp(qstate=[qs], prob=[1.0])

    ent = de.entropy()
    ent_A = de.entropy(id_A)
    ent_B = de.entropy(id_B)

    # 'ent_A' is equal to 'ent_B', if state for system A+B is pure state
    print("- entropy (system A+B):                S(A,B)  = {:.4f}".format(ent))
    print("- entanglement entropy (system A):     S(A)    = {:.4f}".format(ent_A))
    print("- entanglement entropy (system B):     S(B)    = {:.4f}".format(ent_B))
    
    ent_Q = entropy_from_qstate(qs,id_A,id_B,1000)

    # 'ent_Q' is equal to 'ent_A','ent_B',
    # if the pure state is represented by schmidt decomposition
    print("- entanglement entropy (predict of A): S(A)'   = {:.4f}".format(ent_Q))
    
    ent_cond = de.cond_entropy(id_A,id_B)
    mut_info = de.mutual_info(id_A,id_B)
    print("- conditional entropy:                 S(A|B)  = {:.4f}".format(ent_cond))
    print("- mutual information:                  I(A:B)  = {:.4f}".format(mut_info))

    if qnum_A == qnum_B:
        de_A = de.partial(id_A)
        de_B = de.partial(id_B)
        rel_ent = de_A.relative_entropy(de_B)
        print("- relative entropy:                    S(A||B) = {:.4f}".format(rel_ent))
        # de_A.free()
        # de_B.free()
    
    # qs.free()
    # de.free()
