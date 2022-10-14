Simple usage examples
=====================

We will get started to show a simple example.

    >>> from qlazy import QState
    >>> 
	>>> # Initialize 2 qubits to |0>
    >>> qs = QState(2)
	>>> 
	>>> # Operation of quantum gates
    >>> qs.h(0)
    >>> qs.cx(0,1)
    >>> qs.show()    # show the current quantum state
	>>> 
    >>> # Measurement
    >>> md = qs.m(shots=100)
	>>> md.show()            # show the measurement result
    >>> print(md.frequency)  # list of frequency (Counter format of python's collection package)
	>>> print(md.last)       # last measurement resutl (string consisting of '0','1')

First, you should initialize a quantum state with 'QState' constructor
with an argument.  The arugment value '2' of the above example means
that you prepared 2-qubit state |00>.  The 'QState' constructor returns
an instance of 'QState' class ('qs' in the above).  Second, after
initializing, you should perform some quantum gates you want to
calculate one after another.  In the above example, Hadamard gate (by
'h' method) for 0th qubit and cx gate (by 'cx' method) for 0th and 1st
qubit are performed.  Finally, some (or all) of qubits are measured
(by 'm' method).  The 'm' method have 'shots' option means measurement
counts and returns an instance of 'MData' class as a measurering result.

You can see some 'show' methods.  The 'show' method for 'QState'
instance ('qs') perform to show the current quantum state.  In the above
example, the following information is displayed on your screen.

    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Since the quantum state is superposition of eigenstates |00>, |01>, |10>, |11>
in 2-qubit system, the state can be expressed in four complex numbers
(called complex amplitudes or probability amplitudes) correspond to each eigenstate.
The "c[00] = +0.7071+0.0000*i : ..." shows the complex amplitude correspond to 
the eigenstate |00> etc.
Here, note that qubit order in qlazy is from left to right,
so |01> means |0> at the 0th qubit and |1> at the 1st qubit.
Real number on the right of complex amplitude (0.5000 or 0.0000) is
absolute value of each complex, that is probability of the eigenstate.
The "++++++" displayed on the right is a stick graph to make
visually easy to understand each probability value.

The 'show' method for MData instance ('md') perform to show the
measurement result.  In the above example, the following information is
displayed on your screen.

    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00

In the above measurement result, the first line of "direction of
Measurement: z-axis" means that the Z-axial direction is measured.
The default measurement direction is the Z-axial direction. Unlike
most other simulators, qlazy can perform a measurement in an arbitrary
direction.  This first line is to clearly show the direction.  The
"frq[xx] = xx" in the second and subsequent line indicates the number of times that
measured state was |xx>.  The default measuring trials are 100
times. The above example indicates that the |00> was 49 times, and the |11>
was 51 times (sum of these is 100).  Qlazy simulates probable measurement,
so this result changes in each execution. The "last state" in the last line
shows what the result of the last measurement was.
In the above example, it was |00>.

If you want to get the measurement frequencies as python standard
Counter class, you can use 'frequency' property.  If you want to get
the last measured value as string type, you can use 'last' property.

    >>> print(md.frequency)  # measurement frequencis (Counter)
	Counter({'00':53,'11':47})
	>>> print(md.last)       # last measured value (str)
	00

In the above example, the last measurement value was |00>. 
In qlazy, the quantum state changing after measurement is simulated.

    >>> qs.show()

then you can see how the wave function is shrinking as shown bellow.

    c[00] = +1.0000+0.0000*i : 1.0000 |+++++++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.0000+0.0000*i : 0.0000 |
