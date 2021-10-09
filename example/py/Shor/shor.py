import sys
import random
import math
import numpy as np
from qlazy import QState

#
# custom gates
#

class MyQState(QState):
    
    def swap(self,q0,q1):

        self.cx(q0,q1).cx(q1,q0).cx(q0,q1)
        return self

    def hadamard(self,id=None):

        for i in range(len(id)):
            self.h(id[i])
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

    def mod_exp(self,a,N,id_up,id_dn):

        # make unitary matrix: |k>|t>->|k>|a^k t mod N>
    
        bitnum_up = len(id_up)
        bitnum_dn = len(id_dn)
    
        matdim_up = 2**bitnum_up
        matdim_dn = 2**bitnum_dn
        matdim = matdim_up * matdim_dn

        mat = np.array([[0]*matdim]*matdim)
        for j in range(matdim_up):
            for k in range(matdim_dn):
                col = matdim_dn*j + k
                if k < N:
                    row = matdim_dn*j + ((a**j)*k)%N
                else:
                    row = col
                mat[row][col] = 1.0

            # apply unitary matrix(mat) to the quantum state

        self.apply(mat)
    
        return self

#
# functions
#

def create_register(num):

    return [0]*num

def init_register(*args):

    idx = 0
    for i in range(len(args)):
        for j in range(len(args[i])):
            args[i][j] = idx
            idx += 1
    return idx

def approx_frac(number):

    iter = 10
    eps = 0.0001

    # if input number is integer
    if number == int(number):
        return (int(number),1)
    
    # expand continued fraction
    x = number
    confra = []
    for i in range(iter):
        a = int(x)
        confra.append(a)
        x -= a
        if x < eps:
            break
        x = 1/x

    # approximate fraction (get denominator,numerator)
    denom_0, numer_0 = confra[0], 1
    denom_1, numer_1 = confra[1] * denom_0 + 1, confra[1]
    denom, numer = denom_1, numer_1
    for i in range(2,len(confra)):
        denom, numer = confra[i]*denom_1+denom_0, confra[i]*numer_1+numer_0
        denom_0, denom_1 = denom_1, denom
        numer_0, numer_1 = numer_1, numer

    return (denom, numer)
    
def discover_order(a,N):

    bitnum_dn = len(str(bin(N-1)))-2
    # bitnum_up = 2*bitnum_dn + 1
    bitnum_up = 4
    id_up = create_register(bitnum_up)
    id_dn = create_register(bitnum_dn)
    qubit_num = init_register(id_up,id_dn)
    
    qs = MyQState(qubit_num)
    qs.hadamard(id_up)
    qs.x(id_dn[0])
    qs.mod_exp(a,N,id_up,id_dn)

    qs.iqft(id_up)
    md = qs.m(id_up,shots=100)

    order = 1
    for i in range(len(md.frq)):
        if md.frq[i] != 0:
            s_r = i/(2**bitnum_up)  # s/r
            (s,r) = approx_frac(s_r)
            if r != 0 and r < N and (a**r)%N == 1 and r%2 == 0:
                order = r
                break
    
    return r  # return 1 if order discovery failure

def discover_order2(a,N):
    
    for i in range(1,N):
        x = (a**i)%N
        if x == 1:
            break
    return i

def is_prime(number):

    if number == 1:
        return False
    for i in range(2,int(math.sqrt(number)+1)):
        if number%i == 0:
            return False
    return True
        
def base_exponent(number):

    size = len(str(bin(number)))-2
    for exp in reversed(range(1,size)):
        bas = int(math.pow(number,1/exp))
        if bas**exp == number:
            break
    return bas,exp
    
def shor(N):

    # if N <= 1
    if N <= 1:
        print("N must be bigger than 1")
        sys.exit()
        
    # if N is prime
    if is_prime(N) == True:
        print("N is prime")
        sys.exit()
    
    # if N is even, then factor->2
    if N%2 == 0:
        print("N is even")
        return 2
    
    # if N = bas^exp, then factor->bas
    bas,exp = base_exponent(N)
    if exp != 1:
        print("N is {0:}^{1:}, factor -> {0:}".format(bas,exp))
        return bas

    # otherwise
    for _ in range(10):
        a = random.randint(2,N-1)
        print(">> try a = ", a)
        fac = math.gcd(a,N)
        print("gcd({0:},{1:}) -> {2:}".format(a,N,fac))
        if fac != 1:
            print("factor -> ",fac)
            break
        else:
            print("order discovery start")
            r = discover_order(a,N)
            # r = discover_order2(a,N)
            print("order -> ", r)

            if r%2 != 0:
                print("order discovery failure")
                continue

            fac = math.gcd(int(a**(r/2))-1,N)
            if fac != 1 and fac != N:
                print("factor -> ",fac)
                break
            fac = math.gcd(int(a**(r/2))+1,N)
            if fac != 1 and fac != N:
                print("factor -> ",fac)
                break
            print("factor estimation failure")

    return fac

if __name__ == '__main__':

    print("== input number ==")
    # args = sys.argv
    # N = int(args[1])
    N = 57
    print("N = ",N)

    print("== Shor's algorithm start ==")
    fac_0 = shor(N)
    fac_1 = N // fac_0

    print("== factorization ==")
    print("N = {0:} = {1:} * {2:}".format(N,fac_0,fac_1))
