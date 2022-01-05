from collections import Counter
import random

from qlazy import QState, PauliProduct
from qlazy.tools.Register import CreateRegister,InitRegister

class QStateLogical(QState):

    parity = 0
    
    def set_register(self, dat_left, dat_rignt, bnd, anc):

        self.__dat = {'left': dat_left, 'right': dat_right}
        self.__bnd = bnd
        self.__anc = anc
        self.__x_stab = {'left': [PauliProduct(pauli_str='XXX', qid=[dat_left[0], dat_left[1], dat_left[2]]),
                                  PauliProduct(pauli_str='XXX', qid=[dat_left[2], dat_left[3], dat_left[4]])],
                         'right': [PauliProduct(pauli_str='XXX', qid=[dat_right[0], dat_right[1], dat_right[2]]),
                                   PauliProduct(pauli_str='XXX', qid=[dat_right[2], dat_right[3], dat_right[4]])],
                         'bnd': [PauliProduct(pauli_str='XXX', qid=[dat_left[1], dat_right[0], bnd[0]]),
                                 PauliProduct(pauli_str='XXX', qid=[bnd[0], dat_left[4], dat_right[3]])]}
        
        return self

    def initialize(self, alpha=0.0, beta=0.0, gamma=0.0):
        ''' inject random quantum state to logical qubit of left site '''
        
        self.reset()
        self.u3(self.__dat['left'][0], alpha=alpha, beta=beta, gamma=gamma)
        self.cx(self.__dat['left'][0], self.__dat['left'][3])

        self.parity = 0
        for site in ['left', 'bnd', 'right']:
            for x_stab in self.__x_stab[site]:
                self.reset(qid=[self.__anc[0]])
                self.h(self.__anc[0])
                self.operate(ctrl=self.__anc[0], pp=x_stab)
                self.h(self.__anc[0])
                mval = self.m(qid=[self.__anc[0]]).last
                if site == 'left' or site == 'bnd':
                    self.parity += int(mval)
                    
        self.parity = self.parity % 2
        print("- parity =", self.parity)

        return self
    
    def split(self):

        return self.m(qid=[self.__bnd[0]]).last

    def measure(self, shots=1):

        mqid = [self.__dat['left'][0], self.__dat['left'][3], self.__dat['right'][0], self.__dat['right'][3]]
        freq = self.mx(qid=mqid, shots=shots).frequency

        if self.parity == 1:  # reverse measured value of right qubit if parity = 1
            result_physical = Counter()
            for k,v in freq.items():
                kk = list(map(int, list(k)))
                kk[-1] = (kk[-1] + 1) % 2
                kk = ''.join(map(str, kk))
                result_physical[kk] = v
        else:
            result_physical = freq

        result_logical = Counter()
        for k,v in result_physical.items():
            right = str(sum(map(int, list(k)[0:2])) % 2)
            left = str(sum(map(int, list(k)[2:4])) % 2)
            total = right + left
            result_logical[total] += v

        return result_logical
    
if __name__ == '__main__':

    shots = 1000
    alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
    print("- alpha, beta, gamma = {:.4f}, {:.4f}, {:.4f}".format(alpha, beta, gamma))
    
    dat_left = CreateRegister(5)
    dat_right = CreateRegister(5)
    bnd = CreateRegister(1)
    anc = CreateRegister(1)
    qubit_num = InitRegister(dat_left, dat_right, bnd, anc)

    qs_logical = QStateLogical(qubit_num=qubit_num).set_register(dat_left, dat_right, bnd, anc)
    qs_logical.initialize(alpha=alpha, beta=beta, gamma=gamma)

    mval = qs_logical.split()
    print("- measured value =", mval)

    result_logical = qs_logical.measure(shots=shots)
    print("- actual =", result_logical)

    qs = QState(qubit_num=1).u3(0, alpha=alpha, beta=beta, gamma=gamma)
    result = qs.mx(shots=shots)
    print("- expect =", result.frequency)
