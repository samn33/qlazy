import random
from qlazypy import QState

def main():

    print("== hadamard gate ==")

    print("** one-way quantum computing")

    # graph state
    qc_oneway = QState(5)
    qc_oneway.h(1).h(2).h(3).h(4)
    qc_oneway.cz(0,1).cz(1,2).cz(2,3).cz(3,4)

    # measurement
    qc_oneway.m(id=[0], shots=1, angle=0.5, phase=0.0)
    qc_oneway.m(id=[1], shots=1, angle=0.5, phase=0.5)
    qc_oneway.m(id=[2], shots=1, angle=0.5, phase=0.5)
    qc_oneway.m(id=[3], shots=1, angle=0.5, phase=0.5)

    # result state
    qc_oneway.show(id=[4])

    print("** conventianal quantum gate")

    qc_gate = QState(1)
    qc_gate.h(0)
    qc_gate.show()

    del qc_oneway
    del qc_gate
    
if __name__ == '__main__':
    main()
