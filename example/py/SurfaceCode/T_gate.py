import random
from qlazy import QState

def main():

    # parameters for generating random state: |psi>
    alpha, beta, gamma = random.random(), random.random(), random.random()
    
    # reference state: T|psi>
    qs_expect = QState(1)
    qs_expect.u3(0, alpha=alpha, beta=beta, gamma=gamma).t(0)

    # prepare initial state
    qs = QState(3)
    qs.h(0).s(0)  # |Y>
    qs.h(1).t(1)  # |A>
    qs.u3(2, alpha=alpha, beta=beta, gamma=gamma)  # |psi>

    # T gate (only with X,Z,H,CNOT and measurement)
    qs.cx(1,2)
    mval = qs.m(qid=[2]).last
    if mval == '1':
        qs.cx(1,0).h(0).cx(1,0).h(0)
        qs.x(1).z(1)
    qs_actual = qs.partial(qid=[1])

    # show the result
    print("== expect ==")
    qs_expect.show()
    print("== actual ==")
    qs_actual.show()
    print("== fidelity ==")
    print("{:.6f}".format(qs_actual.fidelity(qs_expect)))

    # QState.free_all(qs, qs_expect, qs_actual)

if __name__ == '__main__':

    main()
