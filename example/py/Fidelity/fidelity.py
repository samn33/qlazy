import random
import numpy as np
from scipy.stats import unitary_group
from qlazy import QState, DensOp

def random_densop(qnum_tar,qnum_ref,qnum_env):

    dim_pur = 2**(qnum_tar+qnum_ref)
    vec_pur = np.array([0.0]*dim_pur)
    vec_pur[0] = 1.0
    mat_pur = unitary_group.rvs(dim_pur)
    vec_pur = np.dot(mat_pur, vec_pur)

    dim_env = 2**qnum_env
    vec_env = np.array([0.0]*dim_env)
    vec_env[0] = 1.0

    vec_whole = np.kron(vec_pur,vec_env)

    qs = QState(vector=vec_whole)
    de = DensOp(qstate=[qs],prob=[1.0])

    # qs.free()
    return de

def random_unitary(qnum):

    dim = 2**qnum
    mat = unitary_group.rvs(dim)
    
    return mat
    
if __name__ == '__main__':

    # settings
    qnum_tar = 2  # system A : target system
    qnum_ref = 2  # system R : reference system
    qnum_env = 2  # system E : environment system
    qnum_whole = qnum_tar + qnum_ref + qnum_env

    # two random states in system A+R+E (A+R:set randomly, E:set |0> initialy)
    de1_whole = random_densop(qnum_tar,qnum_ref,qnum_env)
    de2_whole = random_densop(qnum_tar,qnum_ref,qnum_env)

    # two states in system A (trace out R+E)
    de1_ini = de1_whole.partial(list(range(qnum_tar)))
    de2_ini = de2_whole.partial(list(range(qnum_tar)))

    # fidelity for initial states
    fid_ini = de1_ini.fidelity(de2_ini)

    # unitary transformation for whole system
    U = random_unitary(qnum_whole)
    de1_whole.apply(U)
    de2_whole.apply(U)

    # two states in system A (trace out R+E)
    de1_fin = de1_whole.partial(list(range(qnum_tar)))
    de2_fin = de2_whole.partial(list(range(qnum_tar)))
    
    # fidelity for final states
    fid_fin = de1_fin.fidelity(de2_fin)

    # result
    print("* fidelity(ini) =", fid_ini)
    print("* fidelity(fin) =", fid_fin)

    if fid_ini <= fid_fin:
        print("OK!")
    else:
        print("NG!")

    # free memory
    # de1_whole.free()
    # de2_whole.free()
    # de1_ini.free()
    # de2_ini.free()
    # de1_fin.free()
    # de2_fin.free()
