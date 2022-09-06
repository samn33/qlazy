import numpy as np
import scipy.optimize
from qlazy import QState, Observable
from qlazy.Observable import X, Y, Z

#------------------------------------
#  functions
#------------------------------------

def ExpectVal(hm,qs):

    return qs.expect(observable=hm).real

def cost(phi):

    qs = QState(2)

    qs.rx(0,phase=phi[0])
    qs.rz(0,phase=phi[1])
    qs.rx(1,phase=phi[2])
    qs.rz(1,phase=phi[3])
    qs.cx(1,0)
    qs.rz(1,phase=phi[4])
    qs.rx(1,phase=phi[5])

    exp = ExpectVal(M, qs)

    return exp
    
def callback(phi):

    print("energy = ", cost(phi))

#------------------------------------
#  main
#------------------------------------

# set Hamiltonian

M = (-3.8503 - 0.2288*X(1) - 1.0466*Z(1) - 0.2288*X(0) + 0.2613*X(0)*X(1) + 0.2288*X(0)*Z(1)
     - 1.0466*Z(0) + 0.2288*Z(0)*X(1) + 0.2356*Z(0)*Z(1)) / 2.0

# VQE

init = np.random.rand(6)
callback(init)
res = scipy.optimize.minimize(cost, init,
                              method='Powell', callback=callback)
