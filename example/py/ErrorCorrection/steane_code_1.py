import numpy as np
from qlazy import QState, DensOp

Hamming   = np.array([[0,1,1,1,1,0,0], [1,0,1,1,0,1,0], [1,1,0,1,0,0,1]])
Hamming_T = Hamming.T

Steane_0 = ['0000000', '1101001', '1011010', '0110011',
            '0111100', '1010101', '1100110', '0001111']
Steane_1 = ['1111111', '0010110', '0100101', '1001100',
            '1000011', '0101010', '0011001', '1110000']

class MyDensOp(DensOp):
    
    def noise(self, kind='', prob=0.0, qid=[]):

        print("== noise ({:}) ==".format(kind))
        print("- qubit = {:}".format(qid))
        print("- prob  = {:}".format(prob))
    
        qchannel = {'bit_flip':self.bit_flip, 'phase_flip':self.phase_flip,
                    'bit_phase_flip':self.bit_phase_flip,
                    'depolarize':self.depolarize, 'amp_dump':self.amp_dump,
                    'phase_dump':self.phase_dump}
        [qchannel[kind](i, prob=prob) for i in qid]
        return self

    def correct(self, kind, qid_C, qid_S):

        self.reset(qid=qid_S)

        if kind == 'phase_flip': [self.h(q) for q in qid_C]

        # syndrome
        for i, row in enumerate(Hamming):
            [self.cx(qid_C[j], qid_S[i]) if row[j] == 1 else False for j in range(len(row))]

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

    print("== quantum state (a |0L> + b |1L>) ==")
    print("- a = {:.4f}".format(a))
    print("- b = {:.4f}".format(b))

    qvec = np.full(2**len(qid_C), 0.+0.j)
    for s in Steane_0: qvec[int(s, 2)] = a
    for s in Steane_1: qvec[int(s, 2)] = b

    norm = np.linalg.norm(qvec)
    qvec = qvec / norm

    qs_C = QState(vector=qvec)
    qs_S = QState(len(qid_S))
    qs = qs_C.tenspro(qs_S)
    de_ini = MyDensOp(qstate=[qs])
    de_fin = de_ini.clone()

    # QState.free_all(qs_C, qs_S, qs)
    return de_ini, de_fin

if __name__ == '__main__':

    # set registers
    qid_C = MyDensOp.create_register(7) # registers for code space
    qid_S = MyDensOp.create_register(3) # registers for error syndrome
    MyDensOp.init_register(qid_C, qid_S)

    # generate initial quantum state (density operator)
    de_ini, de_fin = generate_qstate(qid_C, qid_S)

    # add noise
    de_fin.noise(kind='depolarize', qid=[qid_C[3]], prob=1.0)

    # error correction
    de_fin.correct('bit_flip', qid_C, qid_S)
    de_fin.correct('phase_flip', qid_C, qid_S)

    # print result
    print("== result ==")
    print("- fidelity = {:.6f}".format(de_fin.fidelity(de_ini, qid=qid_C)))
