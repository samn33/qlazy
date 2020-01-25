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
    vec_A = [random_vector(qubit_num) for _ in range(mixed_num)]
    qs_A = [QState(vector=vec_A[i]) for i in range(mixed_num)]

    # random density operator
    de_A = DensOp(qstate=qs_A, prob=prob_mixed)

    # free memory
    for i in range(mixed_num):
        qs_A[i].free()
    
    return de_A
    
def computational_basis(qubit_num):

    dim = 2**qubit_num
    basis = np.array([[1 if j==i else 0 for j in range(dim)] for i in range(dim)])

    return basis

def eigen_values_vectors(densop):

    matrix = densop.get_elm()
    eigvals, eigvecs = eigh(matrix, eigvals_only=False)
    #eigvecs = np.conjugate(eigvecs.T)
    eigvecs = eigvecs.T

    eigvals_list = [eigvals[i] for i in range(len(eigvals)) if abs(eigvals[i]) > MIN_DOUBLE]
    eigvecs_list = [eigvecs[i] for i in range(len(eigvecs)) if abs(eigvals[i]) > MIN_DOUBLE]
            
    eigvals = np.array(eigvals_list)
    eigvecs = np.array(eigvecs_list)

    return eigvals, eigvecs

def purification(de_A):

    # representation of the input state with orthogonal basis of system A
    coef,basis_A = eigen_values_vectors(de_A)
    rank = len(basis_A)

    # make computational basis of system R
    qnum_R = int(math.log2(rank))
    if 2**qnum_R != rank:
        qnum_R += 1
    basis_R = computational_basis(qnum_R)

    # orthogonal basis of system A+R
    basis_AR = [np.kron(basis_A[i],basis_R[i]) for i in range(rank)]

    # representation of the purified state with orthogonal basis of system A+R
    vec_AR = np.array([0]*len(basis_AR[0]))
    for i in range(rank):
        vec_AR = vec_AR + (math.sqrt(coef[i]) * basis_AR[i])

    qs_AR = QState(vector=vec_AR)
    de_AR = DensOp(qstate=[qs_AR], prob=[1.0])

    # free memory
    qs_AR.free()

    return de_AR

def difference(de_1, de_2):

    mat_1 = de_1.get_elm()
    mat_2 = de_2.get_elm()
    vec_1 = np.ndarray.flatten(mat_1)
    vec_2 = np.ndarray.flatten(mat_2)
    diff = np.linalg.norm(vec_1-vec_2)

    return diff

if __name__ == '__main__':

    qnum_A = 1
    mixed_num = 3
    
    print("=== system A (mixed state) ===")
    de_A = random_mixed_state(qnum_A, mixed_num)
    print("* density operator:")
    print(de_A)
    print("* square trace:", de_A.sqtrace())
    
    print("=== system A+R (pure state) ===")
    de_AR = purification(de_A)
    print("* square trace:", de_AR.sqtrace())

    print("=== system A (partial system of A+R) ===")
    de_AR_pat = de_AR.partial(id=list(range(qnum_A)))
    print("* density operator:")
    print(de_AR_pat)
    print("* square trace:", de_AR_pat.sqtrace())

    print("=== result ===")
    if difference(de_A, de_AR_pat) < MIN_DOUBLE:
        print("* OK!")
    else:
        print("* NG!")

    de_A.free()
    de_AR.free()
    de_AR_pat.free()
