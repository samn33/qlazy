qlazy
=====

Quantum Computing Simulator

## Install

### command and library - qlazy,libqlz.so

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ mkdir build; cd build; cmake ..; make
    $ mv libqlz.so ~/lib; mv qlazy ~/bin
	
add followings to your ~/.bashrc

    export PATH=$PATH:~/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/lib

You may also need to install 'libreadline-dev'

    $ sudo apt install libreadline-dev

### python package - qlazypy

    $ cd ../../py
    $ pip install -e .

## Usage

### qlazy (read-file)

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

### qlazy (interactive-mode)

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

### qlazypy

foo.py
	
    from qlazypy import QState
    
    qs = QState(2)
    qs.h(0)
    qs.cx(0,1)
    qs.show()
    md = qs.m(shots=100)
    md.show()
    
    qs.free()

execute the program

    $ python foo.py
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
    direction of measurement: z-axis
    frq[00] = 46
    frq[11] = 54
    last state => 11

another style to print measured result.

    ...
    qs.m(shots=100)
	print(qs.m_freq())
    >> Counter({'00': 46, '11': 54})

## Requirements

    * Linux(Ubuntu18.04)
    * Python3.6.9

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
