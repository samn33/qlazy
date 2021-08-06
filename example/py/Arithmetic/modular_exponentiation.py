from qlazy import QState

def swap(self,id_0,id_1):

    dim = min(len(id_0),len(id_1))
    for i in range(dim):
        self.cx(id_0[i],id_1[i]).cx(id_1[i],id_0[i]).cx(id_0[i],id_1[i])
    return self
    
def ctr_swap(self,id_ctr,id_0,id_1):

    dim = min(len(id_0),len(id_1))
    for i in range(dim):
        self.ccx(id_ctr[0],id_0[i],id_1[i])
        self.ccx(id_ctr[0],id_1[i],id_0[i])
        self.ccx(id_ctr[0],id_0[i],id_1[i])
    return self
    
def sum(self,q0,q1,q2):

    self.cx(q1,q2).cx(q0,q2)
    return self
    
def i_sum(self,q0,q1,q2):

    self.cx(q0,q2).cx(q1,q2)
    return self
    
def carry(self,q0,q1,q2,q3):

    self.ccx(q1,q2,q3).cx(q1,q2).ccx(q0,q2,q3)
    return self

def i_carry(self,q0,q1,q2,q3):

    self.ccx(q0,q2,q3).cx(q1,q2).ccx(q1,q2,q3)
    return self

def plain_adder(self,id_a,id_b,id_c):

    depth = len(id_a)
    for i in range(depth):
        self.carry(id_c[i],id_a[i],id_b[i],id_c[i+1])
    self.cx(id_a[depth-1],id_b[depth-1])
    self.sum(id_c[depth-1],id_a[depth-1],id_b[depth-1])
    for i in reversed(range(depth-1)):
        self.i_carry(id_c[i],id_a[i],id_b[i],id_c[i+1])
        self.sum(id_c[i],id_a[i],id_b[i])
    return self

def arrow(self,N,q,id):

    for i in range(len(id)):
        if (N>>i)%2 == 1:
            self.cx(q,id[i])
    return self

def arrow2(self,i,a,id_ctr,id_x,id_xx):

    aa = a * 2**i
    for j in range(len(id_xx)):
        if (aa>>j)%2 == 1:
            self.ccx(id_ctr[0],id_x[i],id_xx[j])
    return self
    
def arrow3(self,id_ctr,id_x,id_y):

    for j in range(len(id_x)):
        self.ccx(id_ctr[0],id_x[j],id_y[j])
    return self
    
def i_plain_adder(self,id_a,id_b,id_c):

    depth = len(id_a)
    for i in range(depth-1):
        self.i_sum(id_c[i],id_a[i],id_b[i])
        self.carry(id_c[i],id_a[i],id_b[i],id_c[i+1])
    self.i_sum(id_c[depth-1],id_a[depth-1],id_b[depth-1])
    self.cx(id_a[depth-1],id_b[depth-1])
    for i in reversed(range(depth)):
        self.i_carry(id_c[i],id_a[i],id_b[i],id_c[i+1])
    return self

def modular_adder(self,N,id_a,id_b,id_c,id_N,id_t):

    self.plain_adder(id_a,id_b,id_c)
    self.swap(id_a,id_N)
    self.i_plain_adder(id_a,id_b,id_c)
    self.x(id_b[len(id_b)-1])
    self.cx(id_b[len(id_b)-1],id_t[0])
    self.x(id_b[len(id_b)-1])
    self.arrow(N,id_t[0],id_a)
    self.plain_adder(id_a,id_b,id_c)
    self.arrow(N,id_t[0],id_a)
    self.swap(id_a,id_N)
    self.i_plain_adder(id_a,id_b,id_c)
    self.cx(id_b[len(id_b)-1],id_t[0])
    self.plain_adder(id_a,id_b,id_c)
    return self

def i_modular_adder(self,N,id_a,id_b,id_c,id_N,id_t):

    self.i_plain_adder(id_a,id_b,id_c)
    self.cx(id_b[len(id_b)-1],id_t[0])
    self.plain_adder(id_a,id_b,id_c)
    self.swap(id_a,id_N)
    self.arrow(N,id_t[0],id_a)
    self.i_plain_adder(id_a,id_b,id_c)
    self.arrow(N,id_t[0],id_a)
    self.x(id_b[len(id_b)-1])
    self.cx(id_b[len(id_b)-1],id_t[0])
    self.x(id_b[len(id_b)-1])
    self.plain_adder(id_a,id_b,id_c)
    self.swap(id_a,id_N)
    self.i_plain_adder(id_a,id_b,id_c)
    
    return self

