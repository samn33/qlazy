from collections import Counter
from qlazy import Stabilizer

def get_common_qid(obj_A, obj_B):

    return list(set(obj_A['dat']) & set(obj_B['dat']))

def create_lattice(row, col):

    face = [[None]*col for _ in range(row)]
    vertex = [[None]*(col+1) for _ in range(row+1)]

    q_row = 2 * row + 1
    q_col = 2 * col + 1
    q_id = 0
    for i in range(q_row):
        for j in range(q_col):
            if i%2 == 1 and j%2 == 1: # face
                dat = []
                dat.append((i - 1) * q_col + j)  # up
                dat.append((i + 1) * q_col + j)  # down
                dat.append(i * q_col + (j - 1))  # left
                dat.append(i * q_col + (j + 1))  # right
                face[i//2][j//2] = {'anc': q_id, 'dat': dat}
            elif i%2 == 0 and j%2 == 0: # vertex
                dat = []
                if i > 0: dat.append((i - 1) * q_col + j)          # up
                if i < q_row - 1: dat.append((i + 1) * q_col + j)  # down
                if j > 0: dat.append(i * q_col + (j - 1))          # left
                if j < q_col - 1: dat.append(i * q_col + (j + 1))  # right
                vertex[i//2][j//2] = {'anc': q_id, 'dat': dat}
            q_id += 1
            
    return {'face': face, 'vertex': vertex}

def initialize(sb, lattice):

    sb.set_all('Z')
    for face_list in lattice['face']:
        for face in face_list:
            sb.h(face['anc'])
            [sb.cz(face['anc'], target) for target in face['dat']]
            sb.h(face['anc'])
            sb.m(qid=[face['anc']])

    for vertex_list in lattice['vertex']:
        for vertex in vertex_list:
            sb.h(vertex['anc'])
            [sb.cx(vertex['anc'], target) for target in vertex['dat']]
            sb.h(vertex['anc'])
            sb.m(qid=[vertex['anc']])

def create_move_defect_p(sb, pos_A, pos_B, path, lattice):

    # create defect pair
    face_A = lattice['face'][pos_A[0]][pos_A[1]]
    face_B = lattice['face'][pos_B[0]][pos_B[1]]
    q = get_common_qid(face_A, face_B)[0]
    md = sb.h(q).m(qid=[q])
    sb.h(q)
    if md.last == '1': [sb.z(i) for i in face_B['dat']]
 
    # move defect
    chain = [q]
    for i in range(1,len(path)):
        # extend defect
        face_A = lattice['face'][path[i-1][0]][path[i-1][1]]
        face_B = lattice['face'][path[i][0]][path[i][1]]
        q = get_common_qid(face_A, face_B)[0]
        md = sb.h(q).m(qid=[q])
        sb.h(q)
        if md.last == '1': [sb.z(i) for i in face_B['dat']]
                
        # remove defect
        sb.h(face_A['anc'])
        [sb.cz(face_A['anc'], target) for target in face_A['dat']]
        sb.h(face_A['anc'])
        md = sb.m(qid=[face_A['anc']])
        if md.last == '1': [sb.x(i) for i in chain]
            
        chain.append(q)

def create_move_defect_d(sb, pos_A, pos_B, path, lattice):

    # create defect pair
    vertex_A = lattice['vertex'][pos_A[0]][pos_A[1]]
    vertex_B = lattice['vertex'][pos_B[0]][pos_B[1]]
    q = get_common_qid(vertex_A, vertex_B)[0]
    md = sb.m(qid=[q])
    if md.last == '1': [sb.x(i) for i in vertex_B['dat']]
 
    # move defect
    chain = [q]
    for i in range(1,len(path)):
        # extend defect
        vertex_A = lattice['vertex'][path[i-1][0]][path[i-1][1]]
        vertex_B = lattice['vertex'][path[i][0]][path[i][1]]
        q = get_common_qid(vertex_A, vertex_B)[0]
        md = sb.m(qid=[q])
        if md.last == '1': [sb.x(i) for i in vertex_B['dat']]
                
        # remove defect
        sb.h(vertex_A['anc'])
        [sb.cx(vertex_A['anc'], target) for target in vertex_A['dat']]
        sb.h(vertex_A['anc'])
        md = sb.m(qid=[vertex_A['anc']])
        if md.last == '1': [sb.z(i) for i in chain]
            
        chain.append(q)

def get_chain(pos_list, lattice):

    chain = []
    for i in range(1,len(pos_list)):
        pos_A = pos_list[i-1]
        pos_B = pos_list[i]
        chain.append(get_common_qid(lattice['vertex'][pos_A[0]][pos_A[1]],
                                    lattice['vertex'][pos_B[0]][pos_B[1]])[0])
    return chain
    
def measure_logical_Z(sb, face, chain, shots=10):

    mval_list = []
    for _ in range(shots):
        sb_tmp = sb.clone()
        mval_0 = sb_tmp.m(qid=face['dat']).last
        mval_1 = sb_tmp.m(qid=chain).last
        mval = (str(sum([int(s) for s in list(mval_0)])%2)
                + str(sum([int(s) for s in list(mval_1)])%2))
        mval_list.append(mval)
        sb_tmp.free()
    return Counter(mval_list)

if __name__ == '__main__':

    lattice_row = 4
    lattice_col = 6
    lattice = create_lattice(lattice_row, lattice_col)

    # make vacuum state
    qubit_num = (2*lattice_row + 1) * (2*lattice_col + 1)
    sb = Stabilizer(qubit_num=qubit_num)
    initialize(sb, lattice)

    # logical qubit #1
    d_pos_A = [2,1]
    d_pos_B = [2,2]
    d_path = [[2,2],[2,3],[2,4]]
    create_move_defect_d(sb, d_pos_A, d_pos_B, d_path, lattice)

    # logical qubit #0
    p_pos_A = [0,0]
    p_pos_B = [0,1]
    # p_path = [[0,1],[0,2]]
    p_path = [[0,1],[0,2],[1,2],[2,2],[3,2],[3,3],[3,4],[3,5],
              [2,5],[1,5],[0,5],[0,4],[0,3],[0,2]]
    create_move_defect_p(sb, p_pos_A, p_pos_B, p_path, lattice)

    # measure logical qubits: #0 and #1
    face = lattice['face'][p_pos_A[0]][p_pos_A[1]]
    chain = get_chain([[2,1],[2,2],[2,3],[2,4]], lattice)
    freq = measure_logical_Z(sb, face, chain, shots=100)
    print(freq)

    sb.free()
