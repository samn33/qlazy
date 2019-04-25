import random
from qlazypy import QState

def main():

    print("== general rotation ==")

    alpha = random.uniform(0.0, 1.0)
    beta = random.uniform(0.0, 1.0)
    gamma = random.uniform(0.0, 1.0)

    print("(euler angle = {0:.4f}, {1:.4f}, {2:.4f})".format(alpha, beta, gamma))

    print("** one-way quantum computing")

    # graph state
    qc_oneway = QState(5)
    qc_oneway.h(1).h(2).h(3).h(4)
    qc_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4)

    # measurement
    alpha_oneway = alpha
    beta_oneway = beta
    gamma_oneway = gamma
    s0 = qc_oneway.m(id=[0], shots=1, angle=0.5, phase=0.0).lst
    if s0 == 1:
        alpha_oneway = -alpha_oneway
    s1 = qc_oneway.m(id=[1], shots=1, angle=0.5, phase=alpha_oneway).lst
    if s1 == 1:
        beta_oneway = -beta_oneway
    s2 = qc_oneway.m(id=[2], shots=1, angle=0.5, phase=beta_oneway).lst
    if(s0+s2)%2 == 1:
        gamma_oneway = -gamma_oneway
    s3 = qc_oneway.m(id=[3], shots=1, angle=0.5, phase=gamma_oneway).lst

    # result state
    qc_oneway.show(id=[4])

    print("** conventianal quantum gate")

    qc_gate = QState(1)
    qc_gate.rx(0, phase=alpha).rz(0, phase=beta).rx(0, phase=gamma)
    qc_gate.show()

    del qc_oneway
    del qc_gate
    
if __name__ == '__main__':
    main()
