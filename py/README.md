qlazypy
=======

framework to develope quantum computer application

## Description

'qlazypy' is a quantum computer application framework for python
developers.  The feature is just "simple description and easy to use".

## Usage

import 'QState' module from 'qlazypy' package in your python program.
simple example is following ...

    from qlazypy import QState
    
    # set qubit number
    N = 2
    print("* qubit_num = ", N)

    # initialize quantum state
    qs = QState(N)
	# operate quantum gates
    qs.h(0)
    qs.cx(0,1)
	# complex amplitude of the quantum state
    print("* amplitude = ", qs.amp)

    # measurement (ex: shots=50)
    md = qs.m(shots=50)
	# result frequency of all measurements
    print("* freq = ", md.frq)
	# last result of all measurements
    print("* last = ", md.lst)

    # free object
    del qs
