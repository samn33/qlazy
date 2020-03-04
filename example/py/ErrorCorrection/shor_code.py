import random
from qlazypy import DensOp

def create_densop():

    de_ini = DensOp(qubit_num=9).h(0)
    de_fin = de_ini.clone()
    return de_ini, de_fin
    
def noise(self, kind='', prob=0.0, qid=[]):

    qchannel = {'bit_flip':self.bit_flip,
                'phase_flip':self.phase_flip,
                'bit_phase_flip':self.bit_phase_flip,
                'depolarize':self.depolarize,
                'amp_dump':self.amp_dump,
                'phase_dump':self.phase_dump}
    [qchannel[kind](i, prob=prob) for i in qid]
    return self

def encode(self):

    self.cx(0,3).cx(0,6)
    self.h(0).h(3).h(6)
    self.cx(0,1).cx(0,2)
    self.cx(3,4).cx(3,5)
    self.cx(6,7).cx(6,8)
    return self
    
def correct(self):

    self.cx(0,2).cx(0,1)
    self.cx(3,5).cx(3,4)
    self.cx(6,8).cx(6,7)
    self.ccx(2,1,0).ccx(5,4,3).ccx(8,7,6)
    self.h(0).h(3).h(6)
    self.cx(0,3).cx(0,6)
    self.ccx(6,3,0)
    return self

if __name__ == '__main__':

    # add custom gate
    DensOp.add_method(encode)
    DensOp.add_method(noise)
    DensOp.add_method(correct)

    # settings
    kind = 'depolarize' # bit_flip,phase_flip,bit_phase_flip,depolarize,amp_dump,phase_dump
    prob = 1.0
    qid = [0]
    print("== settings ==")
    print("* kind of noise        =", kind)
    print("* probability of noise =", prob)
    print("* noisy channels       =", qid)

    # error correction (shor code)
    de_ini, de_fin = create_densop()
    de_fin.encode()
    de_fin.noise(kind=kind, prob=prob, qid=qid)
    de_fin.correct()

    # evaluate fidelity
    fid = de_fin.fidelity(de_ini, qid=[0])
    print("== result ==")
    print("* fidelity = {:.6f}".format(fid))

    # free all densops
    DensOp.free_all(de_ini, de_fin)
