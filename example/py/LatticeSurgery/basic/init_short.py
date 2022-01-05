from collections import Counter
import random

from qlazy import QState, PauliProduct
from qlazy.tools.Register import CreateRegister,InitRegister

class QStateLogical(QState):

    def set_register(self, dat, anc):

        self.__dat = dat
        self.__anc = anc
        self.__x_stab = [PauliProduct(pauli_str='XXX', qid=[dat[0], dat[1], dat[2]]),
                         PauliProduct(pauli_str='XXX', qid=[dat[2], dat[3], dat[4]])]
        self.__z_stab = [PauliProduct(pauli_str='ZZZ', qid=[dat[0], dat[2], dat[3]]),
                         PauliProduct(pauli_str='ZZZ', qid=[dat[1], dat[2], dat[4]])]
        self.__lx = PauliProduct(pauli_str='XX', qid=[dat[0], dat[3]])
        self.__lz = PauliProduct(pauli_str='ZZ', qid=[dat[0], dat[1]])
        
        return self

    def initialize(self, alpha=0.0, beta=0.0, gamma=0.0):

        self.reset()
        self.u3(self.__dat[0], alpha=alpha, beta=beta, gamma=gamma)
        self.cx(self.__dat[0], self.__dat[3])
        for i in range(len(self.__x_stab)):
            self.reset(qid=[self.__anc[0]])
            self.h(self.__anc[0])
            self.operate(ctrl=self.__anc[0], pp=self.__x_stab[i])
            self.h(self.__anc[0])
            self.m(qid=[self.__anc[0]])

        return self

    def Mx(self, shots=1):

        self.reset(qid=[self.__anc[0]])
        self.h(self.__anc[0])
        self.operate(ctrl=self.__anc[0], pp=self.__lx)
        self.h(self.__anc[0])
        return self.m(qid=[self.__anc[0]], shots=shots).frequency
    
    def Mz(self, shots=1):

        self.reset(qid=[self.__anc[0]])
        self.h(self.__anc[0])
        self.operate(ctrl=self.__anc[0], pp=self.__lz)
        self.h(self.__anc[0])
        return self.m(qid=[self.__anc[0]], shots=shots).frequency
    
if __name__ == '__main__':

    alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
    meas = random.choice(['X', 'Z'])
    shots = 10000

    print("- alpha, beta, gamma = ", alpha, beta, gamma)
    print("- measure {}".format(meas))
    print("- shots =", shots)
        
    dat = CreateRegister(5)
    anc = CreateRegister(1)
    qubit_num = InitRegister(dat, anc)
    qs_logical = QStateLogical(qubit_num).set_register(dat, anc).initialize(alpha, beta, gamma)

    qs = QState(qubit_num=1).u3(0, alpha=alpha, beta=beta, gamma=gamma)

    if meas == 'X':
        result_actual = qs_logical.Mx(shots=shots)
        result_expect = qs.mx(shots=shots).frequency
    elif meas == 'Z':
        result_actual = qs_logical.Mz(shots=shots)
        result_expect = qs.mz(shots=shots).frequency
        
    print("- actual =", result_actual)
    print("- expect =", result_expect)
