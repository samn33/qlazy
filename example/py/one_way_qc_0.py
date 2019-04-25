import random
from qlazypy import QState

def main():

    a = random.uniform(0.0, 1.0)
    b = random.uniform(0.0, 1.0)
    phi = random.uniform(0.0, 1.0)
    print("a,b = {0:.4f}, {1:.4f}".format(a,b))
    print("phi = {0:.4f}".format(phi))

    print("** one-way quantum computing")

    # graph state
    qc_oneway = QState(2)
    qc_oneway.ry(0, phase=a).rz(0, phase=b)  # input state (random)
    qc_oneway.h(1)
    qc_oneway.cz(0,1)

    # measurement
    s = qc_oneway.m(id=[0], shots=1, angle=0.5, phase=phi)

    # result state
    qc_oneway.show(id=[1])

    print("** conventianal quantum gate")

    qc_gate = QState(1)
    qc_gate.ry(0, phase=a).rz(0, phase=b)  # input state (random)
    qc_gate.rz(0, phase=-phi).h(0)
    qc_gate.show()

    del qc_oneway
    del qc_gate

if __name__ == '__main__':
    main()
