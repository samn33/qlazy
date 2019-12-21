import random
from scipy.stats import unitary_group
import numpy as np
from qlazypy import QState,DensOp

import sys

def random_qstate(qubit_num):

    dim = 2**qubit_num
    vec_ini = np.array([0.0]*dim)
    vec_ini[0] = 1.0
    mat = unitary_group.rvs(dim)
    vec = np.dot(mat, vec_ini)
    qs = QState(vector=vec)

    return qs

def random_qubit_id(qubit_num):

    id = list(range(qubit_num))
    #random.shuffle(id)
    qubit_num_A = random.randint(1,qubit_num-1)
    qubit_num_B = qubit_num - qubit_num_A
    id_A = id[:qubit_num_A]
    id_B = id[qubit_num_A:]

    return id_A,id_B

if __name__ == '__main__':

    qubit_num = 5
    id_A, id_B = random_qubit_id(qubit_num)
    qnum_A = len(id_A)
    qnum_B = len(id_B)

    # random state in system A
    qs_A = [random_qstate(qnum_A),random_qstate(qnum_A)]
    pr_A = [0.2,0.8] 
    de_A = DensOp(qstate=qs_A, prob=pr_A)

    # random state in system B
    qs_B = [random_qstate(qnum_B),random_qstate(qnum_B)]
    pr_B = [0.7,0.3] 
    de_B = DensOp(qstate=qs_B, prob=pr_B)

    # tensor product A and B
    de = de_A.tenspro(de_B)

    # system A and B
    de_AA = de.partial(id=id_A)
    de_BB = de.partial(id=id_B)

    print("* system A = {0:}, system B = {1:}".format(id_A, id_B))
    print("* trace distance (system A) = {:.6f}".format(de_A.distance(de_AA)))
    print("* trace distance (system B) = {:.6f}".format(de_B.distance(de_BB)))

    for q in qs_A:
        q.free()
    for q in qs_B:
        q.free()
    de_A.free()
    de_AA.free()
    de_B.free()
    de_BB.free()
    de.free()
