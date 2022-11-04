import random
from qlazy import QState, PauliProduct
from qlazy.tools.Register import CreateRegister,InitRegister

class QStateLogical(QState):

    def set_register(self, dat_cnt, dat_int, dat_tar, bnd_cnt, bnd_tar, anc):

        self.__dat = {'cnt': dat_cnt, 'int': dat_int, 'tar': dat_tar}
        self.__bnd = {'cnt': bnd_cnt, 'tar': bnd_tar}
        self.__anc = anc
        self.__x_stab = {'cnt': [PauliProduct(pauli_str='XXX', qid=[dat_cnt[0], dat_cnt[1], dat_cnt[2]]),
                                  PauliProduct(pauli_str='XXX', qid=[dat_cnt[2], dat_cnt[3], dat_cnt[4]])],
                         'int': [PauliProduct(pauli_str='XXX', qid=[dat_int[0], dat_int[1], dat_int[2]]),
                                   PauliProduct(pauli_str='XXX', qid=[dat_int[2], dat_int[3], dat_int[4]])],
                         'tar': [PauliProduct(pauli_str='XXX', qid=[dat_tar[0], dat_tar[1], dat_tar[2]]),
                                   PauliProduct(pauli_str='XXX', qid=[dat_tar[2], dat_tar[3], dat_tar[4]])],
                         'bnd_tar': [PauliProduct(pauli_str='XXX', qid=[dat_int[1], dat_tar[0], bnd_tar[0]]),
                                     PauliProduct(pauli_str='XXX', qid=[bnd_tar[0], dat_int[4], dat_tar[3]])]}
        self.__z_stab = {'cnt': [PauliProduct(pauli_str='ZZZ', qid=[dat_cnt[0], dat_cnt[2], dat_cnt[3]]),
                                  PauliProduct(pauli_str='ZZZ', qid=[dat_cnt[1], dat_cnt[2], dat_cnt[4]])],
                         'int': [PauliProduct(pauli_str='ZZZ', qid=[dat_int[0], dat_int[2], dat_int[3]]),
                                   PauliProduct(pauli_str='ZZZ', qid=[dat_int[1], dat_int[2], dat_int[4]])],
                         'tar': [PauliProduct(pauli_str='ZZZ', qid=[dat_tar[0], dat_tar[2], dat_tar[3]]),
                                 PauliProduct(pauli_str='ZZZ', qid=[dat_tar[1], dat_tar[2], dat_tar[4]])],
                         'bnd_cnt': [PauliProduct(pauli_str='ZZZ', qid=[dat_cnt[0], bnd_cnt[0], dat_int[3]]),
                                     PauliProduct(pauli_str='ZZZ', qid=[dat_cnt[1], bnd_cnt[0], dat_int[4]])]}
        self.__lx = PauliProduct(pauli_str='XXXX', qid=[dat_int[0], dat_int[3], dat_cnt[0], dat_cnt[3]])
        self.__lz = PauliProduct(pauli_str='ZZZZ', qid=[dat_int[0], dat_int[1], dat_tar[0], dat_tar[1]])
        return self

    def __indirect_measure(self, pp, shots=1):

        self.reset(qid=[self.__anc[0]])
        self.h(self.__anc[0])
        self.operate(qctrl=self.__anc[0], pp=pp)
        self.h(self.__anc[0])
        return self.m(qid=[self.__anc[0]], shots=shots)
    
    def initialize(self, alpha=0.0, beta=0.0, gamma=0.0):
        ''' |cnt> = a |0> + b |1>, |tar> = |0> '''
        
        self.reset()
        self.rz(self.__dat['cnt'][0], phase=alpha).rx(self.__dat['cnt'][0], phase=beta).rz(self.__dat['cnt'][0], phase=gamma)
        self.cx(self.__dat['cnt'][0], self.__dat['cnt'][3])
        self.h(self.__dat['int'][0])
        self.cx(self.__dat['int'][0], self.__dat['int'][3])
        for site in ['cnt', 'int', 'tar']:
            for x_stab in self.__x_stab[site]:
                mval = self.__indirect_measure(x_stab).last
        return self

    def merge_cnt_int(self):

        parity = 0
        self.reset(qid=self.__bnd['cnt'])
        self.h(self.__bnd['cnt'][0])
        for z_stab in self.__z_stab['bnd_cnt']:
            parity += int(self.__indirect_measure(z_stab).last)
        if parity % 2 == 1: self.operate(pp=self.__lx)
        return self

    def merge_int_tar(self):

        self.reset(qid=self.__bnd['tar'])
        for x_stab in self.__x_stab['bnd_tar']:
            self.__indirect_measure(x_stab)
        return self

    def split_cnt_int(self):

        return self.mx(qid=[self.__bnd['cnt'][0]]).last

    def measure(self, shots=1):

        return self.__indirect_measure(self.__lz, shots=shots).frequency

if __name__ == '__main__':

    shots = 100
    alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
    print("- alpha, beta, gamma = {:.4f}, {:.4f}, {:.4f}".format(alpha, beta, gamma))
    
    dat_cnt, dat_int, dat_tar = CreateRegister(5), CreateRegister(5), CreateRegister(5)
    bnd_cnt, bnd_tar, anc = CreateRegister(1), CreateRegister(1), CreateRegister(1)
    qubit_num = InitRegister(dat_cnt, dat_int, dat_tar, bnd_cnt, bnd_tar, anc)

    qs_logical = QStateLogical(qubit_num).set_register(dat_cnt, dat_int, dat_tar, bnd_cnt, bnd_tar, anc)
    qs_logical.initialize(alpha=alpha, beta=beta, gamma=gamma)
    qs_logical.merge_cnt_int()
    qs_logical.split_cnt_int()
    qs_logical.merge_int_tar()

    result_logical = qs_logical.measure(shots=shots)
    print("- actual =", result_logical)

    result = QState(qubit_num=1).rz(0, phase=alpha).rx(0, phase=beta).rz(0, phase=gamma).m(shots=shots)
    print("- expect =", result.frequency)
