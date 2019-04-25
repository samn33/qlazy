qlazy
=====

Quantum Computer Simulator

## Install

### command and library - qlazy,libQlazy.so

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ mkdir build; cd build; cmake ..; make
    $ mv libQlazy.so ~/lib; mv qlazy ~/bin

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

print help
	
    $ qlazy -h

### qlazy (interactive-mode)

    $ qlazy
	
	>> init 2
	>> h 0
	>> cx 0 1
	>> show   # show the current quantum state
	>> m
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
    
    del qs

execute the program

    $ python foo.py

## Requirements

    * Linux(Ubuntu16.04)
    * Python3.5

## Licence

Apache License 2.0

## Author

[Sam.N](http://github.com/samn33)
