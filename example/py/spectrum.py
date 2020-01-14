import random
import math
import numpy as np
from scipy.stats import unitary_group
from scipy.linalg import eigh
from qlazypy import QState, DensOp

MIN_DOUBLE = 0.000001

def random_vector(qubit_num):

    dim = 2**qubit_num
    vec_ini = np.array([0.0]*dim)
    vec_ini[0] = 1.0
    mat = unitary_group.rvs(dim)
    vec = np.dot(mat, vec_ini)

    return vec

def random_mixed_state(qubit_num, mixed_num):

    # random probabilities
    r = [random.random() for _ in range(mixed_num)]
    s = sum(r)
    prob_mixed = [r[i]/s for i in range(mixed_num)]

    # random quantum states
    vecs = [random_vector(qubit_num) for _ in range(mixed_num)]
    qstate = [QState(vector=vecs[i]) for i in range(mixed_num)]

    # random density operator
    de = DensOp(qstate=qstate, prob=prob_mixed)

    # free memory
    for i in range(len(qstate)):
        qstate[i].free()
    
    return de

if __name__ == '__main__':

    qubit_num = 2
    mixed_num = 5

    de_ini = random_mixed_state(qubit_num, mixed_num)
    qstate,prob = de_ini.spectrum()
    de_fin = DensOp(qstate=qstate, prob=prob)
    dis = de_ini.distance(de_fin)

    print("* densop(ini) =\n",de_ini)
    print("* densop(fin) =\n",de_fin)
    print("* trace distance = ", dis)
    if abs(dis) < MIN_DOUBLE:
        print("OK!")
    else:
        print("NG!")

    de_ini.free()
    for i in range(len(qstate)):
        qstate[i].free()
