import math
import numpy as np
from qlazy import QState, DensOp

def make_povm(theta=0.0):

    s = math.sin(theta * math.pi)
    c = math.cos(theta * math.pi)
    f = 1.0/(1.0 + c)

    E0 = f * np.array([[s*s, -c*s], [-c*s, c*c]])
    E1 = f * np.array([[0, 0], [0, 1]])
    E2 = np.eye(2) - E0 - E1

    return (E0, E1, E2)

if __name__ == '__main__':

    theta = 0.4  # -0.5 <= theta <= 0.5
    print("prob. of success =", 1.0 - math.cos(theta * math.pi))
        
    qs = [QState(1), QState(1).ry(0,phase=theta*2.0)]
    de = [DensOp(qstate=[qs[0]], prob=[1.0]), DensOp(qstate=[qs[1]], prob=[1.0])]

    povm = make_povm(theta)
    
    print("theta = {0:}*PI".format(theta))
    print("     [0]   [1]   [?]")
    for i in range(2):
        prob = de[i].probability(povm=povm)
        print("[{0:}] {1:.3f} {2:.3f} {3:.3f}".format(i, prob[0],prob[1],prob[2]))
            
        de[i].free()
        qs[i].free()
