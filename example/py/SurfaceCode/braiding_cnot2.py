from collections import Counter
from qlazypy import Stabilizer

XBASE = {'0':'+', '1':'-'}
OBJECT = {'p':'face', 'd':'vertex'}

def get_common_qid(obj_A, obj_B):

    return list(set(obj_A['dat']) & set(obj_B['dat']))

def get_path(pos_A, pos_B):

    path = []

    if pos_A[1] < pos_B[1]: h_list = list(range(pos_A[1], pos_B[1] + 1))
    else: h_list = list(reversed(range(pos_B[1], pos_A[1] + 1)))
    for j in h_list: path.append([pos_A[0], j])

    if pos_A[0] < pos_B[0]: v_list = list(range(pos_A[0] + 1, pos_B[0] + 1))
    else: v_list = list(reversed(range(pos_B[0], pos_A[0])))
    for i in v_list: path.append([i, pos_B[1]])

    return path

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

    i = 0  # generator id
    for face_list in lattice['face']:
        for face in face_list:
            [sb.set_pauli_op(i, q, 'Z') for q in face['dat']]
            i += 1
            sb.set_pauli_op(i, face['anc'], 'Z')
            i += 1

    for vertex_list in lattice['vertex']:
        for vertex in vertex_list:
            [sb.set_pauli_op(i, q, 'X') for q in vertex['dat']]
            i += 1
            sb.set_pauli_op(i, vertex['anc'], 'Z')
            i += 1

def get_chain(pos_list, dtype, lattice):

    chain = []
    for i in range(1,len(pos_list)):
        pos_A = pos_list[i-1]
        pos_B = pos_list[i]
        chain.append(get_common_qid(lattice[OBJECT[dtype]][pos_A[0]][pos_A[1]],
                                    lattice[OBJECT[dtype]][pos_B[0]][pos_B[1]])[0])
    return chain

def move_defect(sb, pos_A, pos_B, path, dtype, lattice, create=False, annihilate=False):

    obj = OBJECT[dtype]
    if create == True:
        obj_A = lattice[obj][pos_A[0]][pos_A[1]]
        obj_B = lattice[obj][pos_B[0]][pos_B[1]]
        q = get_common_qid(obj_A, obj_B)[0]
        if dtype == 'p':
            md = sb.mx(qid=[q])
            if md.last == '1': [sb.z(i) for i in obj_B['dat']]
        elif dtype == 'd':
            md = sb.m(qid=[q])
            if md.last == '1': [sb.x(i) for i in obj_B['dat']]
        
    chain = get_chain(get_path(pos_A, pos_B), dtype, lattice)
    for i in range(1,len(path)):
        # extend defect
        obj_A = lattice[obj][path[i-1][0]][path[i-1][1]]
        obj_B = lattice[obj][path[i][0]][path[i][1]]
        q = get_common_qid(obj_A, obj_B)[0]
        if dtype == 'p':
            md = sb.mx(qid=[q])
            if md.last == '1': [sb.z(i) for i in obj_B['dat']]
        elif dtype == 'd':
            md = sb.m(qid=[q])
            if md.last == '1': [sb.x(i) for i in obj_B['dat']]
            
        # remove defect
        sb.h(obj_A['anc'])
        if dtype == 'p': [sb.cz(obj_A['anc'], target) for target in obj_A['dat']]
        elif dtype == 'd': [sb.cx(obj_A['anc'], target) for target in obj_A['dat']]
        sb.h(obj_A['anc'])
        md = sb.m(qid=[obj_A['anc']])
        if md.last == '1':
            if dtype == 'p': [sb.x(i) for i in chain]
            elif dtype == 'd': [sb.z(i) for i in chain]
            sb.x(obj_A['anc'])

        chain.append(q)

    if annihilate == True:
        obj_A = lattice[obj][pos_A[0]][pos_A[1]]
        obj_B = lattice[obj][path[-1][0]][path[-1][1]]
        q = get_common_qid(obj_A, obj_B)[0]
        if dtype == 'p': md = sb.mx(qid=[q])
        elif dtype == 'd': md = sb.m(qid=[q])
        return md.last
    
    return None

def measure_logical_X(sb, chain_A, chain_B, shots=1):

    mval_list = []
    for _ in range(shots):
        sb_tmp = sb.clone()
        mval_A = sb_tmp.mx(qid=chain_A).last
        mval_B = sb_tmp.mx(qid=chain_B).last
        mval_A_bin = str(sum([int(s) for s in list(mval_A)])%2)
        mval_B_bin = str(sum([int(s) for s in list(mval_B)])%2)
        mval = (XBASE[mval_A_bin] + XBASE[mval_B_bin])
        mval_list.append(mval)
        sb_tmp.free()
        
    return Counter(mval_list)

