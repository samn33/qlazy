import random
import math
import numpy as np
from scipy.stats import unitary_group
from qlazypy import QState,DensOp

def random_qstate_ensemble(qubit_num, mimxed_num):

    qstate = []
    dim = 2**qubit_num
    for _ in range(mixed_num):
        vec_ini = np.zeros(dim)
        vec_ini[0] = 1.0
        mat = unitary_group.rvs(dim)
        vec = np.dot(mat, vec_ini)
        qstate.append(QState(vector=vec))
        
    prob = [random.random() for _ in range(mixed_num)]
    total = sum(prob)
    prob = [p/total for p in prob]

    return (qstate,prob)

def get_pauli_index(index, total):
    # ex) index = 9 = 1001 -> [10,01] -> [2,1] --reverse-> [1,2] = pauli_index
    #     '1' means X for 0th-qubit, '2' means Y for 1st-qubit

    pauli_index = [0]*int(math.log2(total)/2)
    count = 0
    while index > 0:
        pauli_index[count] = index%4
        index = index // 4
        count += 1
    pauli_index.reverse()

    return pauli_index

def make_pauli_product(index, total, pauli_mat):

    pauli_index = get_pauli_index(index, total)
    pauli_prod_dim = 2**len(pauli_index) 
    pauli_prod = np.array([1.0])
    for pid in pauli_index:
        pauli_prod = np.kron(pauli_prod, pauli_mat[pid])

    return pauli_prod
    
def make_densop(expect, qubit_num, pauli_mat):

    dim = 2**qubit_num
    measure_num = len(expect)
    matrix = np.zeros((dim,dim))
    for i in range(measure_num):
        pauli_prod = make_pauli_product(i,measure_num,pauli_mat)
        matrix = matrix + expect[i] * pauli_prod
    matrix = matrix / (2.0**qubit_num)
    
    return DensOp(matrix=matrix)

def calc_expect(prb):

    N = len(prb)
    val = np.zeros(N)
    for index in range(N):
        bin_list = [int(s) for s in list(format(index, 'b'))]
        val[index] = (-1)**sum(bin_list)  # odd -> -1, even -> +1

    return np.dot(prb, val)

def estimate_densop(prob,qstate,shots):

    pauli_mat = [np.eye(2),                   # = I
                 np.array([[0,1],[1,0]]),     # = X
                 np.array([[0,-1j],[1j,0]]),  # = Y
                 np.array([[1,0],[0,-1]])]    # = Z
    
    mixed_num = len(prob)
    qubit_num = qstate[0].qubit_num
    measure_num = 4**qubit_num

    for i in range(mixed_num):

        expect = {}
        for index in range(measure_num):

            pauli_index = get_pauli_index(index,measure_num)

            if index == 0:
                expect[index] = 1.0
                continue
                    
            qs = qstate[i].clone()

            for qid in range(len(pauli_index)):

                if pauli_index[qid] == 0:
                    continue
                elif pauli_index[qid] == 1:
                    qs.h(qid)
                elif pauli_index[qid] == 2:
                    qs.s_dg(qid).h(qid)
                else:
                    pass

            frq = qs.m(shots=shots).frq
            prb = np.array([f/shots for f in frq])
            expect[index] = calc_expect(prb)

            qs.free()

        de_tmp = make_densop(expect, qubit_num, pauli_mat)
        
        if i == 0:
            de_tmp.mul(prob[i])
            densop_est = de_tmp.clone()
        else:
            de_tmp.mul(prob[i])
            densop_est.add(de_tmp)

    de_tmp.free()

    return densop_est
    
if __name__ == '__main__':

    # settings
    qubit_num = 1
    mixed_num = 2
    shots = 100

    # quantum state ensemble (original)
    qstate, prob = random_qstate_ensemble(qubit_num, mixed_num)

    # density operator (original)
    densop_ori = DensOp(qstate=qstate, prob=prob)

    # density operator estimation only from quantum state ensemble
    # (quantum state tomography)
    densop_est = estimate_densop(prob,qstate,shots)

    print("** density operator (original)")
    densop_ori.show()
    print("** density operator (estimated)")
    densop_est.show()
    print("** fidelity =",densop_ori.fidelity(densop_est))

    for q in qstate:
        q.free()
    densop_ori.free()
    densop_est.free()
