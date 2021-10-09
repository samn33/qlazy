import random
from qlazy import QState

def main():

    a = random.uniform(0.0, 1.0)
    b = random.uniform(0.0, 1.0)
    phi = random.uniform(0.0, 1.0)
    print("a,b = {0:.4f}, {1:.4f}".format(a,b))
    print("phi = {0:.4f}".format(phi))

    print("** one-way quantum computing")

    # graph state
    qs_oneway = QState(2)
    qs_oneway.ry(0, phase=a).rz(0, phase=b)  # input state (random)
    qs_oneway.h(1)
    qs_oneway.cz(0,1)

    # measurement
    s = qs_oneway.m([0], shots=1, angle=0.5, phase=phi)

    # result state
    qs_oneway.show([1])

    print("** conventianal quantum gate")

    qs_gate = QState(1)
    qs_gate.ry(0, phase=a).rz(0, phase=b)  # input state (random)
    qs_gate.rz(0, phase=-phi).h(0)
    qs_gate.show()

if __name__ == '__main__':
    main()
