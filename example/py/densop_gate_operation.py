from qlazypy import QState,DensOp

if __name__ == '__main__':

    qs = QState(2)
    de = DensOp(qstate=[qs], prob=[1.0])

    de.h(0).cx(0,1).rx(1,phase=0.4).ry(0,phase=0.3).cx(1,0).cu2(0,1, alpha=0.6,beta=0.3)
    qs.h(0).cx(0,1).rx(1,phase=0.4).ry(0,phase=0.3).cx(1,0).cu2(0,1, alpha=0.6,beta=0.3)

    de2 = DensOp(qstate=[qs],prob=[1.0])

    print("* fidelity = {:.6f}".format(de.fidelity(de2)))
    print("* trace distance = {:.6f}".format(de.distance(de2)))
    
    qs.free()
    de.free()
    de2.free()
