Quantum state vector (QState class)
===================================

## Operation of quantum state vector

### Initialization

First of all, you need to prepare an initial quantum state before
starting your quantum calculation.  In order to do it, call 'QState'
class constructor to set the qubit number required for the
calculation.  In the case of preparing a 2-qubit initial quantum state
|00>, do as follows.

    >>> qs = QState(qubit_num=2)

Since result of the quantum calculation is probabilistic, it changes
every time.  Qlazy simulates these situation by generating random
number internally.  However, if you want to get a fixed result
regarding to your calculation, you can set a seed number of random
generation using 'seed' option as follows.

    >>> qs = QState(qubit_num=2, seed=123)

About this initialization, there are 2 important points you should
know.

1. The quantum state is always |00..>.  There is no initialization
option to make any qubit to be |1>.  If you want to do that, use Pauli
X gate to reverse qubit after initialization.

2. The maximum number of qubits that can be specified is 30, If you
exceed 30, you will get an error (But before that, your PC memory
will be run out, maybe).

In addtion, you can prepare the initial quantum state by specifing a
ndarray (numpy array) as follows.

    >>> import numpy as np
    >>> vec = np.array([1,0,0,0])
    >>> qs = QState(vector=vec)

Here, the dimention of the vector must be a power of 2 (2, 4, 8, ..).

### Copy

If you want to copy the quantum state vector, use the 'clone' method,

    >>> qs_clone = qs.clone()

### Reset

If you want to initialize and use it again without discarding the
already generated quantum state vector, use the reset method.

    >>> qs.reset()

The quantum state vector becomes |00...0>.  If you give a qubit id
list with arguments, you can forcibly make the qubit corresponding to
the id list |0>.

    >>> qs.reset(qid=[1,5])

When you reset some specific qubits, the qubits are internally measured
and then reset. So if the qubits and the remained qubits are
entangled, the effect of the reset (measureing) extends the remaining
qubits.  In other words, the result is probable.  Please note that the
results may change each time you execute.

### Memory release

If the memory of the quantum state vector instance is no longer used,
it will be released automatically, but if you want to clearly release
it, do as follows.

    >>> del qs

Using the class method 'del_all' allows you to release multiple
quantum state vector instances at once.

    >>> qs_0 = QState(1)
    >>> qs_1 = QState(1)
    >>> qs_2 = QState(1)
    >>> ...
    >>> QState.del_all(qs_0, qs_1, qs_2)

In addition, you can specify quantum state vectors list, tuples or
nest of those as follows.

    >>> qs_A = [qs_1, qs_2]
    >>> QState.del_all(qs_0, qs_A)
	>>> 
    >>> qs_B = [qs_3, [qs_4, qs_5]]
    >>> QState.del_all(qs_B)

### Gate operation

After preparing the initial quantum state vector, you can perform
various kind of gate operations to the state.  The gate operations
that are supported by qlazy are listed bellow.

#### Pauli X,Y,Z gate

    >>> qs.x(q)
    >>> qs.y(q)
    >>> qs.z(q)

The argument 'q' is the qubit id to operate the single-qubit gate,
same applies hereafter.

#### root Pauli X gate

This is the gate that square becomes X gate. 

    >>> qs.xr(q)
    >>> qs.xr_dg(q)  # Hermitian conjugate of 'xr'

#### Hadamard gate

    >>> qs.h(q)

#### Phase shift gate

    >>> qs.s(q)  # PI/2 phase shift
    >>> qs.t(q)  # PI/4 phase shift
    >>> qs.s_dg(q)  # Hermitian conjugate of 's'
    >>> qs.t_dg(q)  # Hermitian conjugate of 't'
	
#### Rotation gate

    >>> qs.rx(q, phase=xxx)  # rotaion around the X-axis
    >>> qs.ry(q, phase=xxx)  # rotaion around the Y-axis
    >>> qs.rz(q, phase=xxx)  # rotaion around the Z-axis
	
If 'phase' is not specified, it means 0 radian rotation (in other
words, do nothing).  The unit of the value specified in 'phase' option
is PI radian. So "phase=0.5" means 0.5*PI radian rotation.

#### Controlled unitary gate

