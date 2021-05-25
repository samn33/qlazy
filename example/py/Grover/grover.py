import math
from qlazy import QState

# custom gates

def hadamard(self,id):

    for i in range(len(id)):
        self.h(id[i])
    return self

def flip(self,id):

    for i in range(len(id)):
        self.x(id[i])
    return self

def multi_cz(self,id_in,id_out):

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
    
    return self

def multi_cx(self,id_in,id_out):

    self.h(id_out[0])
    self.multi_cz(id_in,id_out)
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

def q_oracle(self,id_in,id_out,func):

    num = 2**len(id_in)
    for x in range(num):
        y = func(x)
        if y == 1:
            self.mpmct(id_in,id_out,x)

    return self

# functions

def gray_code(n):

    for k in range(2**n):
        yield k^(k>>1)
        
def func(x):

    if x == 881 or x == 883:
        y = 1
    else:
        y = 0
    return y

def create_register(num):

    return [0]*num

def init_register(*args):

    idx = 0
    for i in range(len(args)):
        for j in range(len(args[i])):
            args[i][j] = idx
            idx += 1
    return idx

def result(self,id,solnum):

    # measurement
    iid = id[::-1]
    freq = self.m(iid, shots=100).frq

    res = []
    for _ in range(solnum):
        idx = freq.index(max(freq))
        res.append(idx)
        freq[idx] = 0

    return res
    
def opt_iter(N,solnum):

    return int(0.25*math.pi/math.asin(math.sqrt(solnum/N)))

if __name__ == '__main__':

    # add custom gates
    QState.hadamard = hadamard
    QState.flip = flip
    QState.multi_cz = multi_cz
    QState.multi_cx = multi_cx
    QState.mpmct = mpmct
    QState.q_oracle = q_oracle
    QState.result = result

    # set parameters
    bits = 10
    N = 2**bits
    solnum = 2
    
    # set register
    id_in = create_register(bits)
    id_out = create_register(1)
    qnum = init_register(id_in,id_out)

    id_in_c = id_in[:-1]
    id_in_t = [id_in[-1]]

    # initial state
    qs = QState(qnum)
    qs.hadamard(id_in)
    qs.x(id_out[0]).h(id_out[0])
    
    iter = opt_iter(N,solnum)
    print("== algorithm start (total iter:{}) ==".format(iter))

    for i in range(iter):

        print("- iter no. = ", i)

        qs.q_oracle(id_in,id_out,func)
    
        qs.hadamard(id_in)
        qs.flip(id_in)
        qs.multi_cz(id_in_c,id_in_t)
        qs.flip(id_in)
        qs.hadamard(id_in)
    
    # print results
    res = qs.result(id_in,solnum)
    print("== result==")
    print("x =", res)

    qs.free()
