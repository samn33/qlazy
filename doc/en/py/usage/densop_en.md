Density Operator (DensOp class)
===============================

## Operation of density operator

The quantum state can be classified into pure state and mixed state.
The mixed state is defined as an ensemble {p(i), |phi(i)>} (i = 0,1,2,
...).  Here, p(i) is the probability that |phi(i)> will appear.  A
"density operator" has been introduced as a convenient notation that
uniformly describes the quantum state, including such a mixed state.
The definition of the density operator 'rho' is expressed by "rho =
sum_{i} p(i) |phi(i)><phi(i)|".  Qlazy has the function of creating
density operators from a set of pure states and executing various
calculations regarding to the density operator.

### Initialization

You can create the density operator as an instance of the 'DensOp' as
follows.

    >>> from qlazy import QState,DensOp
	>>> 
    >>> qs1 = QState(2).h(0).cx(0,1)
    >>> qs2 = QState(2).x(0).z(1)
	>>> 
    >>> de = DensOp(qstate=[qs1,qs2], prob=[0.3,0.7])

When two quantum state vector 'qs1' and 'qs2' are present, giving
lists of quantum states and probability values as arguments of
'Densop', you obtain the instance of the density operator.  You can
specify many quantum states as long as the memory allows.
However, all specified qubits number must be equal.  If you omit a
'prob' option, the density operator is created such that all quantum
states have same probability.  In addition, you can create the
instance by specifing the numpy matrix (two-dimensional array) as
follows.

    >>> import numpy as np
	>>> mat = np.array([[1,0],[0,0]])
    >>> de = DensOp(matrix=mat)
	
Here, note that the dimension of the matrix must be integer power of 2
(2, 4, 8, 16, ...).

### Gate operation

You can perform a gate operation to the density operator.  If the gate
is 'U' and the density operator is 'rho', the gate operation is
expressed by 'U * rho * U^' (U^ means Hermitian conjugate of U).
Qlazy's specification for the gate operation is exactly the same as in
the 'Qstate' class as follows.

    >>> de.h(0).cx(0,1)
	>>> de.crx(0,1, phase=0.1)
    >>> ...

#### Custom gate

By inheriting the 'DensOp' class, you can easily create and add your
own quantum gate as follows.

    >>> class MyDensOp(DensOp):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> de = MyDensOp(qubit_num=2)
	>>> de.bell(0,1)
    >>> ...

This is a very simple example, so you may not feel much profit, but
there are many situations where you can use it, such as when you want
to create a large quantum circuit.

### Pauli product operation

You can perform to operate a Pauli product (tensor product of pauli
operator X, Y and Z) to the density operator.  In order to handle
pauli product, you must import the 'PauliProduct' class as follows.

    >>> from qlazy import DensOp, PauliProduct
	
For example, if you want to operate the pauli product "X2 Y0 Z1" for
the 3-qubit density operator 'de', create the instance of
'PauliProduct' as follows,

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])

then perform 'operate' method with 'pp' option.

	>>> de.operate(pp=pp)
	
Controlled pauli product can be operated by specifying the control
qubit id in the 'qctrl' option of the 'operate' method as follows.

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	>>> de.operate(pp=pp, qctlr=3)

### Quantum channel

You can apply some typical quantum channels to the density operator.

    >>> de.bit_flip(q, prob=xxx)
    >>> de.phase_flip(q, prob=xxx)
    >>> de.bit_phase_flip(q, prob=xxx)
    >>> de.depolarize(q, prob=xxx)
    >>> de.amp_dump(q, prob=xxx)
    >>> de.phase_dump(q, prob=xxx)

In order from the top, they represents methods executing "bit flip",
"phase flip", "bit and phase flip", "polarization", "amplitude
dumping", and "phase dumping".  The argument 'q' is the qubit id you
want to apply.  The 'prob' option is a parameter that indicates the
probability of applying noise ('xxx' is some real number).  For what
each quantum channel means, see Nielsen Chang's ["Quantum Computation
and Quantum Information"](https://en.wikipedia.org/wiki/Quantum_Computation_and_Quantum_Information).

### Memory release

If the memory of the density operator instance is no longer used, it will be
released automatically, but if you want to clearly release it, do as follows.

    >>> del de

Using the class method 'del_all' allows you to release multiple
density operator instances at once.

	>>> mat = np.array([[0.3, 0.1], [0.1, 0.7]])
    >>> de_0 = DensOp(matrix=mat)
    >>> de_1 = DensOp(matrix=mat).x(0)
    >>> de_2 = DensOp(matrix=mat).h(0)
    >>> ...
    >>> DensOp.del_all(de_0, de_1, de_2)

