import numpy as np
import scipy.optimize
from qlazy import Backend, ParametricQCirc
from qlazy.Observable import X, Y, Z

#------------------------------------
#  functions
#------------------------------------

def cost(phi):

    qc.set_params(params={'0': phi[0], '1': phi[1], '2': phi[2], '3': phi[3], '4': phi[4], '5': phi[5]})
    result = bk.run(qcirc=qc, out_state=True)
    exp = result.qstate.expect(observable=M).real
    return exp
    
def callback(phi):

    print("energy = ", cost(phi))

#------------------------------------
#  main
#------------------------------------

# Hamiltonian
M = (-3.8503 - 0.2288*X(1) - 1.0466*Z(1) - 0.2288*X(0) + 0.2613*X(0)*X(1) + 0.2288*X(0)*Z(1)
     - 1.0466*Z(0) + 0.2288*Z(0)*X(1) + 0.2356*Z(0)*Z(1)) / 2.0

# Backend
bk = Backend(product='qlazy', device='qstate_simulator')

# Parametric quantum circuit
qc = ParametricQCirc()
qc.rx(0, tag='0').rz(0, tag='1').rx(1, tag='2').rz(1, tag='3').cx(1,0).rz(1, tag='4').rx(1, tag='5')

# VQE
init = np.random.rand(6)
callback(init)
res = scipy.optimize.minimize(cost, init, method='Powell', callback=callback)
