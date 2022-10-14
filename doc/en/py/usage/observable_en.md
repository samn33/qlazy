Observable (Obserbable class)
=============================

In the context of quantum mechanics, physical values including
Hamiltonian etc are called 'observable'.  Unlike classical mechanics,
the observalble is expressed by an operator mapping complex vector to
complex vector (or a complex matrix), and an observed physical value
in the actual measuring device is regarded to an eigenvalue of the
operator.  Since this eigenvalue must be a real number (It is strange
that the measured value is complex number, isn't it?), the observable
operator must be a 'Hermitian operator' (see the standard textbook of
quantum mechanics for details).

Observalbles often seen in quantum mechanics and quantum information
theory are expressed in linear sum of products of pauli operators X,
Y and Z.

Qlazy allows you to perform some calculations related to the
observables that are represented by the linear sum of the pauli
operators.  The following calculation can be made for the quantum
state of the 'Qstate' class.

- Expectation value of the observable
- Time development of quantum state of the system with Hamiltonian
  expressed by the observable

In addtion, the following calculations can be made for the quantum
state of the 'MPState' class.

- Expectation value of observable

However, this document does not mention these details.  Please refer
to the 'Qstate' class and the 'MPState' class documentation for it.
This document describes the method of creating an observable and
calculating between the obserbables created like this.


## Create observalble

First, for creating observable, import the 'Observable' class and the
'Observable' related functions X, Y, Z.

    >>> from qlazy import Observable
    >>> from qlazy.Observable import X,Y,Z

There are three ways to create an observable.

- Method by specifying a string
- Method by adding weighted pauli products sequentially
- Method by specifing a linear sum of pauli products

### Method by specifying a string

For example, observable "3.0 Z(0) Z(1) + 4.0 X(2) X(3) 5 Y(4) - 2.0"
can be created as follows.

    >>> ob = Observable("3.0*Z_0*Z_1+4.0*X_2*X_3+5*Y_4-2.0")

It allowed that there is space before and after '+', '-' and '*',
X, Y, Z can be lowercase letters.

    >>> ob = Observable("3.0 * z_0 * z_1 + 4.0 * x_2 * x_3 + 5 * y_4 - 2.0")

You can check the observable using print statements.

    >>> print(ob)
	3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0

Here, there is an important point to describe.  Last term of the above
example '-2.0' means '-2.0 * I' ('I' is an identity operator).  In qlazy, a term
including identity operator is specified without explicitly describing
the identity operator 'I', only specified constant real number.  Of
course, it performs calculations including identity operators.

### Method by adding weighted pauli products sequentially

The same observable as the previous section can be created as follows.
First, create an empty observable instance.

    >>> ob = Observable()

Then, add pauli product and the coefficient (weight) for it by
applying the 'ad_wpp' method (means add weighted pauli product method)
to the created instance.

    >>> ob.add_wpp(weight=3.0, pp=PauliProduct('ZZ', [0,1]))
    >>> ob.add_wpp(weight=4.0, pp=PauliProduct('XX', [2,3]))
    >>> ob.add_wpp(weight=5.0, pp=PauliProduct('Y', [4]))
    >>> ob.add_wpp(weight=-2.0)
    >>> print(ob)
	3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0

### Method by specifing a linear sum of pauli products

When creating in this method, the X, Y and Z function must be imported.

    >>> from qlazy.Qbservable import X, Y, Z

Then, the observable of the previous section can be created as follows.

    >>> ob = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> print(ob)
    3.0 Z(0) Z(1) + 4.0 X(2) X(3) + 5.0 Y(4) - 2.0


## Operation related to observable

You can execute the four arithmetical operation (+, -, *, /) and
comparison operation (=, !=) for observable instances created as
described above.

### Addition

You can execute the addition of two observables using the '+' operator.

    >>> ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    >>> ob_3 = ob_1 + ob_2
    >>> print(ob_3)
    2.0 X(2) X(3) + 5.0 Y(4) + X(1) X(2)

In addition, you can use the '+=' operator to perform incremental additions.

    >>> ob_1 = -2.0 + 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4)
    >>> ob_2 = 2.0 - 3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2)
    >>> ob_1 += ob_2
    >>> print(ob_1)
    2.0 X(2) X(3) + 5.0 Y(4) + X(1) X(2)

