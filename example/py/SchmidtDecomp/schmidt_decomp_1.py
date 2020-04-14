import numpy as np
from scipy.stats import unitary_group
from qlazypy import QState

def generate_qstate(qid_0, qid_1, entangle=True): # random pure state (entangle or not)

    if entangle == True:
        dim = 2**len(qid_0+qid_1)
        vec = np.array([0.0]*dim)
        vec[0] = 1.0
        mat = unitary_group.rvs(dim)
        vec = np.dot(mat, vec)
        qs = QState(vector=vec)
    else:
        dim_0 = 2**len(qid_0)
        dim_1 = 2**len(qid_1)
        vec_0 = np.array([0.0]*dim_0)
        vec_1 = np.array([0.0]*dim_1)
        vec_0[0] = 1.0
        vec_1[0] = 1.0
        mat_0 = unitary_group.rvs(dim_0)
        mat_1 = unitary_group.rvs(dim_1)
        vec_0 = np.dot(mat_0, vec_0)
        vec_1 = np.dot(mat_1, vec_1)
        qs_0 = QState(vector=vec_0)
        qs_1 = QState(vector=vec_1)
        qs = qs_0.tenspro(qs_1)
        QState.free_all(qs_0, qs_1)
    return qs

if __name__ == '__main__':

    qid_0 = [0,1]
    qid_1 = [2,3,4]
    qs_ori = generate_qstate(qid_0, qid_1, entangle=True)

    print("qnum = ", len(qid_0+qid_1))
    print("qid_0 = ", qid_0)
    print("qid_1 = ", qid_1)

    # schmidt decomposition
    coef, qs_0, qs_1 = qs_ori.schmidt_decomp(qid_0=qid_0, qid_1=qid_1)
    rank = len(coef)
    print("schmidt coef = ", coef)
    print("schmidt coef = ", qs_ori.schmidt_coef(qid_0=qid_0, qid_1=qid_1))
    print("schmidt rank = ", len(coef))

    # reconstruction
    qs_list = [qs_0[i].tenspro(qs_1[i]) for i in range(rank)]
    vec_comp = np.zeros(qs_ori.state_num, dtype=np.complex)
    for i in range(rank):
        vec_comp = vec_comp + coef[i] * qs_list[i].get_amp()
    qs_comp = QState(vector=vec_comp)

    # evaluation
    print("fidelity = {:.6f}".format(qs_ori.fidelity(qs_comp))) # 1.000000
    
    QState.free_all(qs_ori, qs_0, qs_1, qs_comp)
