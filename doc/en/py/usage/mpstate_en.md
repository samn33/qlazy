Matrix product state (MPState class)
====================================

## Operation of matrix product state

The quantum computing simulation can mainly be performed using the
quantum state vector, but as the number of qubits N increases, a
memory of O(2^N) will be required.  So too large size quantum
computation cannot be performed.  The limit is about 25 to 30 qubits
in generally popular PC.  However, considering the realistic quantum
state, it is not always necessary to use the freedom of O(2^n) fully.
As a method of compressing the quantum state according to the degree
of freedom, it is known that the method utilizing the matrix product
state using a tensor network.  Qlazy allows you to simulate the matrix
product state using the 'MPState' class.  It uses Google's
[tensornetwork](https://github.com/google/TensorNetwork) internally.

### Simple example

We will get started to show a simple example.

    >>> from qlazy import MPState
    >>> 
    >>> mps = MPState(qubit_num=100)
    >>> mps.h(0)
    >>> [mps.cx(i,i+1) for i in range(99)]
    >>> md = mps.m(shots=100)
    >>> print(md.frequency)
    Counter({'0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000': 55, '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111': 45})

You can apply quantum gates one after another and finally get the
measurement value by the 'm' method like 'QState' class.  The major
difference from 'QState' is that it can be calculated even in quantum
state exceeding 30 quantum bits (but it is difficult to calculate a
large amount of entangles ...).

We will explain how to use the 'MPstate' class in detail below.

### Initialization

You can create the matrix product state as an instance of the
'MPState' as follows.

    >>> from qlazy import MPState
	>>> mps = MPState(qubit_num=100)

### Gate operation

You can perform a gate operation to the matrix product state.
The format is the same as in the 'Qstate' class as follows.

    >>> mps.h(0).cx(0,1)
	>>> ...

#### Custom gate

By inheriting the 'MPState' class, you can easily create and add your
own quantum gate as follows.

    >>> class MyMPState(MPState):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> mps = MyMPState(qubit_num=2)
	>>> mps.bell(0,1)
    >>> ...

This is a very simple example, so you may not feel much profit, but
there are many situations where you can use it, such as when you want
to create a large quantum circuit.

### Pauli product operation

You can perform to operate a Pauli product (tensor product of pauli
operator X, Y and Z) to the matrix product state.  In order to handle
pauli product, you must import the 'PauliProduct' class as follows.

    >>> from qlazy import MPState, PauliProduct
	
For example, if you want to operate the pauli product "X2 Y0 Z1" for
the 3-qubit matrix product state 'mps', create the instance of
'PauliProduct' as follows,

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])

then perform 'operate' method with 'pp' option.

    >>> mps.operate(pp=pp)

Controlled pauli product can be operated by specifying the control
qubit id in the 'qctrl' option of the 'operate' method as follows.

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	>>> mps.operate(pp=pp, qctrl=3)

### Memory release

If the memory of the 'MPState' instance is no longer used, it will be
released automatically, but if you want to clearly release it, you can
release it at any time as follows.

    >>> del mps

Using the class method 'del_all' allows you to release multiple
stabilizer instances at once.

    >>> mps_0 = MPState(qubit_num=2)
    >>> mps_1 = MPState(qubit_num=3)
    >>> mps_2 = MPState(qubit_num=4)
	>>> ...
    >>> MPState.del_all(mps_0, mps_1, mps_2)

In addition, you can specify matrix product states list, tuples or
nest of those as follows.

    >>> mps_A = [mps_1, mps_2]
    >>> MPState.del_all(mps_0, mps_A)
	>>> 
    >>> mps_B = [mps_3, [mps_4, mps_5]]
    >>> MPState.del_all(de_B)

### Copy

If you want to copy the matrix product state, use the 'clone' method,

    >>> mps_clone = mps.clone()

### Reset

If you want to initialize and use it again without discarding the
already generated matrix product state, use the reset method.

    >>> mps.reset()

The matrix product state becomes |00...0>.  If you give a qubit id
list with arguments, you can forcibly make the qubit corresponding to
the id list |0>.

    >>> mps.reset(qid=[1,5])

When you reset some specific qubits, the qubits are internally measured
and then reset. So if the qubits and the remained qubits are
entangled, the effect of the reset (measureing) extends the remaining
qubits.  In other words, the result is probable.  Please note that the
results may change each time you execute.


## Display of matrix product state

### Display the whole qubits state

You can display the matrix product state by using 'show' method.

    >>> mps = MPState(qubit_num=2).h(0).cx(0,1)
	>>> mps.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Please note that if you try to display a matrix product state for the
large number of qubits, you may run out of memory, because qlazy
internally converts it to a quantum state vector.

### Display the partial qubits state

You can also display the matrix product state for specific qubits.  In
the case of displaying a matrix product state for 0th and 2nd qubit,
do as follows.

    >>> mps = MPState(qubit_num=3)
	>>> mps.h(0)
	>>> mps.h(2)
    >>> mps.show(qid=[0,2])

The result is this.

    c[00] = +0.5000+0.0000*i : 0.2500 |++++
    c[01] = +0.5000+0.0000*i : 0.2500 |++++
    c[10] = +0.5000+0.0000*i : 0.2500 |++++
    c[11] = +0.5000+0.0000*i : 0.2500 |++++

If you specify the other qubit as follows,

    >>> mps.show(qid=[1])
	
the result is this.

    c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
    c[1] = +0.0000+0.0000*i : 0.0000 |

If the qubits you want to display and the other qubits are entangled,

    >>> mps = MPState(qubit_num=2).h(0).cx(0,1)
    >>> mps.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

the result is probable.  For example,

    >>> mps.show(qid=[0])
   