These are controlled unitary gate for Pauli X,Y,Z gate, root Pauli X
gate, Hadamard gate, phase shift gate, and rotation gate.  The
arguments 'q0' and 'q1' are the qubit id to operate the 2-qubit gate;
same applies hereafter.  Here, the 'q0' is the control qubit, the 'q1'
is the target qubit.

    >>> qs.cx(q0,q1)              # controlled X gate (Controlled-NOT,CNOT)
    >>> qs.cy(q0,q1)              # controlled X gate
    >>> qs.cz(q0,q1)              # controlled Z gate
    >>> qs.cxr(q0,q1)             # controlled XR (root Pauli X) gate
    >>> qs.cxr_dg(q0,q1)          # controlled XR+ (rot Pauli X) gate (Hermitian conjugate)
    >>> qs.ch(q0,q1)              # controlled H gate
    >>> qs.cs(q0,q1)              # controlled S gate
    >>> qs.cs_dg(q0,q1)           # controlled S+ gate (Hermitian conjugate)
    >>> qs.ct(q0,q1)              # controlled T gate
    >>> qs.ct_dg(q0,q1)           # controlled T+ gate (Hermitian conjugate)
	>>> qs.cp(q0,q1, phase=xxx)   # controlled phase shift gate
	>>> qs.crx(q0,q1, phase=xxx)  # controlled X-axis rotation gate
	>>> qs.cry(q0,q1, phase=xxx)  # controlled Y-axis rotation gate
	>>> qs.crz(q0,q1, phase=xxx)  # controlled Z-axis rotation gate

### Ising coupling gate

There are 2-qubit gates that are the basics of ion trap quantum
computer.

	>>> qs.rxx(q0,q1, phase=xxx)  # for XX operator
	>>> qs.ryy(q0,q1, phase=xxx)  # for YY operator
	>>> qs.rzz(q0,q1, phase=xxx)  # for ZZ operator

#### Swap gate

    >>> qs.sw(q0,q1)  # swap q0 and q1

#### Toffoli gate

    >>> qs.ccx(q0,q1,q2)  # q0,q1: control qubits, q2: target qubit

#### Controlled swap gate (Fredkin gate)

    >>> qs.csw(q0,q1,q2)  # q0: control qubit, q1,q2: swapped qubits 

#### Multi controlled X gate

This is a controlled X gate with 3 or more control qubits.

    >>> qs.mcx(qid=[q0,q1,..])

The last element of the 'qid' list is interpreted as a target qubit
id, and the other elements are interpreted as the list of control
qubits id.  Please note that the argument is the "list" of the qubit
id.  In qlazy, if it is necessary to specify an indefinite number of
qubit id, give a "list" of the qubit id to the method or function.

#### Quantum Fourier transform

Performing Quantum Fourier transform and its inverse transform are
possible as follows.

    >>> qs.qft(qid=[q0,q1,..])
    >>> qs.iqft(qid=[q0,q1,..])

#### Custom gate

By inheriting the 'QState' class, you can easily create and add your
own quantum gate as follows.

    >>> class MyQState(QState):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> qs = MyQState(qubit_num=2)
	>>> qs.bell(0,1)
    >>> ...

This is a very simple example, so you may not feel much profit, but
there are many situations where you can use it, such as when you want
to create a large quantum circuit.

### Pauli product operation

You can perform to operate a Pauli product (tensor product of pauli
operator X, Y and Z) to the quantum state vector.  In order to handle
pauli product, you must import the 'PauliProduct' class as follows.

    >>> from qlazy import QState, PauliProduct
	
For example, if you want to operate the pauli product "X2 Y0 Z1" for
the 3-qubit quantum state vector 'qs', create the instance of
'PauliProduct' as follows,

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])

then perform 'operate_pp' method with 'pp' option.

    >>> qs.operate_pp(pp=pp)
	
Controlled pauli product can be operated by specifying the control
qubit id in the 'qctrl' option of the 'operate_pp' method as follows.

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
	>>> qs.operate_pp(pp=pp, qctlr=3)


### Quantum circuit operation

You can operate a quantum circuit to the quantum state.
The quantum circuit is prepared using the 'QCirc' class as follows.

    >>> from qlazy import QCirc
    >>> qc = QCirc().h(0).cx(0,1)
	>>> qc.show()
    q[0] -H-*-
    q[1] ---X-

To operate this into the quantum state, use the 'operate_qcirc' method

    >>> qs = QState(qubit_num=2)
	>>> qs.operate_qcirc(qc)

You can also add a control qubit just like 'operate_pp' method.

	>>> qs.operate_qcirc(qc, qctrl=3)

Here, you should note that the quantum circuit that can be operated is limited to unitary.
Those that contain non-unitary gates, such as the measurement gate, cannot be operated.


## Display of quantum state vector

### Display the whole qubits state

You can display the quantum state vector by using 'show' method.

    >>> qs = QState(qubit_num=2).h(0).cx(0,1)
	>>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