### Subtraction

You can use the '-' operator to subtract the two observables.

    >>> ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    >>> ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    >>> ob_3 = ob_1 - ob_2
    >>> print(ob_3)
    6.0 Z(0) Z(1) + 6.0 X(2) X(3) + 5.0 Y(4) - 4.0 - X(1) X(2)

In addition, you can use the '-=' operator to perform incremental subtractions.

    ob_1 = 3.0 * Z(0) * Z(1) + 4.0 * X(2) * X(3) + 5.0 * Y(4) - 2.0
    ob_2 = -3.0 * Z(0) * Z(1) - 2.0 * X(2) * X(3) + X(1) * X(2) + 2.0
    ob_1 -= ob_2
    print(ob_1)
    6.0 Z(0) Z(1) + 6.0 X(2) X(3) + 5.0 Y(4) - 4.0 - X(1) X(2)

### Multiplication

You can use the '*' operator to multiply an observable by a real number. 

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 * 3.0
    >>> print(ob_2)
    3.0 Z(0) + 6.0 Z(1)

You can also multiply the two observables.

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 3.0 * Z(0) + 4.0 * Z(1)
    >>> ob_3 = ob_1 * ob_2
    >>> print(ob_3)
    11.0 + 10.0 Z(0) Z(1)

In addtion, you can use '*=' operators to perform incremental multiplication.

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_1 *= 3.0
    >>> print(ob_1)
    3.0 Z(0) + 6.0 Z(1)

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 3.0 * Z(0) + 4.0 * Z(1)
    >>> ob_1 *= ob_2
    >>> print(ob_1)
    11.0 + 10.0 Z(0) Z(1)

### Division

You can use the '/' operator to divide an observable with a real number. 

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 / 2.0
    >>> print(ob_2)
    0.5 Z(0) + Z(1)

In addition, you can use the '/=' operator to perform incremental division.

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_1 /= 2.0
    >>> print(ob_1)
    0.5 Z(0) + Z(1)

The division of the observable with an observable is not supported.

### Exponentiation

You can use the '**' operator to perform the observable to the power of interger.

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = ob_1 ** 2
    >>> print(ob_2)
    5.0 + 4.0 Z(0) Z(1)
    >>> ob_3 = ob_1 ** 3
    >>> print(ob_3)
    13.0 Z(0) + 14.0 Z(1)

### Comparison

You can check whether the two observables are equal by '==', '!=' operator.

    >>> ob_1 = Z(0) + 2.0 * Z(1)
    >>> ob_2 = 2.0 * Z(1) + Z(0)
    >>> print(ob_1 == ob_2)
	True
    >>> print(ob_1 != ob_2)
	False

### Note: non-Hermitian observables

As a result of executing the calculation shown above, a non-Hermitian
observable may be created.  For example,

    >>> ob_1 = Z(0) * X(0)

Since ZX = iY, ob_1 is no longer Hermitian. Any meaningful observalbes
corenpond to real pysical quantity must be Hermitian, but this is
allowed in qlazy specifications.  However, if this observable is
displayed by print statement or calculating expectation value in some
quantum state, an error occurs that means "not Hermitian".

    >>> print(ob_1)  # --> error
	>>> expect_value = qs.expect(observable=ob_1)  # --> error

This is not allowed, but you can do some calculation to the above ob_1.
For example,

    >>> ob_2 = ob_1 * X(0)

This operation can be executed without any problems.
As a result, you can get an Hermitian observable because it is ZXX = Z.
So this can be displayed without any problems in print statement.

    >>> print(ob_2)
	Z(0)

In addition, expectation value can be calculated without any problems.

    >>> qs.expect(observable=ob_2)
	
Whether the observable is Hermitian or not can be obtained by the
'is_hermitian' method.

    >>> ob_1 = Z(0) X(0)
	>>> print(ob_1.is_hermitian())
	False
    >>> ob_2 = ob_1 * X(0)
	>>> print(ob_2.is_hermitian())
	True
