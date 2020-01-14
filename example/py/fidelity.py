import numpy as np
from qlazypy import QState

if __name__ == '__main__':

    qs_0 = QState(2).h(0).h(1)
    qs_1 = QState(2)

    print("fidelity = {:.6f}".format(qs_0.fidelity(qs_0)))
    print("fidelity = {:.6f}".format(qs_0.fidelity(qs_1)))
