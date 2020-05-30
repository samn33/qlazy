import numpy as np
from qlazypy import QState

def logic_x(self, qid):

    [self.x(q) for q in qid]
    return self
    
def logic_z(self, qid):

    [self.z(q) for q in qid]
    return self
    
def ctr_logic_x(self, q, qid):

    [self.cx(q, qtar) for qtar in qid]
    return self

def ctr_logic_z(self, q, qid):

    [self.cz(q, qtar) for qtar in qid]
    return self

def ctr_g1(self, q, qid):

    self.cx(q, qid[0]).cz(q, qid[1]).cz(q, qid[2]).cx(q, qid[3])
    return self

def ctr_g2(self, q, qid):

    self.cx(q, qid[1]).cz(q, qid[2]).cz(q, qid[3]).cx(q, qid[4])
    return self

def ctr_g3(self, q, qid):

    self.cx(q, qid[0]).cx(q, qid[2]).cz(q, qid[3]).cz(q, qid[4])
    return self
    
def ctr_g4(self, q, qid):

    self.cz(q, qid[0]).cx(q, qid[1]).cx(q, qid[3]).cz(q, qid[4])
    return self

def encode(self, phase, qid_anc, qid_cod):

    # make logical zero state: |0>_L

    # g1
    self.h(qid_anc[0]).ctr_g1(qid_anc[0], qid_cod).h(qid_anc[0])
    self.m(qid=[qid_anc[0]])
    mval = self.m_value(binary=True)
    if mval == '1': self.z(qid_cod[0]).z(qid_cod[2])
    self.reset(qid=[qid_anc[0]])

    # g2
    self.h(qid_anc[1]).ctr_g2(qid_anc[1], qid_cod).h(qid_anc[1])
    self.m(qid=[qid_anc[1]])
    mval = self.m_value(binary=True)
    if mval == '1': self.z(qid_cod[0]).z(qid_cod[1]).z(qid_cod[2]).z(qid_cod[3])
    self.reset(qid=[qid_anc[1]])
    
    # g3
    self.h(qid_anc[2]).ctr_g3(qid_anc[2], qid_cod).h(qid_anc[2])
    self.m(qid=[qid_anc[2]])
    mval = self.m_value(binary=True)
    if mval == '1': self.z(qid_cod[0]).z(qid_cod[1]).z(qid_cod[3]).z(qid_cod[4])
    self.reset(qid=[qid_anc[2]])
    
    # g4
    self.h(qid_anc[3]).ctr_g4(qid_anc[3], qid_cod).h(qid_anc[3])
    self.m(qid=[qid_anc[3]])
    mval = self.m_value(binary=True)
    if mval == '1': self.z(qid_cod[0]).z(qid_cod[2]).z(qid_cod[3])
    self.reset(qid=[qid_anc[3]])

    # logical z
    self.h(qid_anc[4]).ctr_logic_z(qid_anc[4], qid_cod).h(qid_anc[4])
    self.m(qid=[qid_anc[4]])
    mval = self.m_value(binary=True)
    if mval == '1':
        self.x(qid_cod[0]).x(qid_cod[1]).x(qid_cod[2]).x(qid_cod[3]).x(qid_cod[4])
    self.reset(qid=[qid_anc[4]])

    # make random quantum state and encode (with quantum teleportation)

    self.u3(qid_anc[0], alpha=phase[0], beta=phase[1], gamma=phase[2]) # input quantum state
    print("* input quantum state")
    self.show(qid=[qid_anc[0]])
    
    self.h(qid_anc[1])
    self.ctr_logic_x(qid_anc[1], qid_cod).cx(qid_anc[0], qid_anc[1])
    self.h(qid_anc[0])
    self.m(qid=qid_anc[0:2])
    mval = self.m_value(binary=True)
    if mval == '00': pass
    elif mval == '01': self.logic_x(qid_cod)
    elif mval == '10': self.logic_z(qid_cod)
    elif mval == '11': self.logic_x(qid_cod).logic_z(qid_cod)
    self.reset(qid=qid_anc)
    
    return self

def add_noise(self, q, qid, kind):

    if kind == 'X': self.x(qid[q])
    elif kind == 'Z': self.z(qid[q])
    elif kind == 'XZ': self.z(qid[q]).x(qid[q])
    return self

def correct_err(self, qid_anc, qid_cod):

    self.reset(qid=qid_anc)

    # syndrome
    self.h(qid_anc[0]).ctr_g1(qid_anc[0], qid_cod).h(qid_anc[0])
    self.h(qid_anc[1]).ctr_g2(qid_anc[1], qid_cod).h(qid_anc[1])
    self.h(qid_anc[2]).ctr_g3(qid_anc[2], qid_cod).h(qid_anc[2])
    self.h(qid_anc[3]).ctr_g4(qid_anc[3], qid_cod).h(qid_anc[3])
    self.m(qid=qid_anc[0:4])
    mval = self.m_value(binary=True)
    print("* syndrome =", mval)

    # recovery
    if mval == '0000': pass
    elif mval == '0001': self.x(qid_cod[0])
    elif mval == '1010': self.z(qid_cod[0])
    elif mval == '1011': self.z(qid_cod[0]).x(qid_cod[0])
    elif mval == '1000': self.x(qid_cod[1])
    elif mval == '0101': self.z(qid_cod[1])
    elif mval == '1101': self.z(qid_cod[1]).x(qid_cod[1])
    elif mval == '1100': self.x(qid_cod[2])
    elif mval == '0010': self.z(qid_cod[2])
    elif mval == '1110': self.z(qid_cod[2]).x(qid_cod[2])
    elif mval == '0110': self.x(qid_cod[3])
    elif mval == '1001': self.z(qid_cod[3])
    elif mval == '1111': self.z(qid_cod[3]).x(qid_cod[3])
    elif mval == '0011': self.x(qid_cod[4])
    elif mval == '0100': self.z(qid_cod[4])
    elif mval == '0111': self.z(qid_cod[4]).x(qid_cod[4])

    return self

if __name__ == '__main__':

    QState.add_methods(logic_x, logic_z, ctr_logic_x, ctr_logic_z,
                       ctr_g1, ctr_g2, ctr_g3, ctr_g4,
                       encode, add_noise, correct_err)

    # create registers
    qid_anc = QState.create_register(5)
    qid_cod = QState.create_register(5)
    qnum = QState.init_register(qid_anc, qid_cod)

    # parameters for input quantum state (U3 gate params)
    phase = [np.random.rand(), np.random.rand(), np.random.rand()]

    # encode quantum state
    qs_ini = QState(qnum)
    qs_ini.encode(phase, qid_anc, qid_cod)
    qs_fin = qs_ini.clone()

    # noise
    q = np.random.randint(0, len(qid_cod))
    kind = np.random.choice(['X','Z','XZ'])
    print("* noise '{:}' to #{:} qubit".format(kind, q))
    qs_fin.add_noise(q, qid_cod, kind)

    # error correction
    qs_fin.correct_err(qid_anc, qid_cod)

    # result
    fid = qs_ini.fidelity(qs_fin, qid=qid_cod)
    print("* fidelity = {:.6f}".format(fid))
    
    QState.free_all(qs_ini, qs_fin)
