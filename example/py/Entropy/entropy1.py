import numpy as np
from scipy.stats import unitary_group
from qlazypy import QState, DensOp

def random_qstate(qnum):  # random pure state

    dim = 2**qnum
    vec = np.array([0.0]*dim)
    vec[0] = 1.0
    mat = unitary_group.rvs(dim)
    vec = np.dot(mat, vec)
    qs = QState(vector=vec)

    return qs

if __name__ == '__main__':

    qnum_A = 2
    qnum_B = 2

    id_A = list(range(qnum_A))
    id_B = [i+qnum_A for i in range(qnum_B)]

    qs = random_qstate(qnum_A+qnum_B)
    de = DensOp(qstate=[qs], prob=[1.0])

    ent = de.entropy()
    ent_A = de.entropy(id_A)
    ent_B = de.entropy(id_B)

    print("** S(A,B)  = {:.4f}".format(ent))
    print("** S(A)    = {:.4f}".format(ent_A))
    print("** S(B)    = {:.4f}".format(ent_B))

    qs.free()
    de.free()
