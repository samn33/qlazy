Stabilizer (Stabilizer class)
=============================

## Operation of stabilizer state

When a quantum state is unchanged even if operated by any element of a
partial pauli group "S=<g1,g2,..,gn>", 'S' is called 'stabilizer
group' (each element of the group is called 'stabilizer' or
'stabilizer operator'), and the invariable quantum state is called a
'stabilizer state'.  Normally, quantum state is expressed as a vector
in Hilbert space, but it can also be expressed by a group of
stabilizers that make the quantum state invariant.  Under this
expression, the state change in the quantum system is represented by
unitary transformation 'U' to stabilizer 'gi', namely "gi -> U gi U+
(i=1,..,n)".  This way of expressing the change of quantum state is
called 'stabilizer formalism'.  According to 'Gottesmann-Knill
theorem', if 'U' is limited to 'Clifford operators'
('X','Y','Z','H','S','S+','CX','CY','CZ'), the change in quantum state
is simulated efficiently with a classical computer by the stabilizer
formalism.  In qlazy, you can simulate this operation by creating the
stabilizer state followed by applying the Clifford operators and
measuring operators.

### Initialization

First, you should initialize the stabilizer state using the Stabilizer
class.  The usage examples is shown bellow.

    >>> from qlazy import Stabilizer
    >>> sb = Stabilizer(qubit_num=3)

This generates three stabilizer operators to identify the 3-qubit
state internaly.  You can check the three stabilizer operators using
'show' method.

    >>> sb.show()
    g[0]:  III
    g[1]:  III
    g[3]:  III

At first, everything is set to identity operator. This doesn't make
sense because 3-qubit state is not determined uniquely.  In order to
determine the 3-qubit state uniquely, three stabilizer operators g[0],
g[1], g[2] are needed to be independent each other.  In general, in
order to determine the N-qubit state uniquely, the N stabilizers are
needed to be independent each other.  Here, 'independent each other'
means that any stabilizer in the group cannot be expressed with
product of other stabilizers.  The group of independent stabilizers is
called 'generators'.

Perhaps you are interested in initializing the quantum state to |00..0>.
In stabilizre formalism, 3-qubit |000> state is expressed as follows.

    g[0]:  ZII
    g[1]:  IZI
    g[2]:  IIZ

You can obtain this state by using the 'set_all' method.

    >>> sb.set_all('Z')
	>>> sb.show()
    g[0]:  ZII
    g[1]:  IZI
    g[2]:  IIZ

The argument 'Z' means that every i-th qubit of i-th generator is set
to pauli Z operator.

In addtion, you can initialize all qubits |+> (|+++> in 3-qubit
system) as follows.

    >>> sb.set_all('X')
	>>> sb.show()
    g[0]:  XII
    g[1]:  IXI
    g[2]:  IIX

You can also set the initial stabilizer operators arbitrarily by using
the 'set_pauli_op' method.  The usage examples are shown below.

    >>> sb.set_pauli_op(0, 0, 'X')
    >>> sb.set_pauli_op(0, 1, 'X')
    >>> sb.set_pauli_op(1, 1, 'Z')
    >>> sb.set_pauli_op(1, 2, 'Z')
    >>> sb.set_pauli_op(2, 0, 'X')
	>>> sb.show()
    g[0]:  XXI
    g[1]:  IZZ
    g[2]:  XII

The first argument of 'set_pauli_op' represents the generators id, the
second argument represents the qubit id, and the third argument
specifies the pauli operator ('X', 'Y', 'Z' or 'I').

You can also add four signs (+1, -1, +i, -i) to each generator by
using 'set_pauli_fac' method.  The usage examples are shown below.

    >>> sb.set_pauli_fac(1, '-i')
	>>> sb.show()
    g[0]:  XXI
    g[1]:-iIZZ
    g[2]:  XII

The first argument of 'set_pauli_fac' is the generator id, and the
second argument specifies the sign (+1, -1, +i, -i) in the character
string.

You can also generate a stabilizer instance by giving a list of pauli
product to the argument of Stabilizer.

    >>> str_list = ["IIIXXXX", "IXXIIXX", "XIXIXIX", "IIIZZZZ", "IZZIIZZ", "ZIZIZIZ"]
    >>> pp_list = [PauliProduct(pauli_str=pp_str) for pp_str in str_list]
    >>> sb = Stabilizer(pp_list=pp_list)
	>>> sb.show()
    g[0]:  IIIXXXX
    g[1]:  IXXIIXX
    g[2]:  XIXIXIX
    g[3]:  IIIZZZZ
    g[4]:  IZZIIZZ
    g[5]:  ZIZIZIZ

### Gate operation

