import random
from qlazy import QState

def main():

    print("== general rotation ==")

    alpha = random.uniform(0.0, 1.0)
    beta = random.uniform(0.0, 1.0)
    gamma = random.uniform(0.0, 1.0)

    print("(euler angle = {0:.4f}, {1:.4f}, {2:.4f})".format(alpha, beta, gamma))

    print("** one-way quantum computing")

    # graph state
    qs_oneway = QState(5)
    qs_oneway.h(1).h(2).h(3).h(4)
    qs_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4)

    # measurement
    alpha_oneway = alpha
    beta_oneway = beta
    gamma_oneway = gamma
    s0 = qs_oneway.m([0], shots=1, angle=0.5, phase=0.0).lst
    if s0 == 1:
        alpha_oneway = -alpha_oneway
    s1 = qs_oneway.m([1], shots=1, angle=0.5, phase=alpha_oneway).lst
    if s1 == 1:
        beta_oneway = -beta_oneway
    s2 = qs_oneway.m([2], shots=1, angle=0.5, phase=beta_oneway).lst
    if(s0+s2)%2 == 1:
        gamma_oneway = -gamma_oneway
    s3 = qs_oneway.m([3], shots=1, angle=0.5, phase=gamma_oneway).lst

    # result state
    qs_oneway.show([4])

    print("** conventianal quantum gate")

    qs_gate = QState(1)
    qs_gate.rx(0, phase=alpha).rz(0, phase=beta).rx(0, phase=gamma)
    qs_gate.show()

    # qs_oneway.free()
    # qs_gate.free()
    
if __name__ == '__main__':
    main()
