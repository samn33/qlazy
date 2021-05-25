#
# 参考：上坂、「量子コンピュータの基礎数理」、コロナ社
#
from qlazy import QState

# custom gates

def encode(self,decimal,id):

    for i in range(len(id)):
        if (decimal>>i)%2 == 1:
            self.x(id[i])
    return self

def decode(self,id):

    iid = id[::-1]
    return self.m(iid,shots=1).lst

def hadamard(self,id):

    for i in range(len(id)):
        self.h(id[i])
    return self

# グレイコードを利用した補助ビットなしのToffoliゲート(p.104-p.119)
# --- 基本ゲート数：O(n^2) ---
def toffoli(self,id_in,id_out):

    # hadamard
    self.h(id_out[0])

    # controlled-RZ(psi), psi=pi/(2**(bitnum-1))
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
    
    # hadamard
    self.h(id_out[0])

    return self

# 多数の補助ビットありToffoliゲート(p.120 図4.22)
# --- 基本ゲート数：O(n) ---
def toffoli2(self,id_ctr,id_sub,id_tar):

    id = id_ctr + id_sub + id_tar

    qnum_ctr = len(id_ctr)
    qnum_sub = len(id_sub)
    qnum_tar = len(id_tar)
    qnum = len(id)

    c0 = qnum_ctr-1
    c1 = qnum-2
    t = qnum-1
    incr = -1
    block = 0
    while True:
        #print(c0,c1,t)
        if c0 == 1:
            self.ccx(id[0],id[1],id[t])
            incr = -incr
            block += 1
        else:
            self.ccx(id[c0],id[c1],id[t])
            
        c0 += incr
        c1 += incr
        t += incr

        if c0 == qnum_ctr-1:
            incr = -incr
            if block == 2:
                break

    return self

# 補助ビット数1のToffoliゲート(p.122 図4.23)
# --- 基本ゲート数：O(n) ---
def toffoli3(self,id_ctr,id_sub,id_tar):

    id = id_ctr + id_sub + id_tar

    qnum_ctr = len(id_ctr)
    qnum_sub = len(id_sub)
    qnum_tar = len(id_tar)
    qnum = len(id)

    qnum_0_ctr = qnum//2
    qnum_0_sub = qnum - 2 - qnum_0_ctr
    id_0_ctr = id[:qnum_0_ctr]
    id_0_sub = id[qnum_0_ctr:-2]
    id_0_tar = [id[-2]]

    qnum_1_sub = qnum//2
    qnum_1_ctr = qnum - 1 - qnum_1_sub
    id_1_sub = id[:qnum_1_sub]
    id_1_ctr = id[qnum_1_sub:-1]
    id_1_tar = [id[-1]]

    self.toffoli2(id_0_ctr,id_0_sub,id_0_tar)
    self.toffoli2(id_1_ctr,id_1_sub,id_1_tar)
    self.toffoli2(id_0_ctr,id_0_sub,id_0_tar)
    self.toffoli2(id_1_ctr,id_1_sub,id_1_tar)
    
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

def toffoli_test(qnum):

    # set register
    qnum_ctr = qnum - 1
    qnum_tar = 1
    id_ctr = create_register(qnum_ctr)
    id_tar = create_register(qnum_tar)
    qnum = init_register(id_ctr,id_tar)

    for x in range(2**qnum_ctr):

        qs = QState(qnum)
        qs.encode(x,id_ctr)
        qs.toffoli(id_ctr,id_tar)

        res = qs.decode(id_tar)
        print("x = {0:0{size}b}, res = {1:}".format(x,res,size=qnum_ctr))

        qs.free()

def toffoli2_test(qnum):

    qnum_ctr = qnum//2
    qnum_tar = 1
    qnum_sub = qnum - qnum_ctr - qnum_tar
    id_ctr = create_register(qnum_ctr)
    id_sub = create_register(qnum_sub)
    id_tar = create_register(qnum_tar)
    init_register(id_ctr,id_sub,id_tar)

    for x in range(2**qnum_ctr):
        
        qs = QState(qnum)
        qs.encode(x,id_ctr)
        qs.toffoli2(id_ctr,id_sub,id_tar)

        print("x = {0:0{size}b}, res = {1:}".format(x,qs.decode(id_tar),size=qnum_ctr))

        qs.free()
    
def toffoli3_test(qnum):

    qnum_ctr = qnum-2
    qnum_sub = 1
    qnum_tar = 1
    id_ctr = create_register(qnum_ctr)
    id_sub = create_register(qnum_sub)
    id_tar = create_register(qnum_tar)
    init_register(id_ctr,id_sub,id_tar)

    for x in range(2**qnum_ctr):
        
        qs = QState(qnum)
        qs.encode(x,id_ctr)
        qs.toffoli3(id_ctr,id_sub,id_tar)

        print("x = {0:0{size}b}, res = {1:}".format(x,qs.decode(id_tar),size=qnum_ctr))

        qs.free()
    
if __name__ == '__main__':

    # add custom gates
    QState.encode = encode
    QState.decode = decode
    QState.hadamard = hadamard
    QState.toffoli = toffoli
    QState.toffoli2 = toffoli2
    QState.toffoli3 = toffoli3

    print("== toffoli ==")
    toffoli_test(6)
    print("== toffoli2 ==")
    toffoli2_test(11)
    print("== toffoli3 ==")
    toffoli3_test(7)
