from qlazypy import QState

if __name__ == '__main__':

    print("== U1,U2,U3 ==")
    qs = QState(1)
    qs.h(0)
    qs.u1(0, alpha=0.1)
    qs.u2(0, alpha=0.2, beta=0.3)
    qs.u3(0, alpha=0.3, beta=0.4, gamma=0.5)
    qs.show()

    print("== controlled U1,U2,U3 ==")
    qs_ctr = QState(2)
    qs_ctr.x(0)
    qs_ctr.h(1)
    qs_ctr.cu1(0, 1, alpha=0.1)
    qs_ctr.cu2(0, 1, alpha=0.2, beta=0.3)
    qs_ctr.cu3(0, 1, alpha=0.3, beta=0.4, gamma=0.5)
    qs_ctr.show(id=[1])
    
    qs.free()
    qs_ctr.free()
