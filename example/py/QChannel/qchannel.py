import math
import numpy as np
from qlazy import DensOp

# Pauli Matrix

Sigma_0 = np.eye(2)
Sigma_1 = np.array([[0,1],[1,0]])
Sigma_2 = np.array([[0,-1j],[1j,0]])
Sigma_3 = np.array([[1,0],[0,-1]])

def get_coordinate(densop=None):

    u_1 = densop.expect(matrix=Sigma_1)
    u_2 = densop.expect(matrix=Sigma_2)
    u_3 = densop.expect(matrix=Sigma_3)

    return (u_1,u_2,u_3)
    
def make_densop_matrix(u_1,u_2,u_3):

    matrix = (Sigma_0+u_1*Sigma_1+u_2*Sigma_2+u_3*Sigma_3) / 2.0

    return matrix

if __name__ == '__main__':

    
    print("== parameter ==")
    prob = 0.1
    print("prob =", prob)
    
    u_1 = math.sqrt(1/3)
    u_2 = math.sqrt(1/3)
    u_3 = math.sqrt(1/3)
    D = make_densop_matrix(u_1,u_2,u_3)
    de = DensOp(matrix=D)

    print("== phase dump ==")
    #de.bit_flip(0, prob=prob)
    #de.phase_flip(0, prob=prob)
    #de.bit_phase_flip(0, prob=prob)
    #de.depolarize(0, prob=prob)
    #de.amp_dump(0, prob=prob)
    de.phase_dump(0, prob=prob)

    (u_1,u_2,u_3) = get_coordinate(densop=de)
    print("(u_1,u_2,u_3) = ({0:},{1:},{2:})".format(u_1,u_2,u_3))
