from qlazy import QState

def sum(self,q0,q1,q2):

    self.cx(q1,q2).cx(q0,q2)
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
    id_a = [i for i in range(digits)]
    num += len(id_a)
    id_b = [i+num for i in range(digits+1)]
    num += len(id_b)
    id_c = [i+num for i in range(digits+1)]
    id_c[digits] = id_b[digits]  # share the qubit id's
    num += (len(id_c)-1)
    return (num,id_a,id_b,id_c)

if __name__ == '__main__':

    # add metthods
    QState.encode = encode
    QState.decode = decode
    QState.sum = sum
    QState.carry = carry
    QState.i_carry = i_carry
    QState.plain_adder = plain_adder

    # create registers
    digits = 4
    num,id_a,id_b,id_c = create_register(digits)

    # set input numbers
    a_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    b = 12

    for a in a_list:

        # initialize quantum state
        qs = QState(num)
        qs.encode(a,id_a)
        qs.encode(b,id_b)

        # execute plain adder
        qs.plain_adder(id_a,id_b,id_c)
        res = qs.decode(id_b)
        print("{0:}+{1:} -> {2:}".format(a,b,res))

        qs.free()
