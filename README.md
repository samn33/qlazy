qlazy
=====

Quantum Computer Simulator

## Install

### command and library - qlazy,libQlazy.so

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ mkdir build; cd build; cmake ..; make
    $ mv libQlazy.so ~/lib; mv qlazy ~/bin
	
add followings to your ~/.bashrc

    export PATH=$PATH:~/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/lib

You may also need to install 'readline-dev' ($ sudo apt install readline-dev).

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
    
    md = qs.m()
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

## Requirements

    * Linux(Ubuntu16.04)
    * Python3.5

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
