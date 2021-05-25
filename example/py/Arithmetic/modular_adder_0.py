from qlazy import QState

def swap(self,id_0,id_1):

    dim = min(len(id_0),len(id_1))
    for i in range(dim):
        self.cx(id_0[i],id_1[i]).cx(id_1[i],id_0[i]).cx(id_0[i],id_1[i])
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
    
def encode(self,decimal,id):

    for i in range(len(id)):
        if (decimal>>i)%2 == 1:
            self.x(id[i])
    return self

def decode(self,id):

    iid = id[::-1]
    return self.m(iid,shots=1).lst
    
def create_register(digits):

    num = 0
    id_a = [i for i in range(digits+1)]
    num += len(id_a)
    id_b = [i+num for i in range(digits+2)]
    num += len(id_b)
    id_c = [i+num for i in range(digits+2)]
    id_c[digits+1] = id_b[digits+1]  # share the qubit id's
    num += (len(id_c)-1)
    id_N = [i+num for i in range(2*digits-1)]
    num += len(id_N)
    id_t = [i+num for i in range(1)]
    num += len(id_t)
    id_r = id_b[:-1] # to store the result
    return (num,id_a,id_b,id_c,id_N,id_t,id_r)

if __name__ == '__main__':

    # add methods
    QState.swap = swap
    QState.sum = sum
    QState.i_sum = i_sum
    QState.carry = carry
    QState.i_carry = i_carry
    QState.arrow = arrow
    QState.plain_adder = plain_adder
    QState.i_plain_adder = i_plain_adder
    QState.modular_adder = modular_adder
    QState.encode = encode
    QState.decode = decode

    # create registers
    digits = 3
    num,id_a,id_b,id_c,id_N,id_t,id_r = create_register(digits)

    # set iput numbers
    a = 6
    b = 7
    N = 9

    # initialize quantum state
    qs = QState(num)
    qs.encode(a,id_a)
    qs.encode(b,id_b)
    qs.encode(N,id_N)
    
    # execute modular adder
    qs.modular_adder(N,id_a,id_b,id_c,id_N,id_t)
    res = qs.decode(id_r)
    print("{0:}+{1:} mod {2:} -> {3:}".format(a,b,N,res))

    qs.free()
