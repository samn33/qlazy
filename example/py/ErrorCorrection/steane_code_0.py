import numpy as np
from qlazy import QState

Hamming   = np.array([[0,1,1,1,1,0,0], [1,0,1,1,0,1,0], [1,1,0,1,0,0,1]])
Hamming_T = Hamming.T

Steane_0 = ['0000000', '1101001', '1011010', '0110011',
            '0111100', '1010101', '1100110', '0001111']
Steane_1 = ['1111111', '0010110', '0100101', '1001100',
            '1000011', '0101010', '0011001', '1110000']

class MyQState(QState):
    
    def noise(self, qid):

        i = np.random.randint(len(qid))
        alpha, beta, gamma = np.random.rand(3)
        self.rz(qid[i], phase=alpha).rx(qid[i], phase=beta).rz(qid[i], phase=gamma)
    
        print("== random noise ==")
        print("- qubit id = #{0:}".format(i, alpha, beta, gamma))
        print("- parameter of rotation = {0:.4f},{1:.4f},{2:.4f}".format(alpha, beta, gamma))

        return self

    def correct(self, kind, qid_C, qid_S):

        self.reset(qid=qid_S)

        if kind == 'phase_flip': [self.h(q) for q in qid_C]

        # syndrome
        for i, row in enumerate(Hamming):
            [self.cx(qid_C[j], qid_S[i]) if row[j] == 1 else False for j in range(len(row))]
            #[self.cx(qid_C[j], qid_S[i], cond=(row[j] == 1)) for j in range(len(row))]

        # correction
        for i, row in enumerate(Hamming_T):
            [self.x(qid_S[j]) if row[j] == 0 else False for j in range(len(row))]
            self.mcx(qid=qid_S+[qid_C[i]])
            [self.x(qid_S[j]) if row[j] == 0 else False for j in range(len(row))]
    
        if kind == 'phase_flip': [self.h(q) for q in qid_C]
        
        return self
    
def generate_qstate(qid_C, qid_S):

    a = np.random.rand() + np.random.rand() * 1.j
    b = np.random.rand() + np.random.rand() * 1.j

    qvec = np.full(2**len(qid_C), 0.+0.j)
    for s in Steane_0: qvec[int(s, 2)] = a
    for s in Steane_1: qvec[int(s, 2)] = b

    norm = np.linalg.norm(qvec)
    qvec = qvec / norm

    qs_C = MyQState(vector=qvec)
    qs_S = MyQState(len(qid_S))
    qs_ini = qs_C.tenspro(qs_S)
    qs_fin = qs_ini.clone()

    print("== random state (a |0L> + b |1L>) ==")
    print("- a = {:.4f}".format(a))
    print("- b = {:.4f}".format(b))

    # QState.free_all(qs_C, qs_S)
    return qs_ini, qs_fin

if __name__ == '__main__':

    # set registers
    qid_C = QState.create_register(7) # registers for code space
    qid_S = QState.create_register(3) # registers for error syndrome
    QState.init_register(qid_C, qid_S)

    # generate initial quantum state
    qs_ini, qs_fin = generate_qstate(qid_C, qid_S)

    # add noise
    qs_fin.noise(qid_C)

    # error correction
    qs_fin.correct('bit_flip', qid_C, qid_S)
    qs_fin.correct('phase_flip', qid_C, qid_S)

    # print result
    print("== result ==")
    print("- fidelity = {:.6f}".format(qs_fin.fidelity(qs_ini, qid=qid_C)))