You can execute the gate operation for the stabilizer instance.
However, it is limited to Clifford operators ('X', 'Y', 'Z', 'H', 'H',
'S+', 'CX', 'CY', 'CY', 'CZ').  T-gates and rotating gates cannot be
executed.  The format is the same as in the 'Qstate' class as follows.

    >>> sb.h(0).cx(0,1)
    >>> ...
	
#### Restrictions on qubits

There is no limitation. You can set the number of qubit as long as the
memory allows.

#### Number of qubits and generators

You can initialize a stabilizer state with 'qubit_num' option and
'gene_num' option of 'Stabilizer'.  The 'gene_num' means number of
generators.  If this option does not be specified, the value will be
the same as 'qubit_num'.  You can also set the 'gene_num' to a
different value from the 'qubit_num'.  In qlazy, you can execute the
gate operations for such stabilizer state (to be exact, stabilizer
group) as follows.  However, cannot execute measurement operation
(return some error).

    >>> sb = Stabilizer(gene_num=4, qubit_num=3)
    >>> sb.set_all('Z')
    >>> sb.h(0).cx(0,1).cx(0,2)
    >>> ...

#### Custom gate

By inheriting the 'Stabilizer' class, you can easily create and add your
own quantum gate as follows.

    >>> class MyStabilizer(Stabilizer):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> sb = MyStabilizer(qubit_num=2).set_all('Z')
	>>> sb.bell(0,1)
    >>> ...

This is a very simple example, so you may not feel much profit, but
there are many situations where you can use it, such as when you want
to create a large quantum circuit.

### Pauli product operation

You can perform to operate a Pauli product (tensor product of pauli
operator X, Y and Z) to the stabilizer state.  In order to handle
pauli product, you must import the 'PauliProduct' class as follows.

    >>> from qlazy import Stabilizer, PauliProduct

For example, if you want to operate the pauli product "X2 Y0 Z1" for
the 3-qubit stabilizer state 'sb', create the instance of
'PauliProduct' as follows,

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])

then perform 'operate' method with 'pp' option.

	>>> sb.operate(pp=pp)

Controlled pauli product can be operated by specifying the control
qubit id in the 'qctrl' option of the 'operate' method as follows.

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])
	>>> sb.operate(pp=pp, qctlr=3)

### Measurement

As in the 'Qstate' class, you can get a measurement data (as an
instance of 'MdataStabilizer' class) by using 'm 'method.  The
measurement data contains frequencis and last measured value.  Each
can be extracted with 'frequency' property and 'last' property as
follows.

    >>> md = sb.m(qid=[0,1,2], shots=100)
    >>> print(md.frequency)
    Counter({'000':58,'111':42})
    >>> print(md.last)
    111

### One-time measurement

If you simply measure it once and get the measured value at the
computational basis, you can use 'measure' method.
The return value of this method is a string that represents the measured value.
In qlazy, the stabilizer state changing after measurement is simulated as follows.

	>>> sb = Stabilizer(qubit=2).set_all('Z').h(0).cx(0,1)
	>>> mval = sb.measure(qid=[0,1])
	>>> print(mval)
	11
	>>> sb.show()
	g[0]: -ZI
	g[1]:  ZZ

### Memory release

If the memory of the 'Stabilizer' instance is no longer used, it will be
released automatically, but if you want to clearly release it, you can
release it at any time as follows.

    >>> del sb
	
Using the class method 'del_all' allows you to release multiple
stabilizer instances at once.

    >>> Stabilizer.del_all(sb_0, sb_1, sb_2)

In addition, you can specify stabilizer list, tuples or nest of
those as follows.

    >>> sb_A = [sb_1, sb_2]
    >>> Stabilizer.del_all(sb_0, sb_A)
	>>> 
    >>> sb_B = [sb_3, [sb_4, sb_5]]
    >>> Stabilizer.del_all(sb_B)

### Copy

If you want to copy the stabilizer, use the clone method,

    >>> sb_clone = sb.clone()

### Reset

If you want to initialize and use it again without discarding the
already generated stabilizer, use the reset method.

    >>> sb.reset()

All operators can be reset to the identity operator I.

### Display

You can display the generators of stabilizer using 'show' method as follows.

    >>> sb.show()
    g[0]:  XXI
    g[1]:-iIZZ
    g[2]:  XII

### Elements of stabilizer

You can obtain a pauli operator corresponding to j-th qubit of i-th
generator of the stabilizer as a string 'X', 'Y', 'Z' or 'I' by using
'get_pauli_op' method.  In addition, you can obtain a factor of i-th
generator as a complex number by using 'get_pauli_fac' method.  The
usage examples are shown below.

    >>> sb.show()
    g[0]:  XXI
    g[1]:-iIZZ
    g[2]:  XII

    >>> print(sb.get_pauli_op(1,2)) # pauli oprator of 2nd qubit of 1st generator
	Z
    >>> print(sb.get_pauli_fac(1)) # factor of 1st generator
	(0-1j)
