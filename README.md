qlazy
=====

Quantum Computer Simulator

## Install

### command and library (qlazy,libqlazy.so)

    $ sudo apt install readline-dev
    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ mkdir build; cd build; cmake ..
    $ mv libQlazy.so ~/lib; mv qlazy ~/bin

### python package (qlazypy)

    $ cd ../../py
    $ pip install -e .

## Usage

### qlazy (read file)

circuit file: foo.qc

    init 2
    h 0
    cx 0 1
    m

run circuit

    $ qlazy -qc foo.qc

print help
	
    $ qlazy -h

### qlazy (interactive mode)

    $ qlazy
	
	>> init 2
	>> h 0
	>> cx 0 1
	>> show   # show the current quantume state
	>> m
	>> quit

print help

	>> help
	>> help <item>

### qlazypy

foo.py
	
    from qlazypy.basic import QState
    
    qs = QState(2)
    qs.h(0)
    qs.cx(0,1)
    qs.show()
    
    md = qs.m(shots=50)
    md.show()
    
    md.free()
    qs.free()

execute 

    $ python foo.py

## ChangeLog

### v0.0.1 (2019.4.1)

initial version

### v0.0.2 (2019.4.3)

make -> cmake

## Licence

Apache License 2.0

## Author

[samn33](http://github.com/samn33)
