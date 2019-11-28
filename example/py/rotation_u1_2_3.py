import sys
import random
import math
import cmath
import numpy as np
from qlazypy import QState

def make_qstate():

    alpha = random.uniform(0.0, 1.0)
    beta = random.uniform(0.0, 1.0)
    gamma = random.uniform(0.0, 1.0)

    qs = QState(1).rz(0,phase=beta).ry(0,phase=gamma).rz(0,phase=alpha)

    return qs

def operate_u1(vec_in, alpha=0.0):

    a = alpha * math.pi
    
    U00 = 1.0
    U01 = 0
    U10 = 0
    U11 = cmath.exp(1j*a)

    U = np.array([[U00,U01],[U10,U11]])
    vec_out = np.dot(U,vec_in)
    return vec_out

def operate_u2(vec_in, alpha=0.0, beta=0.0):

    a = alpha * math.pi
    b = beta * math.pi

    U00 = 1.0 / math.sqrt(2.0)
    U01 = -cmath.exp(1j*a)/ math.sqrt(2.0)
    U10 = cmath.exp(1j*b) / math.sqrt(2.0)
    U11 = cmath.exp(1j*(a+b))/ math.sqrt(2.0)

    U = np.array([[U00,U01],[U10,U11]])
    vec_out = np.dot(U,vec_in)
    return vec_out

def operate_u3(vec_in, alpha=0.0, beta=0.0, gamma=0.0):

    a = alpha * math.pi
    b = beta * math.pi
    g = gamma * math.pi

    U00 = math.cos(g/2.0)
    U01 = -cmath.exp(1j*a) * math.sin(g/2.0)
    U10 = cmath.exp(1j*b) * math.sin(g/2.0)
    U11 = cmath.exp(1j*(a+b)) * math.cos(g/2.0)

    U = np.array([[U00,U01],[U10,U11]])
    vec_out = np.dot(U,vec_in)
    return vec_out

def operate(vec_in, unitary=None, alpha=0.0, beta=0.0, gamma=0.0):

    vec_out = None
    if unitary == "u1":
        vec_out = operate_u1(vec_in, alpha=alpha)
    elif unitary == "u2":
        vec_out = operate_u2(vec_in, alpha=alpha, beta=beta)
    elif unitary == "u3":
        vec_out = operate_u3(vec_in, alpha=alpha, beta=beta, gamma=gamma)
    else:
        print("unknown unitary operator")
        sys.exit()
        
    return vec_out

if __name__ == '__main__':

    print("== settings ==")

    unitary = random.choice(["u1","u2","u3"])
    alpha = random.uniform(0.0, 1.0)
    beta = random.uniform(0.0, 1.0)
    gamma = random.uniform(0.0, 1.0)
    print("- unitary =", unitary)
    if unitary == "u1":
        print("- alpha =", alpha)
    elif unitary == "u2":
        print("- alpha,beta =", alpha,beta)
    elif unitary == "u3":
        print("- alpha,beta,gamma =", alpha,beta,gamma)
    else:
        print("unknown unitary operator")
        sys.exit()

    print("== initial quantum state ==")

    qs = make_qstate()
    vec_in = qs.amp
    print(vec_in)

    print("== matrix operation ==")

    vec_out = operate(vec_in, unitary=unitary,
                      alpha=alpha, beta=beta, gamma=gamma)
    print(vec_out)

    print("== quantum operation ==")

    if unitary == "u1":
        qs.u1(0, alpha=alpha)
    elif unitary == "u2":
        qs.u2(0, alpha=alpha, beta=beta)
    elif unitary == "u3":
        qs.u3(0, alpha=alpha, beta=beta, gamma=gamma)
    else:
        print("unknown unitary operator")
        sys.exit()
    qvec_out = qs.amp
    print(qvec_out)

    print("== result ==")
    diff = np.linalg.norm(qvec_out - vec_out)
    if diff < 0.0000001:
        print("OK! - diff of vectors =", diff)
    else:
        printt("NG - diff of vectors =", diff)
    
    qs.free()
