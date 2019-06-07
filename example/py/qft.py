from qlazypy import QState

def qft2(self,q0,q1):

    self.h(q1).cp(q0,q1,phase=0.5)
    self.h(q0)
    return self

def iqft2(self,q0,q1):

    self.h(q0)
    self.cp(q0,q1,phase=-0.5).h(q1)
    return self

def qft3(self,q0,q1,q2):

    self.h(q2).cp(q1,q2,phase=0.5).cp(q0,q2,phase=0.25)
    self.h(q1).cp(q0,q1,phase=0.5)
    self.h(q0)
    return self

def qft(self,id=None):

    dim = len(id)

    for i in range(dim):
        self.h(id[dim-i-1])
        phase = 1.0
        for j in range(dim-i-1):
            phase /= 2.0
            self.cp(id[dim-i-j-2],id[dim-i-1],phase=phase)
            
    return self
    
def iqft3(self,q0,q1,q2):

    self.h(q0)
    self.cp(q0,q1,phase=-0.5).h(q1)
    self.cp(q0,q2,phase=-0.25).cp(q1,q2,phase=-0.5).h(q2)
    return self

def iqft(self,id=None):

    dim = len(id)

    for i in range(dim):
        phase = -1.0/2**i
        for j in range(i):
            self.cp(id[j],id[i],phase=phase)
            phase *= 2.0
        self.h(id[i])
            
    return self
    
def main():

    QState.qft2 = qft2
    QState.qft3 = qft3
    QState.qft = qft
    QState.iqft2 = iqft2
    QState.iqft3 = iqft3
    QState.iqft = iqft
    
    qs = QState(3)
    print("== before ==")
    qs.show()

    qs.qft(id=[0,1,2])
    print("== after ==")
    qs.show()

    qs.free()

if __name__ == '__main__':
    main()
