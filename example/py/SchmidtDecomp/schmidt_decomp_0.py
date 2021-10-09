import random
import numpy as np
from scipy.stats import unitary_group
from scipy.linalg import eigh
from qlazy import QState, DensOp

MIN_DOUBLE = 0.000001

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
    random.shuffle(id)
    qubit_num_A = random.randint(1,qubit_num-1)
    qubit_num_B = qubit_num - qubit_num_A
    id_A = id[:qubit_num_A]
    id_B = id[qubit_num_A:]

    return id_A,id_B

def eigen_values(densop):

    matrix = densop.get_elm()
    eigvals = eigh(matrix, eigvals_only=True)
    eigvals_out = [eigvals[i] for i in range(len(eigvals)) if eigvals[i] > MIN_DOUBLE]

    return eigvals_out
    
if __name__ == '__main__':

    # whole quantum state
    qubit_num = 5
    qs = random_qstate(qubit_num)
    de = DensOp(qstate=[qs], prob=[1.0])  # pure state

    # partial density operators (system A and B)
    id_A, id_B = random_qubit_id(qubit_num)
    de_A = de.patrace(id_B)
    de_B = de.patrace(id_A)

    # eigen-values of density operators (system A and B)
    eval_A = eigen_values(de_A)
    eval_B = eigen_values(de_B)

    print("== system A ==")
    print("- qubit id =", id_A)
    print("- square trace = ", de_A.sqtrace())
    print("- eigen values =", eval_A)
    print("- rank =", len(eval_A))

    print("== system B ==")
    print("- qubit id =", id_B)
    print("- square trace = ", de_B.sqtrace())
    print("- eigen values =", eval_B)
    print("- rank =", len(eval_B))
