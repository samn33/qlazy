import numpy as np
from qlazy import QState,DensOp

PERM = {'0000':'0000', '0001':'0001', '0010':'0010', '0100':'0011',
        '1000':'0100', '0011':'0101', '0101':'0110', '0110':'0111', 
        '1001':'1000', '1010':'1001', '1100':'1010', '0111':'1011',
        '1011':'1100', '1101':'1101', '1110':'1110', '1111':'1111'}

def perm_matrix(PERM):

    dim = len(PERM)
    perm_mat = np.zeros((dim,dim))
    iperm_mat = np.zeros((dim,dim))

    for k,v in PERM.items():
        col = int(k,2)
        row = int(v,2)
        perm_mat[row][col] = 1
        iperm_mat[col][row] = 1

    return (perm_mat, iperm_mat)

def create_densop():

    mat_1 = np.array([[0.75,0.25],[0.25,0.25]])
    de_1 = DensOp(matrix=mat_1)
    de_ini = de_1.composite(num=4)
    de_1.free()

    return de_ini

def coder(de_ini, id_all, id_comp, theta, perm_mat):

    de_tmp = de_ini.clone()
    [de_tmp.ry(i, phase=-theta) for i in id_all]
    de_tmp.apply(perm_mat)
    de_comp = de_tmp.partial(id_comp)  # 4-qubit -> 3-qubit state
    de_tmp.free()

    return de_comp

def decoder(de_comp, id_all, theta, iperm_mat):

    qs_0 = QState(1)
    de_0 = DensOp(qstate=[qs_0])
    de_fin = de_0.tenspro(de_comp)  # add 1-qubit (|0>)
    de_fin.apply(iperm_mat)
    [de_fin.ry(i, phase=theta) for i in id_all]

    qs_0.free()
    de_0.free()

    return de_fin
    
if __name__ == '__main__':

    # settings
    id_all = [0,1,2,3]
    id_comp = [1,2,3]
    theta = 0.25
    (perm_mat,iperm_mat) = perm_matrix(PERM)

    # initial state (4-qubit state)
    de_ini = create_densop()

    # coding (4-qubit -> 3-qubit state)
    de_comp = coder(de_ini, id_all, id_comp, theta, perm_mat)

    # decoding (3-qubit -> 4-qubit state)
    de_fin = decoder(de_comp, id_all, theta, iperm_mat)

    # fidelity
    print("fidelity = {:.6f}".format(de_fin.fidelity(de_ini)))

    de_ini.free()
    de_comp.free()
    de_fin.free()
