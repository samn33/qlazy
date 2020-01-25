import math
import numpy as np
from qlazypy import QState

def get_unitary():

    theta = math.pi / 8
    cos = math.cos(theta)
    sin = math.sin(theta)
    sqrt2 = math.sqrt(2.0)

    hadam = np.array([[1,1], [1,-1]]) / sqrt2
    rot_x = np.array([[cos, -sin*1.0j], [-sin*1.0j, cos]])
    ident = np.eye(2)

    uni_h = np.kron(hadam, ident)
    uni_r = np.kron(ident, rot_x)
    unitary = np.dot(uni_r, uni_h)

    return unitary

def get_ctr_unitary(unitary):

    ident = np.eye(4)
    proj_0 = np.array([[1+0j,0+0j],[0+0j,0+0j]])
    proj_1 = np.array([[0+0j,0+0j],[0+0j,1+0j]])
    c_unitary = np.kron(proj_0, ident) + np.kron(proj_1, unitary)

    return c_unitary
    
def main():

    unitary = get_unitary()
    c_unitary = get_ctr_unitary(unitary)
    
    print("== convergence on engenstate ==")
    
    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(2).h(0).h(1)
    qs = qs_0.tenspro(qs_psi)
    
    qs_psi.free()  # for reset control register

    # circuit for hadamard test

    iter = 100
    for _ in range(iter):
        qs.h(0)
        qs.ch(0,1).crx(0,2,phase=0.25)
        #qs.apply(matrix=c_unitary)
        qs.h(0)
        qs.m(id=[0],shots=1)

        # reset control register
        qs_psi = qs.partial(id=[1,2])
        qs.free()
        qs = qs_0.tenspro(qs_psi)
        qs_psi.free()

    print("- final |psi>")
    qs.show()
    print("- unitary operated |psi>")
    qs.h(1).rx(2,phase=0.25).show(id=[0,1,2])
    #qs.apply(matrix=unitary,id=[1,2]).show(id=[0,1,2])

    qs_0.free()

if __name__ == '__main__':
    main()
