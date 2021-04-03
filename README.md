qlazy
=====

Quantum Computing Simulator

## Feature

- Command line tool to perform simple quantum calculation.
- Python package for performing complex quantum calculations.
- Supports three types of quantum states: 1) quantum state vector, 2) density operator (matrix), 3) stabilizer state.
- Other quantum computing simulators can be uesd as a backend: [qulacs/qulacs-gpu](https://github.com/qulacs/qulacs) (at present).

## Install

### Command line tool and Library ('qlazy', 'libqlz.so')

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ mkdir build; cd build; cmake ..; make
    $ mv libqlz.so ~/lib; mv qlazy ~/bin
	
add followings to your ~/.bashrc

    export PATH=$PATH:~/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/lib

You may also need to install 'libreadline-dev'

    $ sudo apt install libreadline-dev

### Python package ('qlazypy')

    $ cd ../../py
    $ pip install -e .

## Usage

### Command line tool ('qlazy')

#### read file

foo.qc

    init 2
    h 0
    cx 0 1
    m

run the circuit

    $ qlazy -qc foo.qc
    direction of measurement: z-axis
    frq[00] = 53
    frq[11] = 47
    last state => 00

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

### Python package ('qlazypy')

#### Example of QState class

foo.py
	
    from qlazypy import QState
    
    qs = QState(2)
    qs.h(0)
    qs.cx(0,1)
    qs.show()
    md = qs.m(shots=100)
    print(md.frequency)
    
    qs.free()

execute the program

    $ python foo.py
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
    Counter({{'00':53,'11':47})

#### Classes

- QState: class for operating quantum state vectors.
- DensOp: class for operating density operators.
- Stabilizer: class for operating stabilizer states.
- Observable: class for specifying observables.
- QComp, Backend: class for quantum computers, and class for specifying backend.

## Documents

- [Tutorial(japanese)](doc/Tutorial.md)

## Requirements

    * Linux(Ubuntu20.04)
    * Python3.8

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
