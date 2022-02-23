# Change Log

## [0.2.4] - 2022-02-24
### Changed
- default device of IBMQ backend: qasm_simulator -> aer_simulator
### Added
- get stats of quantum circuit (frequency of each gate etc)
- generate random quantum circuit
- dump and load quntum circuit file
- import/export OpenQASM 2.0 string/file
- quantum circuit optimization by ZX-calculus (using pyzx)
- equivalent judgement of 2 quantum circuits by ZX-calculus (using pyzx)
### Removed
- u1,u2,u3,cu1,cu2,cu3 gates

## [0.2.3] - 2022-01-14
### Added
- QCirc class (quantum circuit)
- Result class (result of quantum circuit execution)
- 'measure' method of QState, Stabilizer (one shot measuremant in computational basis)
- example of "Lattice Surgery"
### Changed
- Backend class (add run method to execute quantum circuit)
### Removed
- QComp class

## [0.2.2] - 2021-10-09
### Changed
- possible to create subclass of QState, DensOp, Stabilizer etc
### Fixed
- 'apply' method of QState, DensOp
- 'patrace','partial','reset' method of DensOp

## [0.2.1] - 2021-09-01
### Changed
- performance improvement (reduce 'memcpy' etc)
- no need to call 'free' method (free automatically, use 'del' to free memory explicitly)
- create 'Stabilizer' instance with list of pauli products
### Added
- 'PauliProduct' class and 'operate' method (to operate pauli product to quantum state)
- 'join' method (for making tensor product of many quantum states)
- elapsed time option (-etm) for command line tool ($ qlazy -qc foo.qc -etm)

## [0.2.0] - 2021-05-25
### Changed
- Quick install supported: "pip install qlazy"
- Python package name changed: 'qlazypy' --> 'qlazy'
### Added
- New option added: 'nonzero' option of 'show' method (for printing only non-zero elements)
    - ex) qs = QState(2).h(0).cx(0,1); qs.show(nonzero=True)

## [0.1.5] - 2021-05-12
### Changed
- Performance improvement: use OpenMP, reduce malloc/free functions etc
- Backend API: specify 'name' only -> specify 'name' and 'device
### Added
- Backend: ibmq
- Example of T gate operation with clifford and measurement (T_gate.py)

## [0.1.4] - 2021-04-03
### Added
- Backend: qulacs, qulacs-gpu

## [0.1.3] - 2021-02-12
### Added
- example of surface code with QComp class (braiding_hadamard.py)
### Fixed
- bug fix: run_qlazy.py

## [0.1.2] - 2021-01-18
### Added
- QComp class - quantum computer
- Backend class - backend quantum device (support qlazy simulator only)
- Register tools
### Fixed
- bug fix: s_dg operation in Stabizer

## [0.1.1] - 2020-09-24
### Added
- Stablizer class
- example of defect braiding with surface code

## [0.1.0] - 2020-07-27
### Added
- add example of error correction with surface code (toric code)
### Changed
- update tutorials

## [0.0.41] - 2020-06-27
- add function(py): MData - last, frequency
- add example(py): fault tolerant

## [0.0.40] - 2020-06-07
- docstring
  - refactoring(py): QState.py,MData.py,DensOp.py,Observable.py
  - remove function(py): QState - m_is_zero, m_is_one

## [0.0.39] - 2020-05-30
- add function(py): QState - add_methods (add custom gates)
- add function(py): DensOp - add_methods (add custom gates)
- add example(py): stabilizer code

## [0.0.38] - 2020-04-15
- add function(py): QState - schmidt_decomp, schmidt_coef
- refactoring(py): error.py
- updata tutorial

## [0.0.37] 2020-03-19
- add option(c/py): DensOp - reset (reset partial qubits)
- update(doc): Tutorials (Tutorial_py, etc)
- add example(py): steane code

## [0.0.36] - 2020-03-10
- add function(py): load darwin library

## [0.0.35] - 2020-03-05
- refactoring(c): qstate.c
- add function(py): DensOp - reset
- add example(py): error correction (hamming code)
- change name(c): libQlazy.so -> libqlz.so

## [0.0.34] - 2020-02-10
- add function(py): DensOp - bit_flip, phase_flip, bit_phase_flip, depolarize, amp_dump, phase_dump
- change spec(py): DensOp - __new__ ('qubit_num' option -> create |00..0><00..0|)
- add example(py): error correction (shor code)

## [0.0.33] - 2020-02-05
- change spec(py): QState - m,mx,my,mz,mb (add 'tag' option)
- change spec(py): QState - m_freq, m_value, m_bit, m_is_zero, m_is_one (refer to 'tag')
- change spec(py): all measurement methods (default 'shots' value changed 100 -> 1)
- add function(py): QState - reset (reset quantum state |i> to |0>)
- add function(py): QState - free_all
- add function(py): DensOp - free_all
- change spec(py): QState - argument name 'id' changed to 'qid'
- change spec(py): DensOp - argument name 'id' changed to 'qid'
- change spec(py): QState - inpro, fidelity (for partial system)
- change spec(py): DensOp - distance, fidelity (for partial system)
- correct example(py): hadamard test

## [0.0.32] - 2020-01-25
- unittest
- change spec(py): QState - mcx
- change spec(py): DensOp - mcx
- change directories of examples(py): structures and 'test.sh'
- correct exapmple(py): hadamard test
- correct exapmple(py): purification
- add function(py): QState - partial (extract partial quantum state)
- bug fix(py): DensOp - relative_entropy
- bug fix(py): rx

