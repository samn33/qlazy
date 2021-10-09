from qlazy import QState

Lattice = [{'edge': 0, 'faces':[0, 6], 'vertices':[0, 1]},
           {'edge': 1, 'faces':[1, 7], 'vertices':[1, 2]},
           {'edge': 2, 'faces':[2, 8], 'vertices':[0, 2]},
           {'edge': 3, 'faces':[0, 2], 'vertices':[0, 3]},
           {'edge': 4, 'faces':[0, 1], 'vertices':[1, 4]},
           {'edge': 5, 'faces':[1, 2], 'vertices':[2, 5]},
           {'edge': 6, 'faces':[0, 3], 'vertices':[3, 4]},
           {'edge': 7, 'faces':[1, 4], 'vertices':[4, 5]},
           {'edge': 8, 'faces':[2, 5], 'vertices':[3, 5]},
           {'edge': 9, 'faces':[3, 5], 'vertices':[3, 6]},
           {'edge':10, 'faces':[3, 4], 'vertices':[4, 7]},
           {'edge':11, 'faces':[4, 5], 'vertices':[5, 8]},
           {'edge':12, 'faces':[3, 6], 'vertices':[6, 7]},
           {'edge':13, 'faces':[4, 7], 'vertices':[7, 8]},
           {'edge':14, 'faces':[5, 8], 'vertices':[6, 8]},
           {'edge':15, 'faces':[6, 8], 'vertices':[0, 6]},
           {'edge':16, 'faces':[6, 7], 'vertices':[1, 7]},
           {'edge':17, 'faces':[7, 8], 'vertices':[2, 8]}]

F_OPERATORS = [{'face':0, 'edges':[ 0,  3,  4,  6]},
               {'face':1, 'edges':[ 1,  4,  5,  7]},
               {'face':2, 'edges':[ 2,  3,  5,  8]},
               {'face':3, 'edges':[ 6,  9, 10, 12]},
               {'face':4, 'edges':[ 7, 10, 11, 13]},
               {'face':5, 'edges':[ 8,  9, 11, 14]},
               {'face':6, 'edges':[ 0, 12, 15, 16]},
               {'face':7, 'edges':[ 1, 13, 16, 17]},
               {'face':8, 'edges':[ 2, 14, 15, 17]}]

V_OPERATORS = [{'vertex':0, 'edges':[ 0,  2,  3, 15]},
               {'vertex':1, 'edges':[ 0,  1,  4, 16]},
               {'vertex':2, 'edges':[ 1,  2,  5, 17]},
               {'vertex':3, 'edges':[ 3,  6,  8,  9]},
               {'vertex':4, 'edges':[ 4,  6,  7, 10]},
               {'vertex':5, 'edges':[ 5,  7,  8, 11]},
               {'vertex':6, 'edges':[ 9, 12, 14, 15]},
               {'vertex':7, 'edges':[10, 12, 13, 16]},
               {'vertex':8, 'edges':[11, 13, 14, 17]}]

LZ_OPERATORS = [{'logical_qid':0, 'edges':[0, 1,  2]},
                {'logical_qid':1, 'edges':[3, 9, 15]}]

LX_OPERATORS = [{'logical_qid':0, 'edges':[0, 6, 12]},
                {'logical_qid':1, 'edges':[3, 4,  5]}]

class MyQState(QState):
    
    def Lz(self, q):

        [self.z(i) for i in LZ_OPERATORS[q]['edges']]
        return self
        
    def Lx(self, q):

        [self.x(i) for i in LX_OPERATORS[q]['edges']]
        return self

def make_logical_zero():

    qs = MyQState(19)  # data:18 + ancilla:1

    mvals = [0, 0, 0, 0, 0, 0, 0, 0, 0] # measured values of 9 plaquette operators
    for vop in V_OPERATORS: # measure and get measured values of 9 star operators
        qid = vop['edges']
        qs.h(18).cx(18,qid[0]).cx(18,qid[1]).cx(18,qid[2]).cx(18,qid[3]).h(18)
        mvals.append(int(qs.m(qid=[18]).last))
        qs.reset(qid=[18])
        
    return qs, mvals

def measure_syndrome(qs, mvals):

    syn = []
    for fop in F_OPERATORS:  # plaquette operators
        qid = fop['edges']
        qs.h(18).cz(18,qid[0]).cz(18,qid[1]).cz(18,qid[2]).cz(18,qid[3]).h(18)
        syn.append(int(qs.m(qid=[18]).last))
        qs.reset(qid=[18])
        
    for vop in V_OPERATORS:  # start operators
        qid = vop['edges']
        qs.h(18).cx(18,qid[0]).cx(18,qid[1]).cx(18,qid[2]).cx(18,qid[3]).h(18)
        syn.append(int(qs.m(qid=[18]).last))
        qs.reset(qid=[18])
        
    for i in range(len(syn)): syn[i] = syn[i]^mvals[i]

    return syn

def get_error_chain(syn):

    face_id = [i for i,v in enumerate(syn) if i < 9 and v == 1]
    vertex_id = [i-9 for i,v in enumerate(syn) if i >= 9 and v == 1]

    e_chn = []
    if face_id != []:  # chain type: X
        for lat in Lattice:
            if lat['faces'][0] == face_id[0] and lat['faces'][1] == face_id[1]:
                e_chn.append({'type':'X', 'qid':[lat['edge']]})
                break

    if vertex_id != []: # chain type: Z
        for lat in Lattice:
            if lat['vertices'][0] == vertex_id[0] and lat['vertices'][1] == vertex_id[1]:
                e_chn.append({'type':'Z', 'qid':[lat['edge']]})
                break

    return e_chn

def error_correction(qs, e_chn):

    for c in e_chn:
        if c['type'] == 'X': [qs.x(i) for i in c['qid']]
        if c['type'] == 'Z': [qs.z(i) for i in c['qid']]

if __name__ == '__main__':

    print("* initial state: logical |11>")
    qs_ini, mval_list = make_logical_zero()  # logical |00>
    qs_ini.Lx(0).Lx(1)  # logical |00> -> |11>
    qs_fin = qs_ini.clone()  # for evaluating later

    print("* add noise")
    qs_fin.x(7)  # bit flip error at #7
    # qs_fin.z(7).x(7)  # bit and phase flip error at #7

    syndrome = measure_syndrome(qs_fin, mval_list)
    err_chain = get_error_chain(syndrome)
    print("* syndrome measurement:", syndrome)
    print("* error chain:", err_chain)

    error_correction(qs_fin, err_chain)
    print("* fidelity after error correction:", qs_fin.fidelity(qs_ini))