In addition, you can specify density operators list, tuples or nest of
those as follows.

    >>> de_A = [de_1, de_2]
    >>> DensOp.del_all(de_0, de_A)
	>>> 
    >>> de_B = [de_3, [de_4, de_5]]
    >>> DensOp.del_all(de_B)

### Copy

If you want to copy the density operator, use the clone method.

    >>> de_clone = de.clone()

### Reset

If you want to initialize and use it again without discarding the
already generated density operator, use the reset method.

    >>> de.reset()

The 'de' becomes |00...0><00...0|.  If you give a qubit id list as
arguments, you can forcibly make the qubit corresponding to the id
list |0> as follows.

    >>> de.reset(qid=[1,5])


## Display of density operator

### Elements of density operator (matrix expression in computational basis)

You can display the elements of density operator using 'show' method.
The usage examples are shown below.

    >>> de.show()
    elm[0][0] = +0.0000+0.0000*i : 0.0000 |
    elm[0][1] = +0.0000+0.0000*i : 0.0000 |
    elm[1][0] = +0.0000+0.0000*i : 0.0000 |
    elm[1][1] = +1.0000+0.0000*i : 1.0000 |+++++++++++
	
In addition, you can display the elements of density operator of
partial system.

    >>> de.show(qid=[q0,q1,...])

For example,

    >>> de.show(qid=[0,3])

then displays the density operator for the 0th and 3rd qubit.
Internally, partial traces are performed for qubits other than the 0th
and 3rd qubits.

### Display only non-zero components

If you want to display only non-zero components, use 'nonzero'
option as follows,

    >>> de.show(nonzero=True)

then,

    elm[1][1] = +1.0000+0.0000*i : 1.0000 |+++++++++++

This option is useful if you want to display the density matrix that
most of the components are zero.

### Getting elements

You can get the elements as a two-dimensional numpy array by using the
'get_elm' method:

    >>> elm = de.get_elm()
    >>> elm = de.get_elm(id=[1,2])


## Calculation regarding density operators

### Tace

You can get a trace of density operator using 'trace' method.
The usage examples are shown below.

    >>> tr = de.trace()

Trace of density operator is theoretically "always one", so in most
cases this method does not make much sense.  But if you apply some
matrix conversion to the density operator, the trace may not be one in
general.  In that case, calculating the trace will make sense
(described later).

### Square trace

You can get a square trace of density operator using 'sqtrace' method.
The usage examples are shown below.

    >>> sqtr = de.sqtrace()

In the case of a pure state density operator, this value is 1, and in
the case of a mixed state, it is theoretically known that it is 1 or
less.  One of the typical situations that you uses this method is when
you want to determine whether some quantum state is pure or mixed.

### Partial trace

You can get a partial trace of the density operator using 'patrace'
method.  The usage examples are shown below.

    >>> de_reduced = de.patrace(qid=[q0,q1,...])

Specify the qubit id list that you want to trace out in the 'qid' option.

### Partial system

You can get the density operator of partial system using 'partial' method.
The usage examples are shown below.

    >>> de_partial = de.partial(qid=[q0,q1,...])

Specify the qubit id list that you want to get in the 'qid' option.
	
In the 'patrace' method, specify the qubit id "I want to throw away",
while the 'partial' method specifies the qubit id "I want to leave".
Except for the interpretation of arguments, the internal processing is
exactly the same.

### Tensor product

You can get a tensor product of two density operators using
'tenspro' method.  The usage examples are shown below.

    de_product = de_A.tenspro(de_B)

The tensor product of de_a and de_b is calculated and store to
de_product.

### Composite states

You can use 'composite' method to create a composit state of exactly
same density operators.  The usage examples are shown below.

    >>> de_com = de.composite(4)

### Conversion by matrix

You can get a result of applying a conversion matrix to the density
operator using 'apply' method.  The usage examples are shown below.

    >>> import numpy as np
    >>> M = np.array([[0.0,1.0],[1.0,0.0]])
    >>> de.apply(matrix=M, qid=[2])  # X-gate operation in the 2nd qubit

Applying a conversoin matrix 'M' to the density operator 'rho' means
calculating "M * rho * M^" ('M^' is Hermitian conjugate of 'M').  This
matrix must be prepared as a two-dimensional array of numpy and the
size must be smaller than the size of the density operator.  In
addition, when the length of the list specified in the qid is
n, the number of rows and columns in the matrix must be 2^n.
Note that the 'apply' method changes the the original instance.

### Addition and Multiplication

You can perform addition between two density operators using 'add'
method, and multiplication with scalar value.  The usage examples are
shown below.

    >>> de.add(de_0)
    >>> de.mul(0.3)

Note that the 'add' and 'mul' method changes the the original instance.

