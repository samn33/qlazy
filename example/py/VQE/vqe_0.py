import numpy as np
import scipy.optimize
from qlazy import QState,Observable

#------------------------------------
#  functions
#------------------------------------

def set_hamiltonian_str():

    s = "{}".format(-3.8503/2)
    s += "-{}*x_1".format(0.2288/2)
    s += "-{}*z_1".format(1.0466/2)
    s += "-{}*x_0".format(0.2288/2)
    s += "+{}*x_0*x_1".format(0.2613/2)
    s += "+{}*x_0*z_1".format(0.2288/2)
    s += "-{}*z_0".format(1.0466/2)
    s += "+{}*z_0*x_1".format(0.2288/2)
    s += "+{}*z_0*z_1".format(0.2356/2)

    return s

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

    # qs.free()

    return exp
    
def callback(phi):

    print("energy = ", cost(phi))

#------------------------------------
#  main
#------------------------------------

# set Hamiltonian

M_str = set_hamiltonian_str()
M = Observable(M_str)

# VQE

init = np.random.rand(6)
callback(init)
res = scipy.optimize.minimize(cost, init,
                              method='Powell', callback=callback)
