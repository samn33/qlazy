import math
from qlazypy import QState

def main():
    
    print("== phase prediction == ")

    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(1).x(0)
    qs = qs_0.tenspro(qs_psi)

    # circuit for hadamard test

    qs.h(0)
    qs.cp(0,1,phase=0.25)
    qs.h(0)

    shots = 1000
    md = qs.m(id=[0], shots=shots)
    p0_mes = md.frq[0]/shots
    p1_mes = md.frq[1]/shots
    print("p0,p1 (measured)    = {0:.3f},{1:.3f}".format(p0_mes,p1_mes))

    p0_theo = (1+math.cos(0.25*math.pi))/2
    p1_theo = (1-math.cos(0.25*math.pi))/2
    print("p0,p1 (theoretical) = {0:.3f},{1:.3f}".format(p0_theo,p1_theo))

    qs_0.free()
    qs_psi.free()
    qs.free()

if __name__ == '__main__':
    main()