## [0.0.31] - 2020-01-15
- add function(py): QState - add_method (add custom gate)
- add function(py): QState - create_register
- add function(py): QState - init_register
- add function(py): QState - mcx (multi-controlled X gate)
- add function(py): QState - fidelity (abs. value of the inner product)
- add function(py): QState - composite (make composite quantum state)
- add function(py): DensOp - composite (make composite density operator)
- add function(py): MData - __str__ (print MData instance)
- change spec(py): DensOp - __init__ (set equal prob., if 'prob' is not specified)
- add example(py): quantum state tomograpy
- add example(py): data compression (shannon)
- add example(py): data compression (schumacher)
- bug fix(c): interactive mode ('segmentation fault' issue of 'init 0')
- bug fix(c): densop_copy

## [0.0.30] - 2019-12-21
- add function(c/py): gate operation for densop
- add function(c/py): tensor product for densop
- bug fix(c/py): cu1,cu2,cu3,densop_init

## [0.0.29] - 2019-12-12
- add function(c/py): cu1,cu2,cu3
- add example(py): holevo
- bug fix(py): Densop class - mix

## [0.0.28] - 2019-11-29
- add function(py): DensOp class - spectrum
- add function(py): DensOp class - entropy,cond_entropy,mutual_info,relative_entropy
- add example(py): trace distance, entropy

## [0.0.27] - 2019-10-28
- add example(py): fidelity
- add function(py): DensOp class - fidelity,distance

## [0.0.26] - 2019-10-11
- add function(c/py): qstate_init, QState.__new__ (create from a vector)
- add example(py): Schmidt decomposition

## [0.0.25] - 2019-10-04
- add function(py): Densop.instrument
- add function(py): Densop.expect
- add function(c): swap gate (sw)
- add function(py): swap gate (sw), fredkin gate (csw)
- add function(c/py): U1,U2,U3 gate (u1,u2,u3)
- change spec(py): Densop.__new__
- change spec(c): densop_probability,densop_apply_matrix
- change spec(py): DensOp.probability,DensOp.apply
- bug fix(c/py): densop_sqtrace, DensOp.sqtrace
- refactoring(c): qstate,gbank,...
- add example(py): QChannel/amplitude_dumping.py

## [0.0.24] - 2019-09-17
- update(doc): Tutorial_py.md - DensOp class
- bug fix(c/py): densop_apply_matrix, DensOp.apply
- change spec(c): qstate_apply_matrix
- add function(c) densop_add,densop_mul,densop_measure_kraus,densop_measure_povm
- add function(py) DensOp.add,DensOp.mul,DensOp.measure,DensOp.mix
- add function(c/py): densop_get_amp, DensOp.get_amp
- add example(py): Measure/povm.py

## [0.0.23] - 2019-09-04
- bug fix(c/py): densop_init, DensOp.__new__
- bug fix(c/py): get_camp, QState.get_amp

## [0.0.22] - 2019-09-01
- add function(c/py): for density operator

## [0.0.21] - 2019-08-24
- change spec(c): qlazy command ... quantum circuit file from stdin (qlazy -i option)
- bug fix(py): find 'libc.so'
- refactoring(py): 'QState' class

## [0.0.20] - 2019-08-19
- bug fix(py): bell-measurement (qlazypy)
- add example(py): Deutsh-Jozsa, Grover, Toffoli(n-qubit)

## [0.0.19] - 2019-07-25
- add functions(c/py): six controlled gates: cxr,cxr+,cs,cs+,ct,ct+
- add example(py): logical function -> quantum oracle

## [0.0.18] - 2019-07-18
- add function(c/py): apply matrix
- add example(py): shor's algorithm

## [0.0.17] - 2019-07-08
- add examples(py): arithmetic operators

## [0.0.16] - 2019-06-17
- bug fix(c/py): 'show' function

## [0.0.15] - 2019-06-07
- add examples(py): qft

## [0.0.14] - 2019-06-04
- add functions(c/py): some controlled unitary gates and tensor product of quantum states

## [0.0.13] - 2019-05-26
- change spec(c): error handling

## [0.0.12] - 2019-05-22
- change spec(c): some c-functions

## [0.0.11] - 2019-05-21
- add function(c/py): get bloch angles

## [0.0.10] - 2019-05-15
- bug fix(c/py): constant term of observable
- update(doc): tutorials

## [0.0.9] - 2019-05-14
- add function(c/py): time evolution, expectation value
- bug fix(c/py): definition of pauli Y

## [0.0.8] - 2019-04-27
- add Tutorial(doc)

## [0.0.7] - 2019-04-26
- bug fix(c/py): measure some qubits
- qlazypy(py): implement destructor of QState

## [0.0.6] - 2019-04-17
- bug fix(py): show of measured data

## [0.0.5] - 2019-04-16
- bug fix(c/py): 'show' command.
- change specification of 'show' command.
  - normalize that amplitude of |00..0> is real and positive value.
  - eliminate phase factor.
- add 2-qubit Bell-measurement (mb).
- qlazypy: "from qlazypy import QState" available.
- qlazypy: add 'get_amp()' method
- qlazypy: no need to md.free()

## [0.0.4] - 2019-04-12
- add option to 'show' command (select some qubits).
- add new measurement gates (mx,my,mz).

## [0.0.3] - 2019-04-08
- measurement from any direction

## [0.0.2] - 2019-04-03
- make -> cmake

## [0.0.1] - 2019-04-01
- initial version
