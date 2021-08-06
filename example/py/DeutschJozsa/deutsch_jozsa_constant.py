import sys
import random
from qlazy import QState

# custom gates

def hadamard(self,id):

    for i in range(len(id)):
        self.h(id[i])
    return self

def multi_cx(self,id_in,id_out):

    #
    # hadamard
    #
    self.h(id_out[0])

    #
    # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
    #
    bitnum = len(id_in)
    psi = 1.0/(2**(bitnum-1)) # unit=pi(radian)
    gray_pre = 0
    for gray in gray_code(bitnum):
        if gray == 0:
            continue
        msb = len(str(bin(gray)))-3
        chb = len(str(bin(gray^gray_pre)))-3
        if gray != 1:
            if chb == msb:
                chb -= 1
            self.cx(id_in[chb],id_in[msb])
        self.cp(id_in[msb],id_out[0],phase=psi)
        psi = -psi
        gray_pre = gray
    
    #
    # hadamard
    #
    self.h(id_out[0])

    return self
    
def mpmct(self,id_in,id_out,x):

    bitnum = len(id_in)
    
    for i in range(bitnum):
        bit = (x>>i)%2
        if bit == 0:
            self.x(id_in[i])
            
    self.multi_cx(id_in,id_out)

    for i in range(bitnum):
        bit = (x>>i)%2
        if bit == 0:
            self.x(id_in[i])

    return self

def q_oracle(self,id_in,id_out,table):

    num = 2**len(id_in)
    for x in range(num):
        y = table[x]
        if y == 1:
            self.mpmct(id_in,id_out,x)

    return self

# functions

def gray_code(n):

    for k in range(2**n):
        yield k^(k>>1)

def create_register(num):

    return [0]*num

def init_register(*args):

    idx = 0
    for i in range(len(args)):
        for j in range(len(args[i])):
            args[i][j] = idx
            idx += 1
    return idx

def result(self,id_a,id_b):

    # measurement
    id_ab = id_a + id_b
    iid_ab = id_ab[::-1]
    shots = (2**len(id_a))*5
    freq = self.m(iid_ab,shots=shots).frq
    
    # set results
    a_list = []
    r_list = []
    for i in range(len(freq)):
        if freq[i] > 0:
            a_list.append(i%(2**len(id_a)))
            r_list.append(i>>len(id_a))
    return (a_list,r_list)

if __name__ == '__main__':

    # add custom gates
    QState.hadamard = hadamard
    QState.multi_cx = multi_cx
    QState.mpmct = mpmct
    QState.q_oracle = q_oracle
    QState.result = result

    # input qubit number
    qnum_in = 4
    
    # set function 'constant' or 'balanced'
    func = 'constant'
    if func == 'constant':
        v = random.randint(0,1)
        table =[v]*(2**qnum_in)
    elif func == 'balanced':
        table = [i%2 for i in range(2**qnum_in)]
        random.shuffle(table)
    else:
        sys.exit()
    print("== test function ==")
    print(table)
    
    # set register
    id_in = create_register(qnum_in)
    id_out = create_register(1)
    qnum = init_register(id_in,id_out)
    id = id_in + id_out

    # initial state
    qs = QState(qnum)
    qs.hadamard(id_in)
    qs.x(id_out[0])

    # quantum oracle
    qs.q_oracle(id_in,id_out,table)
    qs.hadamard(id)

    # measure and judge
    cnt = 0
    for freq in qs.m(id_in, shots=100).frq:
        if freq != 0: cnt += 1
    print("== judgement ==")
    if cnt == 1:
        print("constant")
    else:
        print("balanced")
        
    # qs.free()
