import numpy as np
from qlazypy import QState,DensOp

if __name__ == '__main__':

    print("== composite of quantum states ==")
    qs_ori = QState(3).h(0).h(1).h(2)
    qs = QState(1).h(0)
    qs_com = qs.composite(3)
    print("fidelity of the 2 quantum states = {:.6f}".format(qs_ori.fidelity(qs_com)))

    print("== composite of density operators ==")
    mat_1 = np.array([[0.75,0.25],[0.25,0.25]])
    mat_2 = np.kron(mat_1,mat_1)
    mat_3 = np.kron(mat_1,mat_2)
    de_ori = DensOp(matrix=mat_3)
    de = DensOp(matrix=mat_1)
    de_com = de.composite(3)
    print("fidelity of the 2 density operators = {:.6f}".format(de_ori.fidelity(de_com)))
