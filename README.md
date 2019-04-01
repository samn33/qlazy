qlazy
=====

Quantum Computer Simulator

## Description

    * command and library (qlazy,libqlazy.so)
    * python package (qlazypy)

## Install

### readline (for interactive mode)

    $ sudo apt install readline-dev

### command and library (qlazy,libqlazy.so)

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy/c
    $ make
    $ mkdir ~/bin ~/lib ~/include
    $ make install

### python package (qlazypy)

    $ cd ../../py
    $ pip install -e .

## Usage

### qlazy (read file)

    $ cat foo.qc
	init 2
    h 0
    cx 0 1
    m
    $ qlazy -qc foo.qc
	
    $ qlazy -h (print help)

### qlazy (interactive mode)

    $ qlazy
	>> init 2
	>> show
	>> h 0
	>> cx 0 1
	>> show
	>> m
	>> quit

	>> help (print help)

### qlazypy

    $ cat foo.py
    from qlazypy.basic import QState
    
    qs = QState(2)
    qs.h(0)
    qs.cx(0,1)
    qs.show()
    
    md = qs.m(shots=50)
    md.show()
    
    md.free()
    qs.free()
	$ python foo.py

## Licence

Apache License 2.0

## Author

[samn33](http://github.com/samn33)
