#
# followings must be equal to definitions in 'qlazy.h'
#

TRUE  = 1
FALSE = 0

EPS = 1e-6
INF = 1e+6

MAX_QUBIT_NUM = 30

DEF_SHOTS = 1

DEF_TAG = 'DEFAULT'

DEF_PHASE  = 0.0
DEF_ANGLE  = 0.0

BELL_PHI_PLUS  = 0
BELL_PHI_MINUS = 3
BELL_PSI_PLUS  = 1
BELL_PSI_MINUS = 2

# Kind

CIRC           = 1
GATES          = 2
SHOW           = 3
BLOCH          = 4
ECHO           = 5
OUTPUT         = 6
HELP           = 7
QUIT	       = 8
INIT           = 9
PAULI_X        = 120
PAULI_Y        = 121
PAULI_Z        = 122
ROOT_PAULI_X   = 123
ROOT_PAULI_X_  = 124
HADAMARD       = 130
PHASE_SHIFT_S  = 140
PHASE_SHIFT_S_ = 141
PHASE_SHIFT_T  = 142
PHASE_SHIFT_T_ = 143
PHASE_SHIFT    = 144
ROTATION_X     = 150
ROTATION_Y     = 151
ROTATION_Z     = 152
ROTATION_U1    = 153
ROTATION_U2    = 154
ROTATION_U3    = 155
CONTROLLED_X   = 160
CONTROLLED_Y   = 161
CONTROLLED_Z   = 162
CONTROLLED_XR  = 163
CONTROLLED_XR_ = 164
CONTROLLED_H   = 165
CONTROLLED_S   = 166
CONTROLLED_S_  = 167
CONTROLLED_T   = 168
CONTROLLED_T_  = 169
CONTROLLED_P   = 170
CONTROLLED_RX  = 171
CONTROLLED_RY  = 172
CONTROLLED_RZ  = 173
CONTROLLED_U1  = 174
CONTROLLED_U2  = 175
CONTROLLED_U3  = 176
SWAP_QUBITS    = 180
MEASURE        = 200
MEASURE_X      = 201
MEASURE_Y      = 202
MEASURE_Z      = 203
MEASURE_BELL   = 204
RESET          = 205
NOT_A_GATE     = 1000
IDENTITY       = 2000

GATE_KIND = {
    'x': PAULI_X,
    'y': PAULI_Y,
    'z': PAULI_Z,
    'xr': ROOT_PAULI_X,
    'xr_dg': ROOT_PAULI_X_,
    'h': HADAMARD,
    's': PHASE_SHIFT_S,
    's_dg': PHASE_SHIFT_S_,
    't': PHASE_SHIFT_T,
    't_dg': PHASE_SHIFT_T_,
    'p': PHASE_SHIFT,
    'rx': ROTATION_X,
    'ry': ROTATION_Y,
    'rz': ROTATION_Z,
    'u1': ROTATION_U1,
    'u2': ROTATION_U2,
    'u3': ROTATION_U3,
    'cx': CONTROLLED_X,
    'cy': CONTROLLED_Y,
    'cz': CONTROLLED_Z,
    'cxr': CONTROLLED_XR,
    'cxr_dg': CONTROLLED_XR_,
    'ch': CONTROLLED_H,
    'cs': CONTROLLED_S,
    'cs_dg': CONTROLLED_S_,
    'ct': CONTROLLED_T,
    'ct_dg': CONTROLLED_T_,
    'cp': CONTROLLED_P,
    'crx': CONTROLLED_RX,
    'cry': CONTROLLED_RY,
    'crz': CONTROLLED_RZ,
    'cu1': CONTROLLED_U1,
    'cu2': CONTROLLED_U2,
    'cu3': CONTROLLED_U3,
    'sw': SWAP_QUBITS,
    'measure': MEASURE,
    'measure_x': MEASURE_X,
    'measure_y': MEASURE_Y,
    'measure_z': MEASURE_Z,
    'measure_bell': MEASURE_BELL,
    'reset': RESET,
}

GATE_STRING = {
    PAULI_X:'x',
    PAULI_Y:'y',
    PAULI_Z:'z',
    ROOT_PAULI_X:'xr',
    ROOT_PAULI_X_:'xr_dg',
    HADAMARD:'h',
    PHASE_SHIFT_S:'s',
    PHASE_SHIFT_S_:'s_dg',
    PHASE_SHIFT_T:'t',
    PHASE_SHIFT_T_:'t_dg',
    PHASE_SHIFT:'p',
    ROTATION_X:'rx',
    ROTATION_Y:'ry',
    ROTATION_Z:'rz',
    ROTATION_U1:'u1',
    ROTATION_U2:'u2',
    ROTATION_U3:'u3',
    CONTROLLED_X:'cx',
    CONTROLLED_Y:'cy',
    CONTROLLED_Z:'cz',
    CONTROLLED_XR:'cxr',
    CONTROLLED_XR_:'cxr_dg',
    CONTROLLED_H:'ch',
    CONTROLLED_S:'cs',
    CONTROLLED_S_:'cs_dg',
    CONTROLLED_T:'ct',
    CONTROLLED_T_:'ct_dg',
    CONTROLLED_P:'cp',
    CONTROLLED_RX:'crx',
    CONTROLLED_RY:'cry',
    CONTROLLED_RZ:'crz',
    CONTROLLED_U1:'cu1',
    CONTROLLED_U2:'cu2',
    CONTROLLED_U3:'cu3',
    SWAP_QUBITS:'sw',
    MEASURE:'measure',
    MEASURE_X:'measure_x',
    MEASURE_Y:'measure_y',
    MEASURE_Z:'measure_z',
    MEASURE_BELL:'meaxure_bell',
    RESET:'reset'
}

GATE_STRING_QASM = {
    # 1-qubit
    PAULI_X:'x',
    PAULI_Z:'z',
    HADAMARD:'h',
    PHASE_SHIFT_S:'s',
    PHASE_SHIFT_S_:'sdg',
    PHASE_SHIFT_T:'t',
    PHASE_SHIFT_T_:'tdg',
    RESET:'reset',
    # 1-qubit, 1-parameter
    ROTATION_X:'rx',
    ROTATION_Z:'rz',
    # 2-qubit
    CONTROLLED_X:'cx',
    CONTROLLED_Z:'cz',
    CONTROLLED_H:'ch',
    # 2-qubit, 1-parameter
    CONTROLLED_RZ:'crz',
    # measurement
    MEASURE:'measure',
}

# MatrixType

KRAUS = 1
POVM  = 2

# ApplyDir

LEFT  = 0
RIGHT = 1
BOTH  = 2

# ComplexAxis

REAL_PLUS  = 0
IMAG_PLUS  = 1
REAL_MINUS = 2
IMAG_MINUS = 3
