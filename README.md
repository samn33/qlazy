qlazy
=====

[![Downloads](https://pepy.tech/badge/qlazy)](https://pepy.tech/project/qlazy)

Quantum Computing Simulator

## Feature

- Simple quantum calculation using command line tool is possible.
- Quantum state operation or quantum circuit execution is possible with Python package.
- Support four types of quantum states: 1) quantum state vector, 2) density operator, 3) stabilizer state, 4) matrix product state.
- Other quantum computing services or simulators can be used as backend (followings are supported).
    - [qulacs](https://github.com/qulacs/qulacs)
    - [IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)
    - [Amazon Braket(LocalSimulator,AWS,IonQ,Rigetti,OQC)](https://aws.amazon.com/braket/?nc1=h_ls)
- High-speed quantum circuit execution using GPU is possible (build from source code).

## Install

### Quick install

    $ pip install qlazy

### Build from source code

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy
    $ python setup.py install --user

You may also need to install 'libreadline-dev'

    $ sudo apt install libreadline-dev

If you want to use GPU version

    $ python setup_gpu.py install --user

### Uninstall

    $ pip uninstall qlazy

## Usage

### Command line tool (for state vector simulation)

#### read file

foo.qc

    init 2
    h 0
    cx 0 1
	show

run the circuit

    $ qlazy -qc foo.qc
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

print help
	
    $ qlazy -h

#### interactive mode

    $ qlazy
    >> init 2
    >> h 0
    >> cx 0 1
    >> show   # show the current quantum state
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
    >> m
    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00
    >> quit

print help

    >> help
    >> help <item>

### Python package

#### State Vector Simulation (by QState class)

    >>> from qlazy import QState
    >>> qs = QState(2)
    >>> qs.h(0).cx(0,1)
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
    >>> md = qs.m(shots=100)
    >>> print(md.frequency)
    Counter({'00':53,'11':47})

#### Quantum Circuit Execution (by QCirc and Backend class)

    >>> # quantum state vector simulator
    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
    >>> result = bk.run(qcirc=qc, shots=100)
    >>> print(result.frequency)
	Counter({'00':52, '11':48})

    >>> # quantum state vector simulator (GPU)
    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_gpu_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
    >>> result = bk.run(qcirc=qc, shots=100)
    >>> print(result.frequency)
	Counter({'00':54, '11':46})

    >>> # stabilizer state simulator
    >>> bk = Backend(product='qlazy', device='stabilizer_simulator')
    >>> qc = QCirc().h(0)
    >>> [qc.cx(i,i+1) for i in range(49)]
    >>> qc.measure(qid=list(range(50)), cid=list(range(50)))
    >>> result = bk.run(qcirc=qc, shots=100)
    >>> print(result.frequency)
    Counter({'00000000000000000000000000000000000000000000000000': 52, '11111111111111111111111111111111111111111111111111': 48})

    >>> # matrix product state simulator
    >>> bk = Backend(product='qlazy', device='mps_simulator')
    >>> qc = QCirc().h(0)
    >>> [qc.cx(i,i+1) for i in range(49)]
    >>> qc.measure(qid=list(range(50)), cid=list(range(50)))
    >>> result = bk.run(qcirc=qc, shots=100)
    >>> print(result.frequency)
    Counter({'11111111111111111111111111111111111111111111111111': 57, '00000000000000000000000000000000000000000000000000': 43})

#### Other classes

- DensOp class: for operating density operator.
- Stabilizer class: for operating stabilizer state.
- MPState class: for operating matrix product state.
- Observable class: for specifying observable.
- PauliProduct: for specifying pauli product.

## Documents

- [Welcome to qlazy's documentations!](http://samn33.github.io/qlazy-docs/index.html)
    - [Tutorial (japanese)](http://samn33.github.io/qlazy-docs/Tutorial_jp.html)
    - [Python API](http://samn33.github.io/qlazy-docs/python-api/qlazy.html)

## Requirements

- Linux (Ubuntu 20.04 LTS)
- Python 3.8
- numpy 1.21.0

Optional ...
- pyzx 0.7.0 (to use quantum circuit optimization with ZX-calculus)
- Qulacs 0.3.0 (to use qulacs backend)
- qiskit 0.37.0 (to use IBMQ backend)
- amazon-braket-sdk 1.25.2 (to use amazon braket backend)
- tensornetwork 0.4.6 (to use matrix product state simulation)
- cuda 11 (to use GPU version)

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
