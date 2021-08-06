import numpy as np
from pprint import pprint
from qlazy import QState

def swap(self,q0,q1):

    self.cx(q0,q1).cx(q1,q0).cx(q0,q1)
    return self

def qft2(self,q1,q0):

    self.h(q1).cp(q0,q1,phase=0.5)
    self.h(q0)
    self.swap(q0,q1)
    return self

def iqft2(self,q0,q1):

    self.h(q0)
    self.cp(q0,q1,phase=-0.5).h(q1)
    self.swap(q0,q1)
    return self

def qft3(self,q2,q1,q0):

    self.h(q2).cp(q1,q2,phase=0.5).cp(q0,q2,phase=0.25)
    self.h(q1).cp(q0,q1,phase=0.5)
    self.h(q0)
    self.swap(q0,q2)
    return self

def iqft3(self,q0,q1,q2):

    self.h(q0)
    self.cp(q0,q1,phase=-0.5).h(q1)
    self.cp(q0,q2,phase=-0.25).cp(q1,q2,phase=-0.5).h(q2)

    self.swap(q0,q2)
    return self

def qft(self,id=None):

    dim = len(id)
    iid = id[::-1]

    for i in range(dim):
        self.h(iid[dim-i-1])
        phase = 1.0
        for j in range(dim-i-1):
            phase /= 2.0
            self.cp(iid[dim-i-j-2],iid[dim-i-1],phase=phase)

    i = 0
    while i < dim-1-i:
        self.swap(iid[i], iid[dim-1-i])
        i += 1

    return self
    
def iqft(self,id=None):

    dim = len(id)

    for i in range(dim):
        phase = -1.0/2**i
        for j in range(i):
            self.cp(id[j],id[i],phase=phase)
            phase *= 2.0
        self.h(id[i])
            
    i = 0
    while i < dim-1-i:
        self.swap(id[i], id[dim-1-i])
        i += 1
        
    return self

def main():
    
    QState.swap = swap
    QState.qft2 = qft2
    QState.qft3 = qft3
    QState.qft = qft
    QState.iqft2 = iqft2
    QState.iqft3 = iqft3
    QState.iqft = iqft

    print("== initial state ==")
    qs = QState(3).h(1).h(0)
    qs.show()
    data_in = qs.amp

    print("== QFT ==")
    qs.qft([0,1,2])
    qs.show()

    print("== FFT (numpy) ==")
    data_fft = np.fft.ifft(data_in)
    norm = np.linalg.norm(data_fft,ord=2)
    data_fft /= norm
    pprint(data_fft)
    
    # qs.free()

if __name__ == '__main__':
    main()