### Display the partial qubits state

You can also display the quantum state vector for specific qubits.  In
the case of displaying a quantum state vector for 0th and 2nd qubit,
do as follows.

    >>> qs = QState(qubit_num=3)
	>>> qs.h(0)
	>>> qs.h(2)
	>>> qs.show(qid=[0,2])

The result is this.

    c[00] = +0.5000+0.0000*i : 0.2500 |++++
    c[01] = +0.5000+0.0000*i : 0.2500 |++++
    c[10] = +0.5000+0.0000*i : 0.2500 |++++
    c[11] = +0.5000+0.0000*i : 0.2500 |++++

If you specify the other qubit as follows,

    >>> qs.show(qid=[1])
	
the result is this.

    c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
    c[1] = +0.0000+0.0000*i : 0.0000 |

If the qubits you want to display and the other qubits are entangled,

    >>> qs = MPState(qubit_num=2).h(0).cx(0,1)
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

the result is probable.  For example,

    >>> qs.show(qid=[0])
   
then,

    c[0] = +1.0000+0.0000*i : 1.0000 |+++++++++++
    c[1] = +0.0000+0.0000*i : 0.0000 |

or,

    c[0] = +0.0000+0.0000*i : 0.0000 |
    c[1] = +1.0000+0.0000*i : 1.0000 |+++++++++++

### Display only non-zero components

If you want to display only components with non-zero probability
amplitude, use the 'nonzero' option as follows,

    >>> qs.show(nonzero=True)
	
then,

    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Use it if you want to display the quantum state vector that most of
the components are zero amplitude.

### Notes on normalization

When you display the quantum state vector with the 'show' method,
normalization is performed to be norm is 1.  In addition, a global
phase factor of the state is taken out, so that the coefficient of
C[00..0] becomes positive number.  In the case that C[00..0] of the
original state is 0, the global phase will not be taken out (we can't
do it).  If you want to take out the global phase so that coefficient
of some specific qubit to become positive number, use 'preal' option
as follows.

    >>> qs.show(preal=2)

If you do not want to take out the global phase, specify -1 to the
'preal' option.

    >>> qs.show(preal=-1)

### Probability amplitude

You can get an array (ndarray) of probability amplitudes using
'get_amp' method.  If you set a list of qubit id in 'qid' option, you
will get probability amplitudes corresponding to the list of qubit id.

    >>> vec = qs.get_amp()  # probability amplitudes for the whole qubits
    >>> vec = qs.get_amp(qid=[0,3])  # probability amplitudes for the specified qubits

Please note that if the specified qubits and the rest are entangled,
the results will change each time you execute (like the show method).

Since the 'get_amp' method without the argument is defined as 'amp'
property, the same result as "qs.get_amp()" can be obtained as follows.

    >>> vec = mps.amp

In addition, you can get an absolute value of each probability
amplitude ('probability') using 'get_prob' method.

    >>> prob = qs.get_prob(qid=[0,1])

The return value is a dictionary that the key is qubit id and the value is probability.

    >>> print(prob)
    {'00': 0.5, '11': 0.5}


### Partial system

You can get the quantum state vector of partial system using 'partial' method.
The usage examples are shown below.

    >>> qs_partial = qs.partial(qid=[1,3])

Please note that if the specified qubits and the rest are entangled,
the results will change each time you execute (like the show method).

### Coodinates on Bloch sphere

You can get coordinates on Bloch sphere for a single qubit state using
'bloch' method.  The return values are the angle of Z-axis and the
angle around Z-axis.  The unit of the each value is PI radian, so 0.5
means 0.5*PI radian.

    >>> theta, phi = qs.bloch(q)

However, multiple qubits cannot be specified at the same time.  If the
argument is not specified, 0 is considerd specified.  Please note that
if the specified qubits and the rest are entangled, the results will
change each time you execute (like the show method).


## Measurement of quantum state vector

### Execution of measurement

You can perform Z-axial direction measurement (measurement at the
computational basis) with 'm' method.  Set the following arguments
and execute.

    >>> md = qs.m(qid=[0,3], shots=100, angle=0.5, phase=0.25)

If you do not specify 'qid', 'shots', 'angle' and 'phase', perform a
measurement of Z-axial direction once.  In the 'qid', specify the list
of qubit id you want to measure.  In the 'shots', specify the number
of measurement.  The 'angle' and 'phase' indecate the derection of
measurement.  In the 'angle', specify the angle of the Z-axis in a
unit PI radian.  In the 'phase', specify the angle around the Z-axis
in a unit PI radian.  This measurement method returns a instance of
MData class.

