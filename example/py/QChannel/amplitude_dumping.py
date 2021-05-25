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

def make_kraus(gamma=0.0):

    transmit = math.sqrt(1.0-gamma)
    reflect = math.sqrt(gamma)
    
    kraus = []
    kraus.append(np.array([[1,0],[0,0]])+transmit*np.array([[0,0],[0,1]]))
    kraus.append(reflect*np.array([[0,1],[0,0]]))

    return kraus

def make_hamiltonian():

    return np.array([[0,0],[0,1]])
    
if __name__ == '__main__':

    print("== parameter ==")

    gamma = 0.5
    H = make_hamiltonian()
    print("gamma =", gamma)
    
    print("== initial density operator ==")
    
    u_1 = math.sqrt(1/3)
    u_2 = math.sqrt(1/3)
    u_3 = math.sqrt(1/3)
    D = make_densop_matrix(u_1,u_2,u_3)
    de = DensOp(matrix=D)

    de.show()
    print("square trace =",de.sqtrace())
    print("(u_1,u_2,u_3) = ({0:.3f},{1:.3f},{2:.3f})".format(u_1,u_2,u_3))
    print("expect value of energy =", de.expect(matrix=H))

    [M_0,M_1] = make_kraus(gamma=gamma)

    print("== finail density operator ==")

    de.instrument(kraus=[M_0,M_1])

    de.show()
    print("square trace =", de.sqtrace())
    (u_1,u_2,u_3) = get_coordinate(densop=de)
    print("(u_1,u_2,u_3) = ({0:.3f},{1:.3f},{2:.3f})".format(u_1,u_2,u_3))
    print("expect value of energy =", de.expect(matrix=H))

    de.free()
