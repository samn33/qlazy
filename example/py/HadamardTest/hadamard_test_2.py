import math
from qlazy import QState

def main():
    
    print("== phase prediction == ")

    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(1).h(0)
    qs = qs_0.tenspro(qs_psi)

    # circuit for hadamard test

    qs.h(0)
    qs.crx(0,1,phase=0.5)
    qs.h(0)

    shots = 1000
    md = qs.m([0], shots=shots)
    p0 = md.frq[0]/shots
    p1 = md.frq[1]/shots
    print("[predicted]   cos(gamma) = {0:.3f}".format(p0-p1))

    print("[theoretical] cos(gamma) = {0:.3f}".format(math.cos(-0.25*math.pi)))

if __name__ == '__main__':
    main()