then,

    c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
    c[1] = +0.0000+0.0000*i : 0.0000 |

or,

    c[0] = +0.0000+0.0000*i : 0.0000 |
    c[1] = +1.0000+0.0000*i : 1.0000 |+++++++++++

### Display only non-zero components

If you want to display only components with non-zero probability
amplitude, use the 'nonzero' option as follows,

    >>> mps.show(nonzero=True)
	
then,

    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Use it if you want to display the matrix product state that most of
the components are zero amplitude.

### Notes on normalization

When you display the matrix product state with the 'show' method,
normalization is performed to be norm is 1.  In addition, a global
phase factor of the state is taken out, so that the coefficient of
C[00..0] becomes positive number.  In the case that C[00..0] of the
original state is 0, the global phase will not be taken out (we can't
do it).  If you want to take out the global phase so that coefficient
of some specific qubit to become positive number, use 'preal' option
as follows.

    >>> mps.show(preal=2)

If you do not want to take out the global phase, specify -1 to the
'preal' option.

    >>> mps.show(preal=-1)

### Probability amplitude

You can get an array (ndarray) of probability amplitudes using
'get_amp' method.  If you set a list of qubit id in 'qid' option, you
will get probability amplitudes corresponding to the list of qubit id.

    >>> vec = mps.get_amp()  # probability amplitudes for the whole qubits
    >>> vec = mps.get_amp(qid=[0,3])  # probability amplitudes for the specified qubits

Please note that if the specified qubits and the rest are entangled,
the results will change each time you execute (like the show method).
Since the 'get_amp' method without the argument is defined as 'amp'
property, the same result as "qs.get_amp()" can be obtained as follows.

    >>> vec = mps.amp


## Measurement of matrix product state

### Execution of measurement

You can perform Z-axial direction measurement (measurement at the
computational basis) with 'm' method.  Set the following arguments
and execute.

    >>> md = qs.m(qid=[0,3], shots=100)

The 'qid' means the list of specified qubit id, the 'shots' means
number of measurement trials.  If the 'qid' is not specified, all
qubits measurements is performed.  If the 'shots' is not specified,
one time measurement is performed.  The 'm' method returns an instance
of the 'MDataMPState' class.

    >>> mps = MPState(qubit_num=2)
	>>> mps.h(0).cx(0,1)
	>>> md = mps.m(qid=[0,1], shots=100)

If you want to get the frequencies of the measured value, use
'frequency' property.  You will get it as python standard 'Counter'
data format.  If you want to get the last measured value, use 'last'
property.

    >>> print(md.frequency)
	Counter({'00':53,'11':47})
	>>> print(md.last)
	11
	
The quantum state after measurement changes according to the last
measurement result as follows.

    >>> mps.show()
    c[00] = +0.0000+0.0000*i : 0.0000 |
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +1.0000+0.0000*i : 1.0000 |+++++++++++


#### Notes

Even if the quantum circuit of several tens to hundreds of quantum
bits is not so deep and not so much entanglements, the calculation of
the quantum circuit can be executed without difficulty.  However, if
it has measurements for many qubits in a large number of shots, it may
take a tremendous time to get the measurement result.  The main
purpose of using the matrix product state simulation is considered to
be a simulation for quantum machine learning, quantum chemical
calculations, and optimization issues on NISC devices, so we recommend
that you try it with the expectation value calculation (described
later) instead of obtaining the measurement values in large number of
shots.

### One-time measurement

If you simply measure it once and get the measured value at the
computational basis, use 'measure' method.

	>>> mps = MPState(qubit=2).h(0).cx(0,1)
	>>> mval = mps.measure(qid=[0,1])
	>>> print(mval)
	11

As a result, the matrix product state becomes the state after
measurement as follows.

	>>> mps.show()
	c[00] = +0.0000+0.0000*i : 0.0000 |
	c[01] = +0.0000+0.0000*i : 0.0000 |
	c[10] = +0.0000+0.0000*i : 0.0000 |
	c[11] = +1.0000+0.0000*i : 1.0000 |+++++++++++


## Calculation regarding matrix product states

### Inner product of two matrix product states

If you want to get an inner product of two matrix product states, use
the 'inpro' method.

    >>> mps_0 = MPState(qubit_num=2)  # |00>
    >>> mps_1 = MPState(qubit_num=2).x(0).x(1)  # |11>
    >>> v = mps_0.inpro(mps_1)
	0j

In the above example, <00|11> value is calculated.

### Fidelity of two matrix product states

If you want to get a fidelity of two matrix product states, use the
'fidelity' method.

    >>> mps_0 = MPState(qubit_num=2)
    >>> mps_1 = MPState(qubit_num=2).x(0).x(1)
    >>> v = qs_0.fidelity(qs_1)
	0.0

In the above example, an absolute value of <00|11>, that is |<00|11>|
is calculated.

### Expectation value for observable

You can calculate an expectation value of observable for the matrix
product state.  In order to do it, first, you should create an
instance of 'Observable' class you are considering.  For example, you
can create the observable expressed by "z0 + 2.0 z1" as follows.

    >>> ob = Observable("z_0 + 2.0 * z_1")

Or,

    >>> ob = Observable()
	>>> ob.add_wpp(weight=1.0, pp=PauliPruduct('Z', [0]))
	>>> ob.add_wpp(weight=2.0, pp=PauliPruduct('Z', [1]))

Or,

    >>> from qlazy.Observable import X, Y, Z
	>>> ob = Z(0) + 2.0 * Z(1)
	
See 'Observable' documentation for more details about how to create.
If the current matrix product state is given as 'mps', the expectation
value 'exp' can be calculated as follows.

    >>> exp = mps.expect(observable=ob)
