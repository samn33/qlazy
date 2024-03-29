from qlazy import QState

# custom gates

class MyQState(QState):
    
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

    def q_oracle(self,id_in,id_out,func):

        num = 2**len(id_in)
        for x in range(num):
            y = func(x)
            if y == 1:
                self.mpmct(id_in,id_out,x)

        return self

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

# functions

def gray_code(n):

    for k in range(2**n):
        yield k^(k>>1)
        
def func(x):

    if x == 1 or x == 5:
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

if __name__ == '__main__':

    # set register
    id_in = create_register(3)
    id_out = create_register(1)
    qnum = init_register(id_in,id_out)

    # initial state
    qs = MyQState(qnum)
    qs.hadamard(id_in)

    # quantum oracle
    qs.q_oracle(id_in,id_out,func)

    # print results
    in_list,out_list = qs.result(id_in,id_out)
    for i in range(len(in_list)):
        print("{0:03b} -> {1:d}".format(in_list[i],out_list[i]))