def ctr_modular_multiplier(self,a,N,id_ctr,id_x,id_xx,id_y,id_c,id_N,id_t):

    depth = len(id_x)
    for i in range(depth):
        self.arrow2(i,a,id_ctr,id_x,id_xx)
        self.modular_adder(N,id_xx,id_y,id_c,id_N,id_t)
        self.arrow2(i,a,id_ctr,id_x,id_xx)
    self.x(id_ctr[0])
    self.arrow3(id_ctr,id_x,id_y)
    self.x(id_ctr[0])
    return self
    
def i_ctr_modular_multiplier(self,a,N,id_ctr,id_x,id_xx,id_y,id_c,id_N,id_t):

    depth = len(id_x)
    self.x(id_ctr[0])
    self.arrow3(id_ctr,id_x,id_y)
    self.x(id_ctr[0])
    for i in reversed(range(depth)):
        self.arrow2(i,a,id_ctr,id_x,id_xx)
        self.i_modular_adder(N,id_xx,id_y,id_c,id_N,id_t)
        self.arrow2(i,a,id_ctr,id_x,id_xx)
    return self

def modular_exponentiation(self,a,N,id_x,id_xx,id_xxx,id_y,id_c,id_N,id_t):

    depth = len(id_x)
    id_ctr = [0]
    for i in range(depth):
        aa = a**(2**i)
        id_ctr[0] = id_x[i]
        self.ctr_modular_multiplier(aa,N,id_ctr,id_xx,id_xxx,id_y,id_c,id_N,id_t)
        self.ctr_swap(id_ctr,id_xx,id_y)
        self.i_ctr_modular_multiplier(aa,N,id_ctr,id_xx,id_xxx,id_y,id_c,id_N,id_t)
    return self
    
def encode(self,decimal,id):

    for i in range(len(id)):
        if (decimal>>i)%2 == 1:
            self.x(id[i])
    return self

def decode(self,id):

    iid = id[::-1]
    return self.m(iid,shots=1).lst

def create_register():

    num = 0
    id_x = [i for i in range(2)]
    num += len(id_x)
    id_xx = [i+num for i in range(2)]
    num += len(id_xx)
    id_xxx = [i+num for i in range(3)]
    num += len(id_xxx)
    id_y = [i+num for i in range(4)]
    num += len(id_y)
    id_c = [i+num for i in range(4)]
    id_c[len(id_c)-1] = id_y[len(id_y)-1]
    num += (len(id_c)-1)
    id_N = [i+num for i in range(3)]
    num += len(id_N)
    id_t = [i+num for i in range(1)]
    num += len(id_t)
    id_r = id_xx

    return (num,id_x,id_xx,id_xxx,id_y,id_c,id_N,id_t,id_r)

if __name__ == '__main__':

    # add methods
    QState.swap = swap
    QState.ctr_swap = ctr_swap
    QState.sum = sum
    QState.i_sum = i_sum
    QState.carry = carry
    QState.i_carry = i_carry
    QState.arrow = arrow
    QState.arrow2 = arrow2
    QState.arrow3 = arrow3
    QState.plain_adder = plain_adder
    QState.i_plain_adder = i_plain_adder
    QState.modular_adder = modular_adder
    QState.i_modular_adder = i_modular_adder
    QState.ctr_modular_multiplier = ctr_modular_multiplier
    QState.i_ctr_modular_multiplier = i_ctr_modular_multiplier
    QState.modular_exponentiation = modular_exponentiation
    QState.encode = encode
    QState.decode = decode
    
    # set input numbers
    a = 2
    N = 3
    x_list = [0,1,2]

    # create registers
    num,id_x,id_xx,id_xxx,id_y,id_c,id_N,id_t,id_r = create_register()

    for x in x_list:
        
        # initialize quantum state
        qs = QState(num)
        qs.encode(x,id_x)
        qs.encode(N,id_N)
        qs.encode(1,id_xx)
            
        # execute controlled modular multiplier
        qs.modular_exponentiation(a,N,id_x,id_xx,id_xxx,id_y,id_c,id_N,id_t)
        res = qs.decode(id_r)
        print("{0:}^{1:} mod {2:} -> {3:}".format(a,x,N,res))

        # qs.free()
