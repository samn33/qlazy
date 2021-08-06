from qlazy import QState

def main():

    print("== convergence on engenstate ==")
    
    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(2).h(0).h(1)
    #qs_psi = QState(2).x(0).x(1).h(0).h(1)
    qs = qs_0.tenspro(qs_psi)

    # circuit for hadamard test

    iter = 100
    for _ in range(iter):
        qs.h(0)
        qs.ch(0,1).crx(0,2,phase=0.25)
        qs.h(0)
        qs.m([0],shots=1)

    print("- final |psi>")
    qs.show([1,2])
    print("- unitary operated |psi>")
    qs.h(1).rx(2,phase=0.25).show([1,2])

    # qs_0.free()
    # qs_psi.free()
    # qs.free()

if __name__ == '__main__':
    main()