In addition, qlazy has 'mx','my' and 'mz' methods to measure of
X-axis, Y-axis and Z-axis.

    >>> md = qs.mx(qid=[0,2], shots=1000)
    >>> md = qs.my(qid=[0,2], shots=1000)
    >>> md = qs.mz(qid=[0,2], shots=1000)

The 'mz' method is exactly the same as the 'm' method.

Qlazy also has 'mb' method to execute bell-measurement.

    >>> md = qs.mb(qid=[0,2], shots=1000)

Please note that the measurement method returns the MData class
instannce, so it is not possible to connect the gate method after the
measurement method.  For example,

    >>> qs.h(0).cx(0,1).m(qid=[0],shots=10).x(0).m(qid=[1],shots=20)

cannot be executed.  If you want to do this calculation, divide it
into two lines as follows.

    >>> qs.h(0).cx(0,1).m(qid=[0],shosts=10)
    >>> qs.x(1).m(qid=[1], shots=20)

### Display of measurement result

You can display the measurement result using 'show' method.

    >>> md.show()
    direction of measurement: z-axis
    frq[0] = 48
    frq[1] = 52
    last state => 00

This example is the result for Z-axial direction.
The following examples are the measurement results other than the Z-axial direction.
The measurement result in the Z-axial direction is |0>, |1>, 
but the other direction is not |0>, |1>, so qlazy represent that |u>, |d> instead.

X-axial measurement:

    >>> md.show()
    direction of measurement: x-axis
    frq[u] = 49
    frq[d] = 51
    last state => u

Y-axial measurement:

    >>> md.show()
    direction of measurement: y-axis
    frq[u] = 51
    frq[d] = 49
    last state => d

Arbitrary direction measurement (in the case of angle=0.2 and phase=0.3):

    >>> md.show()
    direction of measurement: theta=0.200*PI, phi=0.300*PI
    frq[u] = 90
    frq[d] = 10
    last state => u

Bell measurement:

    bell-measurement
    frq[phi+] = 47
    frq[phi-] = 53
    last state => phi+  # phi+,phi-,psi+,psi-のどれか

### Getting measurement data

You can get the frequency list using 'frq' property and the last
measured value using 'lst' property.

    >>> md.frq
	>>> md.lst
	
The frequency list is a list in which the frequency is stored in the
descending order when the measured value is expressed in decimal
number.  For example, in the case that the frequency |00> is 48 times
while the frequency of |11> is 52 times and others are all 0 times,
'frq' property holds the following values.

    >>> print(md.frq)
    [48,0,0,52]

The 'lst' property holds the measured value converted as a decimal
number.  In the case of measurement other than the Z-axial direction,
it is replaced as u => 0, d => 1.  In the case of Bell measurement, it
is replaces as phi+ => 0, phi- => 3, psi+ => 1, psi- => 2.

However, the output value of the 'frq' and 'lst' properties is
honestly difficult to understand. Recommendations are as follows.

You can get a frequency list in a python standard container data
subclass 'Counter' format using 'frequency' property, and you can get
the last measured value in a binary string using 'last' property.

    >>> print(md.frequency)  # frequency list (dictionary)
	Counter({'00':53,'11':47})
	>>> print(md.last)       # last measurement result
	11

### One-time measurement

If you simply measure it once and get the measured value at the
computational basis, use 'measure' method.

	>>> qs = QState(qubit=2).h(0).cx(0,1)
	>>> mval = qs.measure(qid=[0,1])
	>>> print(mval)
	11

As a result, the quantum state vector becomes the state after
measurement as follows.

    >>> qs.show()
	c[00] = +0.0000+0.0000*i : 0.0000 |
	c[01] = +0.0000+0.0000*i : 0.0000 |
	c[10] = +0.0000+0.0000*i : 0.0000 |
	c[11] = +1.0000+0.0000*i : 1.0000 |+++++++++++


## Calculation regarding quantum state vector

### Inner product of two quantum state vectors

If you want to get an inner product of two quantum state vectors,
use the 'inpro' method.

    >>> qs_0 = QState(2)  # |00>
    >>> qs_1 = QState(2).x(0).x(1)  # |11>
    >>> v = qs_0.inpro(qs_1)

In the above example, <00|11> value is calculated.

### Fidelity of two quantum state vectors

If you want to get a fidelity of two quantum state vectors,
use the 'fidelity' method.

    >>> qs_0 = QState(2)
    >>> qs_1 = QState(2).x(0).x(1)
    >>> v = qs_0.fidelity(qs_1)

