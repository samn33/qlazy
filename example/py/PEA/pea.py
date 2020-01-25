from qlazypy import QState

def iqft(self,id=None):

    dim = len(id)
    iid = id[::-1]
    
    for i in range(dim):
        phase = -1.0/2**i
        for j in range(i):
            self.cp(iid[j],iid[i],phase=phase)
            phase *= 2.0
        self.h(iid[i])
        
    return self

def c_unitary(self,id=None):  # id[0] = controll qubit id

    self.cp(id[0],id[1],phase=0.5).cp(id[0],id[2],phase=0.25)
    return self

def eigen_state_ctr(psi_dim):

    # initial |psi> and controll qubit
    qs = QState(psi_dim+1)
    for i in range(psi_dim):
        qs.h(i)

    # hadamard test iteratively
    id = [psi_dim] + list(range(psi_dim))
    iter = 100
    for _ in range(iter):
        qs.h(psi_dim).c_unitary(id).h(psi_dim).m(id=[2],shots=1)

    print("== eigen state (convergence) ==")
    id = list(range(psi_dim))
    qs.show(id)

    return qs

def main():

    # add methods
    QState.iqft = iqft
    QState.c_unitary = c_unitary

    # prepare initial state
    sub_dim = 3  # order of precision
    psi_dim = 2  # qubit number for |psi> (must be qubit number for the unitary)
    qs_sub = QState(sub_dim)
    qs_psi_ctr = eigen_state_ctr(psi_dim)  # estimate the eigen state of the unitary
    qs_total = qs_sub.tenspro(qs_psi_ctr)

    # qubit id list (for the following steps)
    psi_qid = list(range(sub_dim,sub_dim+psi_dim))
    sub_qid = list(range(sub_dim))

    # hadamard operation to sub-qubits
    for i in range(sub_dim):
        qs_total.h(i)

    # c-unitary operation to the eigen state:|psi> iteratively
    for i in range(sub_dim):
        times = 2**i
        for _ in range(times):
            id = [i] + psi_qid  # qubit id list for eigen state:|psi>
            qs_total.c_unitary(id)
            
    # inverse QFT
    qs_total.iqft(sub_qid)

    # show final quantum state
    print("== final quantum state ==")
    qs_total.show(sub_qid)

    # mesurement
    print("== result of measurement ==")
    md = qs_total.m(sub_qid)
    md.show()

    # phase estimation
    print("== phase estimation ==")
    print(2*md.lst/md.state_num,"* PI")

    # free memory
    qs_sub.free()
    qs_psi_ctr.free()
    qs_total.free()

if __name__ == '__main__':
    main()