def operate_logical_Z(sb, lq, lattice):

    if lq == 0: face = lattice['face'][0][0]
    elif lq == 2: face = lattice['face'][0][7]
    elif lq == 3: face = lattice['face'][6][0]
    [sb.z(q) for q in face['dat']]

def operate_logical_X(sb, lq, lattice):

    if lq == 2:
        chain = get_chain([[0,7],[1,7],[2,7],[3,7]], 'p', lattice)
        [sb.x(q) for q in chain]

def operate_logical_cnot(lq, shots=5):

    # set lattice
    lattice_row, lattice_col = 7, 8
    lattice = create_lattice(lattice_row, lattice_col)

    # make vacuum state
    qubit_num = (2 * lattice_row + 1) * (2 * lattice_col + 1)
    sb = Stabilizer(qubit_num=qubit_num, gene_num=qubit_num+1)
    initialize(sb, lattice)

    # set logical qubit #0
    p0_pos_A, p0_pos_B = [0,0], [0,1]
    p0_path = [[0,1],[0,2]]
    move_defect(sb, p0_pos_A, p0_pos_B, p0_path, 'p', lattice, create=True)
    if lq[0] == '-': operate_logical_Z(sb, 0, lattice)

    # set logical qubit #1
    d1_pos_A, d1_pos_B = [2,5], [3,5]
    d1_path = [[3,5],[4,5],[5,5]]
    move_defect(sb, d1_pos_A, d1_pos_B, d1_path, 'd', lattice, create=True)

    # set logical qubit #2
    p2_pos_A, p2_pos_B = [0,7], [1,7]
    p2_path = [[1,7],[2,7],[3,7]]
    move_defect(sb, p2_pos_A, p2_pos_B, p2_path, 'p', lattice, create=True)

    # set logical qubit #3
    p3_pos_A, p3_pos_B = [6,0], [6,1]
    p3_path = [[6,1],[6,2]]
    move_defect(sb, p3_pos_A, p3_pos_B, p3_path, 'p', lattice, create=True)
    if lq[1] == '-': operate_logical_Z(sb, 3, lattice)

    # braid logical qubit #0
    p0_pos_A, p0_pos_B = [0,0], [0,2]
    p0_path = [[0,2],[1,2],[2,2],[3,2],[3,3],[3,4],[3,5],[3,6],
               [2,6],[1,6],[0,6],[0,5],[0,4],[0,3],[0,2]]
    move_defect(sb, p0_pos_A, p0_pos_B, p0_path, 'p', lattice)
    
    # braid logical qubit #2
    p2_pos_A, p2_pos_B = [0,7], [3,7]
    p2_path = [[3,7],[3,6],[3,5],[3,4],[3,3],[4,3],[5,3],
              [6,3],[6,4],[6,5],[6,6],[6,7],[5,7],[4,7],[3,7]]
    move_defect(sb, p2_pos_A, p2_pos_B, p2_path, 'p', lattice)

    # braid and annihilate logical qubit #3
    p3_pos_A, p3_pos_B = [6,0], [6,2]
    p3_path = [[6,2],[6,3],[6,4],[6,5],[6,6],[5,6],[4,6],[3,6],
               [3,5],[3,4],[3,3],[3,2],[4,2],[5,2],[6,2],[6,1]]
    mval_p = move_defect(sb, p3_pos_A, p3_pos_B, p3_path, 'p', lattice, annihilate=True)

    # braid and annihilate logical qubit #1
    d1_pos_A, d1_pos_B = [2,5], [5,5]
    d1_path = [[5,5],[4,5],[3,5]]
    mval_d = move_defect(sb, d1_pos_A, d1_pos_B, d1_path, 'd', lattice, annihilate=True)

    if mval_p == '1':
        operate_logical_Z(sb, 0, lattice)
        operate_logical_Z(sb, 2, lattice)

    # measure logical qubits: #0 and #2
    chain_0 = get_chain(get_path([0,0],[0,2]), 'p', lattice)
    chain_2 = get_chain(get_path([0,7],[3,7]), 'p', lattice)
    freq = measure_logical_X(sb, chain_0, chain_2, shots=shots)
    print("Input('{0:}') == [CNOT] ==> {1:}".format(lq, freq))

    sb.free()

if __name__ == '__main__':

    operate_logical_cnot('++', shots=10)  # --> '++'
    operate_logical_cnot('+-', shots=10)  # --> '--'
    operate_logical_cnot('-+', shots=10)  # --> '-+'
    operate_logical_cnot('--', shots=10)  # --> '+-'