### Mixing density operators

You can get a result of mixing many density operators (linear sum of
the density operators).  The usage examples are shown below.

    >>> de = DensOp.mix(densop=[de1,de2], prob=[0.2,0.8])

### Probability

You can get a probability list related to POVM (Positive Operator
Valued Measure) or Kraus operators using 'probability' method (For
what POVM or Kraus operator means, see Nielsen Chang's ["QuantumComputation and Quantum Information"](https://en.wikipedia.org/wiki/Quantum_Computation_and_Quantum_Information). The usage examples are shown below,

    >>> prob = de.probability(povm=[E0,E1], qid=[0,1])
    >>> prob = de.probability(kraus=[M0,M1], qid=[0,1])

where the 'E0' and 'E1' represent POVM operators (numpy matrix) and
the 'M0', 'M1' represent Kraus operators (numpy matrix).  the list
specified as 'qid' represent qubit id to be measured.  If the length
of qubit id is n, the size of 'E0', 'E1', 'M0' and 'M1' must be all 2^n.
Note that this method does not change the original density operator.

### Probability（CP-instrument）

You can get a density operator after executing the measurement
related to Kraus operators using 'instrument' method.  The 'kraus' and
'qid' option means same as 'probability' method.  The usage examples
are shown below.

    >>> de.instrument(kraus=[M0,M1], qid=[0,1])

This is an example of 'non-selective measurement'.  The 'non-selective
measurement' is the situation where the measurement is performed but
forget the result.

    >>> de.instrument(kraus=[M0,M1], qid=[0,1], measured_value=1)

This is an example of 'selective measurement' in the case that
measured value is '1'.  The 'selective measurement' is the situation
where the measurement is performed and remember the result.  Note that
this method does change the original density operator.  In addition,
this method does not perform normalization, in other words, trace of
'de' is not 1.  So if you want to obtain a normalized density
operator, do as follows.

    >>> prob = de.trace()
    >>> de.mul(factor=1.0/prob)

### Fidelity

You can get a fidelity between two density operators using 'fidelity'
method.  The usage examples are shown below.

	>>> fid = de1.fidelity(de2)

### Trace distance

You can get a trace disance between two density operators using
'distance' method.  The usage examples are shown below.

	>>> dis = de1.distance(de2)

### Spectral decomposition

You can get a spectral decomposition of the density operator using
'spectrum' method.  The usage examples are shown below.

	>>> qstate, prob = de.spectrum()

This method returrns a list of quantum states (list of QState
instances) and a list of propbabilities.  As a side note,

	>>> de1 = DensOp(qstate=qstate, prob=prob)

means inverse operation of spectral decomposition, so 'de1' is same as
original density operator 'de'.

### Entropy (von Neumann Entropy)

You can get a von Neumann entropy of the density operator using
'entropy' method.  The usage examples are shown below.

	>>> ent = de.entropy()

### Entanglment entropy

In addition, you can get an entropy for partial system (called
'entanglment entropy') using 'entropy' method by specifing 'qid'
option.

	>>> ent_A = de.entropy(qid=[0,1])    # for system A

This is an example of calculating the entanglment entropy for a
sub-system represented by 0th and 1st qubits.

	>>> ent_B = de.entropy(qid=[2,3,4])  # for system B

This is an example of calculating the entanglment entropy for a
sub-system represented by 2nd, 3rd and 4th qubits.

### Conditional entropy

You can get a conditional entropy of the density operator using
'cond_entropy' method.

	>>> ent_cond = de.cond_entropy([0,1],[2,3,4])

This is an example of calculating the conditional entropy of partial
system A (represented by 0th and 1st qubits) under the condition that
partial system B (represented by 2nd, 3rd and 4th qubits) is
determined.  Unlike conditional entropy in classical information
theory, it can be negative.  As a side note, the conditional entropy
S(A|B) is calculated by S(A|B) = S(A,B) - S(A) (S(A,B): entropy of
whole system, S(A): partial entropy for system A).

### Mutual information

You can get a mutual information of the density operator using
'mut_info' method.

	>>> mut_info = de.mutual_info([0,1],[2,3,4])

This is an example of calculating the mutual information between
partial system A (represented by 0th and 1st qubits) and partial
system B (represented by 2nd, 3rd and 4th qubits).  Even if A and B
are replaced, the value will be the same.  As a side note, the mutual
information I(A:B) is calculated by I(A:B) = S(A) + S(B) - S(A,B)
(S(A,B): entropy of whole system, S(A), S(B): partial entropy for
system A, B).

### Relative entropy

You can get a relative entropy of the two density operators using
'relative_entropy' method.  The usage examples are shown below.

    >>> rel_ent = de1.relative_entropy(de2)