In the above example, an absolute value of <00|11>, that is |<00|11>|
is calculated.

### Tensor product of two quantum state vectors

You can get a tensor product of two quantum state vectors using
'tenspro' method.  The usage examples are shown below,

    >>> qs_1 = QState(1).x(0)
    >>> qs_2 = QState(2).h(0).cx(0,1)
    >>> qs_3 = qs_1.tenspro(qs_2)

where tensor product of |1> and (|00>+|11>)/sqrt(2) is stored the variable 'qs_3'

### Composite states

You can use 'composite' method to create a composit state of exactly
same quantum state vectors.  The usage examples are shown below.

    >>> qs_com = qs.composite(4)

### Conversion by matrix

You can get a result of applying a matrix to the quantum state vector
using 'apply' method.

	>>> import numpy as np
    >>> qs = QState(5)	
    >>> M = np.array([[0,1],[1,0]])
	>>> qs.apply(matrix=M, qid=[2])

The above example illustrates that the matrix 'M' is applied to the
2nd qubit of 5-qubit state |00000>.  Here, the size of the matrix must
be smaller than the size of the quantum state vector.  In addition to
that, when the length of the list specified in the 'qid' is n, the
number of rows and columns in the matrix must be 2^n.  Note that the
'apply' method changes the the original instance.

### Schmidt decomposition

You can get the Schmidt coefficients and the bases as a result of the
Schmidt decomposition.  For example, suppose you have a 5-qubit state
'qs', and you want to decompose into [0,1]-system and [2,3,4]-system
in the sense of Schmidt decomposition.  Use 'schmidt_decomp' method as
follows.

    >>> coef,qs_0,qs_1 = qs.schmidt_decomp(qid_0=[0,1], qid_1=[2,3,4])

As a result of this calculation, suppose 'Shmidt rank' was 4.  The
'coef' is a list of four Schmidt coefficient (four real numbers).  The
'qs_0' is a list of four bases (four quantum state vectors) for the
[0,1]-system, and 'qs_1' is a list of four bases (four quantum state
vectors) for the [2,3,4]-system.  If you want to get only the Schmidt
coefficients, use the Schmidt_coef method.

    >>> coef = qs.schmidt_coef(qid_0=[0,1], qid_1=[2,3,4])
	
Since both methods ignore the 0 Schmidt coefficient, 'len(coef)' will
be same as the Schmidt rank.  If the Schmit rank is 1, the [0,1]
system and the [2,3,4] system can be decomposed by tensor, that is,
they are not entangled each other.  So the Schmit decomposition can be
used as an entanglement discriminator.

### Expectation value for observable

You can calculate an expectation value of observable for the quantum
state vector.  In order to do it, first, you should create an instance
of 'Observable' class you are considering.  For example, you can
create the observable expressed by "z0 + 2.0 z1" as follows.

    >>> ob = Observable("z_0 + 2.0 * z_1")

Or,

    >>> ob = Observable()
	>>> ob.add_wpp(weight=1.0, pp=PauliPruduct('Z', [0]))
	>>> ob.add_wpp(weight=2.0, pp=PauliPruduct('Z', [1]))

Or,

    >>> from qlazy.Observable import X, Y, Z
	>>> ob = Z(0) + 2.0 * Z(1)
	
See 'Observable' documentation for more details about how to create.
If the current quantum state vector is given as 'qs', the expectation
value 'exp' can be calculated as follows.

    >>> exp = qs.expect(observable=ob)

### Time development of quantum state

If a Hamiltonian of the system is given, the time development of the
quantum state can be described using a unitary operator that depends
on the Hamiltonian.  This unitary operator is called "time development
operator".  In particular, in the case of a many body system of
two-level quantum particle such as electron with spin freedom, it is
known that the operator can be expressed by a quantum circuits
approximately.  Qlazy implements this calculation.  Use 'evolve'
method as follows.

    >>> qs = QState(2)
    >>> hm = -2.0*Z(0) + Z(0)*Z(1) + X(0) + X(1)
    >>> qs.evolve(observable=hm, time=0.1, iteration=10)
	
In the first line, the 2-qubit state is defined.  The quantum state is
inistialized to |00>.  In the second line, the Hamiltonian described
in the Pauli matrix "-2.0*Z0*Z1+X0+X1" is defined.  In the third line,
the time development prescribed in this Hamiltonian is applied to
quantum state 'qs'.  Here, the 'time' option is time to develop the
quantum state.  The 'iteration' option is a repetition number of times
that is processed internally to improve the approximate accuracy.
Specify a larger value than 'time'.
