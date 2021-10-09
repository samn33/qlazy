from qlazy import QState

def logical_zero():

    anc = [0,1,2,3,4,5,6]     # registers for ancila
    cod = [7,8,9,10,11,12,13] # registers for steane code
    qs_total = QState(14)

    # g1
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cx(anc[0], cod[3]).cx(anc[1], cod[4]).cx(anc[2], cod[5]).cx(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.z(cod[0]).z(cod[1]).z(cod[2]).z(cod[3])
    qs_total.reset(qid=anc)

    # g2
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cx(anc[0], cod[1]).cx(anc[1], cod[2]).cx(anc[2], cod[5]).cx(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.z(cod[0]).z(cod[1]).z(cod[4]).z(cod[5])
    qs_total.reset(qid=anc)

    # g3
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cx(anc[0], cod[0]).cx(anc[1], cod[2]).cx(anc[2], cod[4]).cx(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.z(cod[2]).z(cod[4]).z(cod[6])
    qs_total.reset(qid=anc)

    # g4
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cz(anc[0], cod[3]).cz(anc[1], cod[4]).cz(anc[2], cod[5]).cz(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.x(cod[0]).x(cod[1]).x(cod[2]).x(cod[3])
    qs_total.reset(qid=anc)
    
    # g5
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cz(anc[0], cod[1]).cz(anc[1], cod[2]).cz(anc[2], cod[5]).cz(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.x(cod[0]).x(cod[1]).x(cod[4]).x(cod[5])
    qs_total.reset(qid=anc)

    # g6
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.cz(anc[0], cod[0]).cz(anc[1], cod[2]).cz(anc[2], cod[4]).cz(anc[3], cod[6])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,4)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': qs_total.x(cod[2]).x(cod[4]).x(cod[6])
    qs_total.reset(qid=anc)

    # g7
    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,7)]
    [qs_total.cz(anc[i], cod[i]) for i in range(7)]
    [qs_total.cx(anc[0], anc[i]) for i in range(1,7)]
    qs_total.h(anc[0])
    mval = qs_total.m(qid=[anc[0]]).last
    if mval == '1': [qs_total.x(q) for q in cod]
    qs_total.reset(qid=anc)

    qs = qs_total.partial(qid=cod)

    return qs

def faulttolerant_t(qs_in):

    A = [0,1,2,3,4,5,6]         # registers for ancila
    B = [7,8,9,10,11,12,13]     # registers for output quantum state
    C = [14,15,16,17,18,19,20]  # registers for input quantum state
    qs_A = QState(7)
    qs_B = logical_zero()
    qs_AB = qs_A.tenspro(qs_B)
    qs_ABC = qs_AB.tenspro(qs_in)

    # -H-T-
    qs_ABC.h(A[0])
    [qs_ABC.cx(A[0], A[i]) for i in range(1,7)]
    [qs_ABC.cx(A[i],B[i]).cs(A[i],B[i]).cz(A[i],B[i]) for i in range(7)]
    [qs_ABC.cx(A[0], A[i]) for i in range(1,7)]
    qs_ABC.t_dg(A[0]).h(A[0])
    mval = qs_ABC.m(qid=[A[0]]).last
    if mval == '1': [qs_ABC.z(q) for q in B]
    qs_ABC.reset(qid=A)

    # -CNOT-
    [qs_ABC.cx(B[i], C[i]) for i in range(7)]
    
    # -M-, -SX-
    qs_ABC.h(A[0])
    [qs_ABC.cx(A[0], A[i]) for i in range(1,7)]
    [qs_ABC.cz(A[i],C[i]) for i in range(7)]
    [qs_ABC.cx(A[0], A[i]) for i in range(1,7)]
    qs_ABC.h(A[0])
    mval = qs_ABC.m(qid=[A[0]]).last
    if mval == '1': [qs_ABC.x(q).s(q).z(q) for q in B]

    qs_out = qs_ABC.partial(qid=B)

    return qs_out

def faulttolerant_m(qs_in):

    anc = [0,1,2,3,4,5,6]      # ancila
    cod = [7,8,9,10,11,12,13]  # steane code
    qs_anc = QState(7)
    qs_total = qs_anc.tenspro(qs_in)

    qs_total.h(anc[0])
    [qs_total.cx(anc[0], anc[i]) for i in range(1,7)]
    [qs_total.cz(anc[i], cod[i]) for i in range(7)]
    [qs_total.cx(anc[0], anc[i]) for i in range(1,7)]
    qs_total.h(anc[0])
    md = qs_total.m(qid=[0], shots=10000)

    return md

if __name__ == '__main__':

    qs = QState(1).h(0).t(0).h(0)    # not fault-tolerant -HTH-
    qs.show()
    
    qs_ini = logical_zero()          # make initial state (logical zero)
    [qs_ini.h(i) for i in range(7)]  # operate fault-tolerant H
    qs_fin = faulttolerant_t(qs_ini) # operate fault-tlerant T
    [qs_fin.h(i) for i in range(7)]  # operate fault-tolerant H
    md = faulttolerant_m(qs_fin)     # execute fault-tolerant measurement
    print(md.frequency)
