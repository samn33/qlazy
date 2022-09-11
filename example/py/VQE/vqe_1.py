import numpy as np
import scipy.optimize
from qlazy import MPState, Observable
from qlazy.Observable import X, Y, Z

#------------------------------------
#  functions
#------------------------------------

def ExpectVal(hm, mps):

    return mps.expect(observable=hm).real

def cost(phi):

    mps = MPState(2)

    mps.rx(0,phase=phi[0])
    mps.rz(0,phase=phi[1])
    mps.rx(1,phase=phi[2])
    mps.rz(1,phase=phi[3])
    mps.cx(1,0)
    mps.rz(1,phase=phi[4])
    mps.rx(1,phase=phi[5])

    exp = ExpectVal(M, mps)

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
