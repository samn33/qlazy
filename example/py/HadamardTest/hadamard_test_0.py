from qlazypy import QState

def hadamard_test_real():
    
    print("== expectaion value prediction (real part) == ")

    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(2)
    qs = qs_0.tenspro(qs_psi)

    # circuit for hadamard test

    qs.h(0)
    qs.ch(0,1).crx(0,2,phase=0.25)
    qs.h(0)

    shots = 1000
    md = qs.m(id=[0], shots=shots)
    p0 = md.frq[0]/shots
    p1 = md.frq[1]/shots
    exp_pred = p0-p1
    print("expectation value (predict) = {0:.3f}".format(exp_pred))

    # theoretical expactation value
    
    qs_op = qs_psi.clone()
    qs_op.h(0).rx(1,phase=0.25)
    exp_theo = qs_psi.inpro(qs_op).real
    print("expectation value (theoretical) = {0:.3f}".format(exp_theo))

    # free memory
    
    #qs_0.free()
    #qs_psi.free()
    #qs_op.free()
    #qs.free()
    
def hadamard_test_imag():
    
    print("== expectaion value prediction (imaginary part) == ")
    
    # prepare initial state

    qs_0 = QState(1)
    qs_psi = QState(2)
    qs = qs_0.tenspro(qs_psi)

    # circuit for hadamard test

    qs.h(0).s(0)
    qs.ch(0,1).crx(0,2,phase=0.25)
    qs.h(0)

    shots = 1000
    md = qs.m(id=[0], shots=shots)
    p0 = md.frq[0]/shots
    p1 = md.frq[1]/shots
    exp_pred = p0-p1
    print("expectation value (predict) = {0:.3f}".format(exp_pred))

    # theoretical expactation value
    
    qs_op = qs_psi.clone()
    qs_op.h(0).rx(1,phase=0.25)
    exp_theo = qs_psi.inpro(qs_op).imag
    print("expectation value (theoretical) = {0:.3f}".format(exp_theo))

    # free memory
    
    qs_0.free()
    qs_psi.free()
    qs_op.free()
    qs.free()

if __name__ == '__main__':
    
    hadamard_test_real()
    hadamard_test_imag()
