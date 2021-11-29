import random

from qlazy import QState, PauliProduct
from qlazy.tools.Register import CreateRegister,InitRegister

class QStateLogical(QState):

    def set_register(self, dat_left, dat_rignt, bnd, anc):

        self.__dat = {'left': dat_left, 'right': dat_right}
        self.__bnd = bnd
        self.__anc = anc
        self.__x_stab = {'left': [PauliProduct(pauli_str='XXX', qid=[dat_left[0], dat_left[2], dat_left[3]]),
                                  PauliProduct(pauli_str='XXX', qid=[dat_left[1], dat_left[2], dat_left[4]])],
                         'right': [PauliProduct(pauli_str='XXX', qid=[dat_right[0], dat_right[2], dat_right[3]]),
                                   PauliProduct(pauli_str='XXX', qid=[dat_right[1], dat_right[2], dat_right[4]])]}
        self.__z_stab = {'left': [PauliProduct(pauli_str='ZZZ', qid=[dat_left[0], dat_left[1], dat_left[2]]),
                                  PauliProduct(pauli_str='ZZZ', qid=[dat_left[2], dat_left[3], dat_left[4]])],
                         'right': [PauliProduct(pauli_str='ZZZ', qid=[dat_right[0], dat_right[1], dat_right[2]]),
                                   PauliProduct(pauli_str='ZZZ', qid=[dat_right[2], dat_right[3], dat_right[4]])],
                         'bnd': [PauliProduct(pauli_str='ZZZ', qid=[dat_left[1], dat_right[0], bnd[0]]),
                                 PauliProduct(pauli_str='ZZZ', qid=[bnd[0], dat_left[4], dat_right[3]])]}
        self.__lx = {'left': PauliProduct(pauli_str='XX', qid=[dat_left[0], dat_left[1]]),
                     'right': PauliProduct(pauli_str='XX', qid=[dat_right[0], dat_right[1]]),
                     'whole': PauliProduct(pauli_str='XXXX', qid=[dat_left[0], dat_left[1], dat_right[0], dat_right[1]])}

        return self
    
    def initialize(self, alpha=0.0, beta=0.0, gamma=0.0):
        ''' inject random quantum state to logical qubit of left site (|left> = a |+> + b |->, |right> = |+>) '''
        
        self.reset()
        self.u3(self.__dat['left'][0], alpha=alpha, beta=beta, gamma=gamma).h(self.__dat['left'][0])
        self.cx(self.__dat['left'][0], self.__dat['left'][1])
        self.h(self.__dat['right'][0])
        self.cx(self.__dat['right'][0], self.__dat['right'][1])

        for site in ['left', 'right']:
            for x_stab in self.__x_stab[site]:
                self.reset(qid=[self.__anc[0]])
                self.h(self.__anc[0])
                self.operate(ctrl=self.__anc[0], pp=x_stab)
                self.h(self.__anc[0])
                self.m(qid=[self.__anc[0]])

        return self

    def merge(self):
        '''  set |+> to boundary qubits and measure the Z stabilizers including boundary qubits '''

        parity = 1
        self.reset(qid=self.__bnd)
        self.h(self.__bnd[0])
        for z_stab in self.__z_stab['bnd']:
            self.reset(qid=[self.__anc[0]])
            self.h(self.__anc[0])
            self.operate(ctrl=self.__anc[0], pp=z_stab)
            self.h(self.__anc[0])
            mval = self.m(qid=[self.__anc[0]]).last
            parity = parity * int(mval)
            
        return parity

    def Mx(self, shots=1):

        self.reset(qid=[self.__anc[0]])
        self.h(self.__anc[0])
        self.operate(ctrl=self.__anc[0], pp=self.__lx['whole'])
        self.h(self.__anc[0])
        return self.m(qid=[self.__anc[0]], shots=shots).frequency

if __name__ == '__main__':

    shots = 1000
    alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
    print("- alpha, beta, gamma = {:.4f}, {:.4f}, {:.4f}".format(alpha, beta, gamma))
    
    dat_left = CreateRegister(5)
    dat_right = CreateRegister(5)
    bnd = CreateRegister(1)
    anc = CreateRegister(1)
    qubit_num = InitRegister(dat_left, dat_right, bnd, anc)

    qs_logical = QStateLogical(qubit_num).set_register(dat_left, dat_right, bnd, anc)
    qs_logical.initialize(alpha=alpha, beta=beta, gamma=gamma)
    
    parity = qs_logical.merge()
    print("- parity =", parity)
    
    result_logical = qs_logical.Mx(shots=shots)
    print("- actual =", result_logical)
    
    qs = QState(qubit_num=1).u3(0, alpha=alpha, beta=beta, gamma=gamma)
    result = qs.m(shots=shots)
    print("- expect =", result.frequency)
