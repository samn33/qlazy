qlazy
=====

Quantum Computing Simulator

## Feature

- Simple quantum calculations are possible with command line tool.
- Quantum state operations or quantum circuit executions are possible with Python package.
- Support three types of quantum states: 1) quantum state vector, 2) density operator, 3) stabilizer state.
- Other quantum computing services or simulators can be uesd as backend (followings are supported).
    - [qulacs](https://github.com/qulacs/qulacs)
    - [IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/)

## Install

### Quick install

    $ pip install qlazy

### Build from source code

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy
    $ python setup.py install --user

You may also need to install 'libreadline-dev'

    $ sudo apt install libreadline-dev

### Uninstall

    $ pip uninstall qlazy

### Uninstall (old version <= 0.1.5)

    $ rm ~/bin/qlazy ~/lib/libqlz.so

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

foo.py
	
    from qlazy import QState
    
    qs = QState(2)
    qs.h(0).cx(0,1)
    qs.show()
    md = qs.m(shots=100)
    print(md.frequency)

execute the program

    $ python foo.py
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
    Counter({'00':53,'11':47})

#### Quantum Circuit Execution (by QCirc and Backend class)

bar.py
	
    from qlazy import QCirc, Backend
    
    bk = Backend()
    qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
    result = bk.run(qcirc=qc, shots=100)
    print(result.frequency)

execute the program

    $ python bar.py
	Counter({'00':52, '11':48})

#### Other classes

- DensOp class: for operating density operators.
- Stabilizer class: for operating stabilizer states.
- Observable class: for specifying observables.
- PauliProduct: for operations related to pauli product.

## Documents

- [Welcome to qlazy's documentations!](http://samn33.github.io/qlazy-docs/index.html)
    - [Tutorial (japanese)](http://samn33.github.io/qlazy-docs/Tutorial_jp.html)
    - [Python API](http://samn33.github.io/qlazy-docs/python-api/qlazy.html)

## Requirements

- Linux(Ubuntu20.04)
- Python3.8

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
