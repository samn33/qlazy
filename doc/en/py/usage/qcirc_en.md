Quantum circuit execution (Backend, QCirc class)
=================================================================

## Basics of quantum circuit execution

Performing quantum calculation on a quantum computer means that you
put a quantum circuit into a quantum computer and obtain a measurement
result.  In qlazy, prepare a quantum computer (or simulator) as a
'Backend' class instance and a quantum circuit as a 'QCirc' class
instance, obtain a measurement result by performing the quantum
circuit on the quantum computer.

### Prepare quantum computer

You can set a quantum computer (or simulator) by specifying 'product'
option and 'device' option in the 'Backend' class constructor.  For
example, if you want to calculate with 'qstate_simulator' device of
'qstate' product, set as follows.

    >>> from qlazy import Backend
	>>> bk = Backend(product='qlazy', device='qstate_simulator')

In the case of 'stabilizer_simulator' of 'qlazy' product:

	>>> bk = Backend(product='qlazy', device='stabilizer_simulator')

'mps_simulator' of 'qlazy' product:

	>>> bk = Backend(product='qlazy', device='mps_simulator')

Nothing to specified as follows, set 'qstate_simulator' device of 'qlazy' product.

	>>> bk = Backend()

In addition, the supported backend in the current version of qlazy are 
[qulacs](https://github.com/qulacs/qulacs), [IBM Quantum(IBMQ)](https://quantum-computing.ibm.com/),
and [Amazon Braket(LocalSimulator,AWS,IonQ,Rigetti,OQC)](https://aws.amazon.com/braket/?nc1=h_ls).

You can get the supporting products list as follows.

    >>> print(Backend.products())
    ['qlazy', 'qulacs', 'ibmq', 'braket_local', 'braket_aws', 'braket_ionq', 'braket_rigetti', 'braket_oqc']

You can get the devices list that can be used in each product as follows.

	>>> print(Backend.devices('ibmq'))
    ['aer_simulator', 'least_busy', 'ibmq_armonk', 'ibmq_bogota', 'ibmq_lima', 'ibmq_belem', 'ibmq_quito', 'ibmq_manila']

### Creating quantum circuit

#### Unitary gate

Once you have a quantum computer, then create a quantum circuit.  In
order to do it, add the gate to the 'QCirc' class instance in the same
notation as the 'Qstate' class.  For example, if you want to create a
circuit to create a Bell state,

    >>> from qlazy import QCirc
    >>> qc = QCirc()
    >>> qc.h(0)
    >>> qc.cx(0,1)

where 'h' represent Hadamard gate and 'cx' represent CNOT gate.
The following description is also allowed.

    >>> qc = QCirc().h(0).cx(0,1)

This circuit can be expressed as follows visually,

    q[0] --H--*---
              |
    q[1] -----X---
    
where q[0], q[1] represent the qubit id (quantum register number).

### Pauli product gate

You can add a Pauli product (tensor product of pauli operator X, Y and
Z) to the quantum circuit.  In order to handle pauli product, you must
import the 'PauliProduct' class as follows.

    >>> from qlazy import QCirc, PauliProduct

For example, if you want to add the pauli product "X2 Y0 Z1" to the
quantum circuit 'qc', create the instance of 'PauliProduct' as
follows,

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[2,0,1])

then perform 'operate_pp' method with 'pp' option.

	>>> qc.operate_pp(pp=pp)

Controlled pauli product can be added by specifying the control
qubit id in the 'qctrl' option of the 'operate_pp' method as follows.

	>>> pp = PauliProduct(pauli_str="XYZ", qid=[0,1,2])
	>>> qc.operate_pp(pp=pp, qctlr=3)

#### Measuring gate

If you want to measure, specify the list of the qubit id in 'qid'
option and the list of the classical bit id (classical memory number
or classical register number) in 'cid' optoin.

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])

The above circuit can be expressed visually as follows,

    q[0] --H--*---M
              |   |
    q[1] -----X---|--M
                  |  |
    c[0] ---------*--|--
                     |
    c[1] ------------*--

where c[0] and c[1] represent the classical bit id.

If you want to turn the gate operation 'on' or 'off' according to the
measurement results stored the classical bit, use 'ctrl' option of
each unitary gate method.  Such an example is shown below,

    >>> qc = QCirc()
    >>> qc.h(0).cx(0,1).measure(qid=[0],cid=[0])
    >>> qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])

where, by adding "h(0).cx(0,1)" and "measure(qid=[0],cid=[0])", the
measured value of the 0th qubit are stored in the 0th classic
register.  Next gate is "x(0, ctrl=0)".  The 'x' represents Pauli X
gate, and the 1st argument is the qubit id to apply the gate.  In the
'QCirc' class, you can also specify the argument called 'ctrl' in each
unitary gate method.  This is to indicate whether or not this gate is
applied according to the measured value stored in the classic bit id
specified in the 'ctrl' option.  In the current example, the 'measure'
in the previous stage stored the measured value of 0th qubit in the
0th classic register, so the Pauli X gate would be executed depending
on whether the value stored classical register was 0 or 1.  If it is
1, the Pauli X gate will be executed.  The following "x(1, ctrl=0)" is
a Pauli X gate where execution is controlled with the same manner.
Finally, it is 'measure' again.  Measured value of the 0th and the 1st
qubit are stored in the 0th and 1st classical registers.  The above
circuit can be expressed as follows visually.

    q[0] --H--*---M---------X-------M
              |   |         |       |
    q[1] -----X---|--M------|---X---|--M
                  |  |      |   |   |  |
    c[0] ---------*--|------*---*---*--|--
                     |                 |
    c[1] ------------*-----------------*--


#### Reset gate

You can force a specific qubit to be |0> using 'reset' method as
follows.

    >>> qc = QCirc().h(0).cx(0,1).reset(qid=[0])

Specify the qubit id you want to be |0> in the 'qid' option.

### Execution of quantum calculation

To execute quantum calculation, use 'run' method of the 'Backend'
class.

	>>> bk = Backend()  # qlazy's quantum state vector simulator (defalut)
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcirc=qc, shots=100)

As described above, specify the quantum circuit in 'qcirc' option and
number of measurements in 'shots' option.  The 'run' method returns an
instance of 'Result' class.  The 'cid' property of the 'Result' class
store the list of the classical register, and the 'frequency' property
of the 'Result' class store the frequencies of measurement as follows.

    >>> print(result.cid)
	[0,1]
	>>> print(result.frequency)
	Counter({'00': 52, '11': 48})
	
You can also specify the list of classical register id you want to
get.  For example, 

	>>> result = bk.run(qcirc=qc, shots=100, cid=[0])

then you can get the only frequencies regarding to the 0th classical
register as follows.

    >>> print(result.cid)
	[0]
    >>> print(result.frequency)
    Counter({'0': 52, '1': 48})

In other words, you can get a marginalized frequencies list.  If 'cid'
is omitted, the frequencies list is calculated over the all classical
regsters.  In addition, backend information, qubit number, classical
bit number, measured number of times, calculation start time,
calculation end time, and calculation time can be obtained as follows.

    >>> print(result.backend)
    {'product': 'qlazy', 'device': 'qstate_simulator'}
    >>> print(result.qubit_num)
    2
    >>> print(result.cmem_num)
    2
    >>> print(result.shots)
    100
    >>> print(result.start_time)
    2022-03-05 13:32:33.837965
    >>> print(result.end_time)
    2022-03-05 13:32:33.842534
    >>> print(result.elapsed_time)
    0.004569

If you want to see only the list of frequencies visually, use 'show'
method as follows.

    >>> result.show()
    freq[00] = 54 (0.5400) |+++++++++++++++++
    freq[11] = 46 (0.4600) |++++++++++++++

If you want to see all at once, set the 'verbose' option to be True as
follows.

    >>> result.show(verbose=True)
    [backend]
    - product      = qlazy
    - device       = qstate_simulator
    [qubit & cmem]
    - qubit_num    = 2
    - cmem_num     = 2
    [measurement]
    - cid          = [0, 1]
    - shots        = 100
    [time]
    - start_time   = 2022-03-15 23:05:41.249034
    - end_time     = 2022-03-15 23:05:41.254211
    - elassed time = 0.005177 [sec]
    [histogram]
    - freq[00] = 54 (0.5400) |+++++++++++++++++
    - freq[11] = 46 (0.4600) |++++++++++++++

You can save this execution result as a file or read the saved ones.

Save file:

    >>> result.save("hoge.res")

Load file:

    >>> from qlazy import Result
    >>> result_load = Result.load("hoge.res")
	
You can also see the result data as follows in the Python one-liner.

    $ python -c "from qlazy import Result; Result.load('hoge.res').show(verbose=True)"

#### Notes: measurement in the matrix status simulator

Even if the quantum circuit of several tens to hundreds of quantum
bits is not so deep and not so much entanglements, the calculation of
the quantum circuit can be executed without difficulty.  However, if
it has measurements for many qubits in a large number of shots, it may
take a tremendous time to get the measurement result.  The main
purpose of using the matrix product state simulation is considered to
be a simulation for quantum machine learning, quantum chemical
calculations, and optimization issues on NISC devices, so we recommend
that you try it with the expectation value calculation instead of
obtaining the measurement values in large number of shots.

#### Getting quantum state (only qlazy backend and qulacs backend)

When you execute the 'run' method using qlazy's 'qstate_simulator',
'stabilizer_simulator', or 'mps_simulator', by specifing 'out_state'
option to be 'True', quantum state after executing the quantum circuit
is set to property of 'qstate', 'stabilizer', or 'mpstate'.

    >>> qc = QCirc().h(0).cx(0,1)
    >>> qs_sim = Backend(product='qlazy', device='qstate_simulator')
    >>> result = qs_sim.run(qcirc=qc, out_state=True)
    >>> qs = result.qstate
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

    >>> qc = QCirc().h(0).cx(0,1)
    >>> sb_sim = Backend(product='qlazy', device='stabilizer_simulator')
    >>> result = sb_sim.run(qcirc=qc, out_state=True)
    >>> sb = result.stabilizer
    >>> sb.show()
    g[0]:  XX
    g[1]:  ZZ

    >>> qc = QCirc().h(0).cx(0,1)
    >>> mps_sim = Backend(product='qlazy', device='mps_simulator')
    >>> result = mps_sim.run(qcirc=qc, out_state=True)
    >>> mps = result.mpstate
    >>> mps.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Based on the quantum state obtained in this way, various calculation
defined in 'QState', 'Stabilizer', and 'MPState' can be executed (for
example, expectation value calculation for observaable, etc).  See the
documentation for each class for details.

You can also get a qlazy's quantum state vector from 'cpu_simulator'
or 'gpu_simulator' of 'qulacs' as follows.

    >>> qc = QCirc().h(0).cx(0,1)
    >>> qs_sim = Backend(product='qulacs', device='cpu_simulator')
    >>> result = qs_sim.run(qcirc=qc, out_state=True)
    >>> qs = result.qstate
    >>> qs.show()
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

#### Expectation value of observable

When you want to calculate an expectation value of an observable after
executing a quantum circuit, you can use 'expect' method of
'Backend' class.  For example, after executing the following quantum
circuit,

    >>> qc = QCirc().h(0).h(1).h(2).h(3)

expectation value of the following observable,

    >>> ob = Z(0)*Z(1) + 0.5*Z(1)*Z(2)

is obtained as follows,

    >>> bk = Backend(product='qlazy', device='qstate_simulator')
    >>> qc = QCirc().h(0).h(1).h(2).h(3)
    >>> ob = Z(0)*Z(1) + 0.5*Z(1)*Z(2)
    >>> exp = bk.expect(qcirc=qc, observable=ob, shots=10000)

If you set the quantum circuit to the 'qcirc' option, set the
observable to 'observable' option and set the number of trials to
'shots' option, then qlazy executes the quantum circuit and measures
the observable for the number of times specified in 'shots', outputs
the average value of the measured values as the expectation value.  If
a simulator is specified as a backend, it generates a random number
internally and simulates the measurement.  If the actual machine is
specified, obtain the actual measurement values and calculate the
expected value.  Therefore, the obtained expectation value isn't equal
to the theoretical value.  The expectation value in the above example
should be theoretically zero, but in fact, it shifts a little as
follows.

    >>> print("exp = {:.6f}".format(exp))
    exp = -0.001200+0.000000j

If you want to get the theoretical expectation value, set the
'precise' option to True instead of the 'shots' option as follows.

    >>> exp = bk.expect(qcirc=qc, observable=ob, precise=True)

This executes the theoretical calculation internally to output
accurate expectation value.

    >>> print("exp = {:.6f}".format(exp))
    -0.000000+0.000000j	
	
However, this can be executed when a simulator is specified in the
backend, specifically, when only qlazy's 'qstate_simulator',
'qstate_gpu_simulator', 'mps_simulator', and qulacs' 'cpu_simulator'
and 'gpu_simulator' are specified.

#### Setting of initial quantum state (only qlazy backend)

If you execute a quantum circuit with the 'run' method or find the
expectation value of the observable after the quantum circuit
execution in the 'expect' method, the initial quantum state is set to |00...0>.
However, you may want to execute 'run' or 'expect' withsome special
quantum state in the initial state.  In such a case, you can use the
'init' option.

For example, suppose an initial quantum state as follows,

    >>> qs = QState(qubit_num=2).h(0).x(1)

execute the following quantum circuit,

    >>> qc = QCirc().cx(0,1).measure(qid=[0,1], cid=[0,1])

do as follows,

    >>> bk = Backend()
	>>> result = bk.run(init=qs, qcirc=qc, shots=100)

The 'expect' method can also set the initial state in the same way as follows.

    >>> ob = Z(0)*Z(1)
	>>> exp_meas = bk.expect(init=qs, qcirc=qc, observable=ob, shots=1000)
	>>> exp_prec = bk.expect(init=qs, qcirc=qc, observable=ob, presice=True)

The initial quantum state can be set in the 'run' method only for
qlazy backends (qstate_simulator, qstate_gpu_simulator,
stabilzer_Simulator, and mps_simulator).  The initial quantum state
can be set in the 'expect' method only for qlazy backends
(qstate_simulator, qstate_gpu_simulator, and mps_simulator).


### Supported quantum gate

The available quantum gates are shown below.  The arguments that can
be specified are the same as those of the 'Qstate' class, etc, and
'ctrl' option described above can also be specified in all unitary gates
(However, it cannot be specified in non-unitary gates like measurement
gate).

#### Single-qubit gate (unitary gate)

- x,y,z: Pauli X/Y/Z gate
- h: Hadamard gate
- xr,xr_dg: root X and root X dagger gate
- s,s_dg: S and S dagger gate
- t,t_dg: T and T dagger gate
- p: phase shift gate
- rx,ry,rz: RX/RY/RZ (rotation around X/Y/Z-axis) gate

#### 2-qubit gate (unitary gate)

- cx,cy,cz: controlled X/Y/Z gate
- cxr,cxr_dg: controlled XR and XR dagger gate
- ch: controlled Hadamard gate
- cs,cs_dg: controlled S and S dagger gate
- ct,ct_dg: controlled T and T dagger gate
- sw: swap gate
- cp: controlled P gate
- crx,cry,crz: controlled RX/RY/RZ gate
- rxx,ryy,rzz: Ising coupling gate

#### 3-qubit gate (unitary gate)

- ccx: toffoli gate (or CCX gate, controlled controlled X gate)
- csw: fredkin gate (or controlled swap gate)

#### Measurement gate (non-unitary gate)

- measure: measurement gate (computational basis)

#### Reset gate (non-unitary gate)

- reset: reset gate (computational basis)

#### Note: in the case of stabilizer simulator

In the case of sutabilizer simullator, only Clifford gates
('x','y','z','h','s','s_dg','cx','cy','cz') can be supported.


## Operation of quantum circuit

### Display of quantum circuit

You can display your quantum circuit using 'print' function as
follows.

    >>> qc = QCirc()
    >>> qc.h(0).cx(0,1).measure(qid=[0],cid=[0])
    >>> qc.x(0, ctrl=0).x(1, ctrl=0).measure(qid=[0,1], cid=[0,1])
	>>> print(qc)
    h 0
    cx 0 1
    measure 0 -> 0
    x 0 , ctrl = 0
    x 1 , ctrl = 0
    measure 0 -> 0
    measure 1 -> 1

You can also display it more visually using 'show' method.

    >>> qc.show()
    q[0] -H-*-M-X---M---
    q[1] ---X-|-|-X-|-M-
    c  =/=====v=^=^=v=v=
        2     0 0 0 0 1

If you want to display a long (deep) quantum circuit that does not fit
into the screen width, you can specify the width of line breaks in
'width' option as follows.

    >>>> qc.show(width=60)
    q[0] -Z---------X-Z-H-X-X-------*-T-S-X-X-------X-X-X-----S-
    q[1] ---------S-|---T---|-H-H-X-|-T-----|-*-------X-|---*-H-
    q[2] -H-X-X-T-H-|-------*-------|-S-S---|-|---------|-S-|-Z-
    q[3] -----------|---T-----------|-H-----*-|-X-*-X-S-*---|-S-
    q[4] -H-------X-*---------------X---X-----X---X---T---Z-X---
    c  =/=======================================================
        5
    
    ----*-X-------X-Z-------------------T-Z-T-X-X-H-X-X-H-Z---X-
    *---|-|-H-X-X---X-X-*-X-Z---H-H-T---------|-|-H---|-------|-
    |-Z-X-*-----*-------|-H---*-X-S-----T-T---|-|-S---*-X-S-X-|-
    |---------S-------H-X-Z-S-X-T-X---*-X---Z-*-*-X-T-------*-*-
    X-----------------T---------H---S-X-----T-----------X-T-----
    ============================================================
    
    Z-S---S-----X-----------M---------
    ------------|-----*---S-|-M-------
    H-----T-----|---S-|-S-S-|-|-M-----
    H-S-*---*---*-X---|---S-|-|-|-M---
    ----X---X-H---*---X-----|-|-|-|-M-
    ========================v=v=v=v=v=
                            0 1 2 3 4
						

#### Identicality of quantum circuits

Whether the two quantum circuits are exactly the same can be
determined by the logical operator '=='.

    >>> qc_A = QCirc().h(0).cx(0,1)
	>>> qc_B = QCirc().h(0).cx(0,1)
	>>> qc_C = QCirc().h(0).cx(1,0)
	>>> print(qc_A == qc_B)
	True
	>>> print(qc_A == qc_C)
	False

Equivalence of the quantum circuits will be described later.

#### Concatenate of quantum circuits

You can concatenate two quantum circuits by '+' operator.

For 3 quantum circuits,

    >>> qc_A = QCirc().h(0)
	>>> qc_B = QCirc().cx(0,1)
	>>> qc_C = QCirc().measure(qid=[0], cid=[0])

you can concatenate those as follows,

    >>> qc = qc_A + qc_B + qc_C

then you will get a following circuit.

    q[0] -H-*-M-
    q[1] ---X-|-
    c  =/=====v=
        1     0

In addition, it is also possible to concatenate using an increment
operator.

    >>> qc = qc_A
    >>> qc += qc_B
    >>> qc += qc_C

Moreover, if you want to concatenate the same quantum circuits
repeatedly, you can use '*' operator as follows,

    >>> qc_A = QCirc().h(0).cx(0,1)
	>>> qc = qc_A * 3
	>>> qc.show()
    q[0] -H-*-H-*-H-*-
    q[1] ---X---X---X-


### Statistical information of quantum circuit

As you may have noticed in the explanation so far, it is not necessary
to explicitly specify the qubit number and classical bits number at
the first quantum circuit generation as follows.

    >>> qc = QCirc()

You don't need to specily nothing.  It is automatically renewed and
retained from the added quantum gate information each time.

    >>> qubit_num = qc.qubit_num
    >>> cmem_num = qc.cmem_num

You can get number of qubits and number of classical bits by the
'qubit_num' property and 'cmem_num' property.  In addition, you can
get the number of quantum gates contained in your circuit by the
'gate_num' property.

    >>> gate_num = qc.gate_num

For example,

    >>> qc = QCirc().h(0).cx(1,0)
    >>> print(qc.qubit_num)
    2
    >>> print(qc.cmem_num)
	0
    >>> print(qc.gate_num)
    2

Here, it is important to know that the quantum gate that is internally
handled is limited to 15 types of gates --
'x','z','h','s','s_dg','t','t_dg','rx','rz','cx','cz','ch','crz','measure',
and 'reset', although the quantum gates available in 'QCirc' are more
than 15 types as described above.  Quantum gates other than 15 types
are expressed in those combinations internally.

For example, the 'sw' (swap) gate is expressed in the form of three
gate operations as follows.

    >>> qc.cx(0,1).cx(1,0).cx(0,1)
	
The 'crx' (controlled rotation-X) gate is expressed as follows.

    >>> qc.h(1).crz(0,1).h(1)

In addition, the 'measure' and the 'reset' are expressed in the
operation of each qubit.  That is,

    >>> qc.measure(qid=[0,1], cid=[0,1])
    >>> qc.reset(qid=[0,1])

is expressed internaly as follows.

    >>> qc.measure(qid=[0], cid=[0]).measure(qid=[1], cid=[1])
    >>> qc.reset(qid=[0]).reset(qid=[1])

So, the value of "qc.gate_num" is larger than you intended value, and
you may say "a little strange?". It is because of the such reason.
You can check how it was expressed internally by 'print' function.

If you want to know the number of qubits, classical bits, quantum
gates, and the frequency of quantum gates, you can get it as a
dictionary data by using the 'get_stats' method as follows.

    >>> qc = QCirc().h(0).cx(1,0).t(1).measure(qid=[0,1], cid=[0,1])
	>>> print(qc.get_stats())
    {'qubit_num': 2, 'cmem_num': 2, 'gate_num': 5, 'gate_freq': Counter({'measure': 2, 'h': 1, 'cx': 1, 't': 1}), 'gatetype_freq': Counter({'unitary': 3, 'clifford': 2, 'non-unitary': 2, 'non-clifford': 1})}

### Generation of quantum circuits

You may want to make a random quantum circuit for the purpose of
quantum calculation performance evaluation or quantum circuit
optimization, etc.  In such case, you can use 'get_random_gate' method
(class method).

For example, as follows,

    >>> qc = QCirc.generate_random_gates(qubit_num=5, gate_num=100, phase=(0.0, 0.25, 0.5), prob={'h':7, 'cx':5, 'rx':3, 'crz':3})

where the 'qubit_num' option and the 'gate_num' option are the number
of quantum bits and quantum gates of quantum circuits you want to
generate.  The 'prob' option is the probabilities of the quantum gates
in a dictionary data.  In the above example, 'h', 'cx', 'rx' and 'crx'
appear in 7: 5: 3: 3.

    prob={'h':0.7, 'cx':0.5, 'rx':0.3, 'crz':0.3}

It may be specified by a decimal in this way (it will process it
internally even if you don't make those sum to be 1.0).  Supported
gates are only unitary gates --
'x','z','h','s','s_dg','t','t_dg','rx','rz','cx','cz','ch','crz'.
Non-unitary gates cannot be specified.  The 'phase' option is valid
when there is a rotating gate (if there is no rotation system, the
specification is ignored).  By the 'phase' option, specify how you
want to set phases such as 'rx' or 'crz', etc.

    phase=(0.0, 0.25, 0.5)

In this case, if a rotating gate appears, 0.0*PI, 0.25*PI or 0.5*PI
phase will be set with equal probability.

By "print(qc)", you can see that the following circuit is generated.

    >>> print(qc)
    h 3
    h 4
    rx(0.25) 3
    h 2
    cx 2 4
    h 2
    h 2
    crz(0.0) 0 1
    cx 3 4
    h 4
    ...

### Save and load quantum circuit

You can save the created quantum circuit to the file or load the
saved file.  To save, use 'save' method as follows.

    >>> qc_A = QCirc().h(0).cx(1,0).measure(qid=[0,1], cid=[0,1])
	>>> qc_A.save("hoge.qc")
	
This describes the contents of 'qc' is saved to the file
'hoge.qc' (using "pickle" internally).  To load, use the 'load' method
(class method) as follows.

    >>> qc_B = QCirc.load("hoge.qc")

### OpenQASM export and import

You can export quantum circuits created in qlazy to OpenQASM 2.0
format strings and file, or import them.  Use 'to_qasm' method to
output a QpenQASM format strings as follows.

    >>> qc = QCirc().h(0).cx(0,1)
	>>> qasm = qc.to_qasm()
	>>> print(qasm)
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    h q[0];
    cx q[0],q[1];

You can use 'to_qasm_file' method to output a file in OpenQASM format
as follows.

	>>> qc.to_qasm_file("foo.qasm")

You can also create a quantum circuit of qlazy from OpenQASM string
and file using the 'from_qasm' method and the 'from_qasm_file' method
as shown below.

    >>> qc = QCirc.from_qasm(qasm)  # qasm: OpenQASM string
    >>> qc = QCirc.from_qasm_file("foo.qasm")  # foo.qasm: OpenQASM file

However, it does not supported to non-unitary gates or user customized
gate.  The 14 types of gates are supported --
'x','y','z','h','s','sdg','t','tdg','cx','cz','ch','rx','rz','crz'.

### Equivalent of quantum circuits (using "PyZX")

The two quantum circuits may represent a unitary gate that has the
same effect, even if the appearance is different.  Here, we will call
it "equivalence" in contrast the above-mentioned "identicality".  In
qlazy, you can determine whether they are equivalent using the
'equivalent' method (but non-unitary gates are not supported).  Qlazy
uses a python package ["PyZX"](https://github.com/Quantomatic/pyzx)
that can calculate ZX-Calculus, so when using this function, the
"PyZX" must be installed.

Here is a simple example.  Let's make sure that 

    --H--*--H--
    --H--X--H--

and

    ---X---
    ---*---

is equivalent (This is a useful formula to know).

    >>> qc_A = QCirc().h(0).h(1).cx(0,1).h(0).h(1)
    >>> qc_B = QCirc().cx(1,0)
    >>> print(qc_A == qc_B)
    False
    >>> print(qc_A.equivalent(qc_B))
    True

Certainly it is not identical because it looks different, but it was
confirmed that the value (effectiveness) was the same (equivalent).

### Optimization of quantum circuit

The non-clifford, T Gate, play an important roll in many quantum
algorithms, but it is a difficult gate in terms of hardware
implementation, so it is desirable that the T gate is excluded as much
as possible from the quantum circuit.  However, simply eliminating the
T gates will be a meaningless circuit, so it is necessary to reduce
the number of T gates such that the circuit is equivalent to the
original.  In this sense, many researches on quantum circuit
optimization has been done in various ways so far.  PyZX has
implemented circuit optimization methods using ZX-Calculus.  Qlazy can
perform the optimization using this PyZX 'full_optimize' function as
follows.

    >>> qc_opt = qc_ori.optimize()

As a trial, let us generate a circuit randomly containing 'h', 'cx',
and 't', and see the effect of optimization by using the 'get_stats'.

    >>> qc = QCirc.generate_random_gates(qubit_num=10, gate_num=100, prob={'h':5, 'cx':5, 't':3})
    >>> qc_opt = qc.optimize()
	>>> print("== before ==")
    >>> print(qc.get_stats())
	>>> print("== after ==")
    >>> print(qc_opt.get_stats())

Then you get the following results.

    == before ==
    {'qubit_num': 10, 'cmem_num': 0, 'gate_num': 100, 'gate_freq': Counter({'cx': 45, 'h': 29, 't': 26}), 'gatetype_freq': Counter({'unitary': 100, 'clifford': 74, 'non-clifford': 26})}
    == after ==
    {'qubit_num': 10, 'cmem_num': 0, 'gate_num': 107, 'gate_freq': Counter({'cx': 55, 'h': 15, 'cz': 14, 'rz': 7, 's_dg': 5, 's': 4, 't': 3, 'z': 2, 'x': 2}), 'gatetype_freq': Counter({'unitary': 107, 'clifford': 97, 'non-clifford': 10})}

The non-clifford gate is reduced from 26 to 10 (T: 3, RZ: 7).
Instead, another clifford gate is added. But it is more desirable that
the non-clifford gate is decreased.

### Interface with PyZX

PyZX has various quantum circuit optimization functions.  It also have
some functions to display and edit a ZX-calculus graph.  For those who
want to play with ZX-calculus, qlazy has functions to input and output
PyZX circuit.

    >>> zxqc = qc.to_pyzx()
	
This allows you to get a PyZX 'Circuit' class instance.

    >>> qc = QCirc.from_pyzx(zxqc)
	
This allows you to convert PyZX's 'Circuit' class instances to qlazy's
'QCirc' class instances.

#### Custom gate

By inheriting the 'QCirc' class, you can easily create and add your
own quantum gate as follows.

    >>> class MyQCirc(QCirc):
    >>>     def bell(self, q0, q1):
    >>>         self.h(q0).cx(q0,q1)
    >>>         return self
	>>> 
    >>> bk = Backend()
    >>> qc = MyQCirc().bell(0,1).measure(qid=[0,1], cid=[0,1])
    >>> result = bk.run(qcirc=qc, shots=10)
    >>> ...

This is a very simple example, so you may not feel much profit, but
there are many situations where you can use it, such as when you want
to create a large quantum circuit.


### Parametric quantum circuit

If you want to execute the quantum circuit repeatedly while changing
the parameters contained in the quantum circuit, you can use
parametric quantum circut.

For example, Suppose you have the following quantum circuit.

    >>> qc = QCirc().h(0).rz(0, phase=0.2).cx(0,1).crx(0,1, phase=0.3).measure(qid=[0,1], cid=[0,1])

It has an 'rz' gate with parameter '0.2' and a 'crx' gate with
parameter '0.3'.  After executing this quantum circuit, if you want to
execute the quantum circuit changing this parameter from (0.2, 0.3) to
(0.4, 0.5), you need to generate a new quantum circuit from scratch as
follows.

    >>> qc = QCirc().h(0).rz(0, phase=0.4).cx(0,1).crx(0,1, phase=0.5).measure(qid=[0,1], cid=[0,1])

If your quantum circuit is very deep and is operated many times, this
method is very useless.  In such a case, you can create a parametric
quantum circuit as follows.

    >>> qc = QCirc().h(0).rz(0, tag='foo').cx(0,1).crx(0,1, tag='bar').measure(qid=[0,1], cid=[0,1])

Here, you set a tag name in the 'tag' option instead of specifing
the 'phase' parameter.  When setting each parameter to 0.2,0.3, use
'set_params' method to set the phase value corresponding to each tag
name as follows.

    >>> qc.set_params({'foo': 0.2, 'bar': 0.3})
	
This means that a quantum circuit containing a specific phase value
has been created.  You can execute this circuit as follows,

    >>> bk = Bakcend()
	>>> result = bk.run(qcirc=qc, ...)

Then, if you want to change the parameters to 0.4,0.5, do as follows,

    >>> qc.set_params({'foo': 0.4, 'bar': 0.5})
    >>> bk.run(qcirc=qc, ...)

There is no need to create another quantum circuit.

The value of the set parameters can be obtained by the 'get_params'
method as follows.

    >>> print(qc.get_params())
	>>> {'foo': 0.4, 'bar': 0.5}

### Adding a control qubit

If you want to add a control qubit to your quantum circuit, use the
'add_control' method.  Suppose you have a following quantum circuit,

    >>> qc = QCirc().x(1).z(2)
    >>> qc.show()
    q[0] ---
    q[1] -X-
    q[2] -Z-

to add the 0th qubit as a control qubit, set 0 in the 'qctrl' option
of the 'add_control' method as follows.

    >>> qc_ctrl = qc.add_controll(qctrl=0)
    >>> qc_ctrl.show()
    q[0] -*-*-
    q[1] -X-|-
    q[2] ---Z-

This is a very simple example, so you may not feel so much profit.
Here are some more complicated example.

    >>> qc = QCirc().crz(0,1, phase=0.3)
    >>> qc.show()
    q[0] -*-------
    q[1] -RZ(0.3)-

For such quantum circuit, to add the 2nd qubit as a control qubit, set
2 in the 'qctrl' option as follows.

    >>> qc_ctrl = qc.add_controll(qctrl=2)
    >>> qc_ctrl.show()
    q[0] ------------*-------RZ(0.25)-X---*--------RZ(-0.25)-X--------------------------------*-------RZ
    q[1] -RZ(0.15)-H-RZ(0.5)-H--------|-H-RZ(-0.5)-H---------|-H-RZ(0.5)-H--------RZ(-0.15)-H-RZ(0.5)-H-
    q[2] -*---------------------------*----------------------*---*-------RZ(0.25)-*---------------------
    
    (0.25)-X---*--------RZ(-0.25)-X--------------------
    -------|-H-RZ(-0.5)-H---------|-H-RZ(0.5)-H--------
    -------*----------------------*---*-------RZ(0.25)-

### Remapping the qubit id and the classical bit id

If you want to change the qubit id and the classical bit id of the
created quantum circuit, you can use 'remap' method.  Suppose you have
the following quantum circuit.

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
    >>> qc.show()
    q[0] -H-*-M---
    q[1] ---X-|-M-
    c  =/=====v=v=
    2         0 1

When you change the qubit id [0,1] of this to [1,0] and the classical
bit id [0 ,1] to [1,0], set [1,0] in the 'qid' option and set [1,0] in
the 'cid' option of 'remap' method.

    >>> qc_new1 = qc.remap(qid=[1,0], cid=[1,0])
    >>> qc_new1.show()
    q[0] ---X---M-
    q[1] -H-*-M-|-
    c  =/=====v=v=
    2         1 0

This allows you to get a new quantum circuit 'qc_new1'.  In addition,
the quantum circuit where the quantum bit id is changed to [2,1] and
the classical bit id to [1,0] can be created as follows.

    >>> qc_new2 = qc.remap(qid=[2,1], cid=[1,0])
    >>> qc_new2.show()
    q[0] ---------
    q[1] ---X---M-
    q[2] -H-*-M-|-
    c  =/=====v=v=
    2         1 0


## Supported backend

Supported backends in the current version of qlazy are 
[qulacs](https://github.com/qulacs/qulacs),
[IBM Quantum](https://quantum-computing.ibm.com/)
and [Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls)
Usage of each backend is described following.

### qulacs

[qulacs](https://github.com/qulacs/qulacs) is an open source quantum
circuit simulator provided by [Qunasys](https://qunasys.com/).  It has
the feature that high-speed calculations can be performed using GPU.
If you want to execute a high-speed calculation using GPU with a
simple interface of qlazy, we recommend using this backend.

#### Install

First, install qulacs referring to
[Installation - Qulacs documentation](http://docs.qulacs.org/en/latest/intro/1_install.html).

#### Usage

In the case of using CPU simulator:

    >>> bk = Backend(product='qulacs', device='cpu_simulator')

In the case of using GPU simulator:

    >>> bk = Backend(product='qulacs', device='gpu_simulator')

Then, add quantum gates and 'run' as follows.

	>>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcirc=qc, shots=100)

### IBM Quantum

[IBM Quantum (IBMQ)](https://quantum-computing.ibm.com/) is a cloud
service to use quantum computer (and simulator) developed by
[IBM](https://www.ibm.com/).

#### Install

Install [qiskit](https://qiskit.org/), a library for using IBMQ and
local simulators from Python, and execute quantum calculations.
Please prepare the environment.

#### Usage

In the case of using local simulator:

    >>> bk = Backend(product='ibmq', device='aer_simulator')

In the case of using real quantum computer (least busy):

    >>> bk = Backend(product='ibmq', device='least_busy')

The 'least_busy' is to automatically select and execute the most
vacant systems in the quantum computer system available in your
account.  You can also explicitly specify the executable system.  In
the case of using real quantum computer, 'ibmq_athens':

    >>> bk = Backend(product='ibmq', device='ibmq_athens')
	
You can check the device that can be used in IBMQ as follows.

	>>> print(Backend.devices('ibmq'))
    ['aer_simulator', 'qasm_simulator', 'least_busy', 'ibmq_armonk', 'ibmq_bogota', 'ibmq_lima', 'ibmq_belem', 'ibmq_quito', 'ibmq_manila']

Then, add quantum gates and 'run' as follows.

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

### Amazon Braket

[Amazon Braket](https://aws.amazon.com/braket/?nc1=h_ls) is a cloud
service to use quantum computer of [IonQ](https://ionq.com/),
[Rigetti](https://www.rigetti.com/), [Oxford Quantum
Circuits](https://oxfordquantumcircuits.com/), etc.  It also have some
simulators developed by [AWS](https://aws.amazon.com/).

#### Install

[AWS](https://aws.amazon.com/jp/console/) account is required. Please
get your account first.  Then, make your local PC possible to use
[Amazon Braket](https://aws.amazon.com/braket/) with reference to the
following.

- [amazon-braket-sdk-python](https://github.com/aws/amazon-braket-sdk-python)

If the following code work without any problems, you can think that
the usage environment of [Amazon Braket](https://aws.amazon.com/brashet/?nc1=h_ls) is set (maybe).

    >>> import boto3
    >>> from braket.aws import AwsDevice
    >>> from braket.circuits import Circuit
    >>> 
    >>> device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
    >>> s3_folder = ("amazon-braket-xxxx", "sv1") # Use the S3 bucket you created during onboarding
    >>> 
    >>> bell = Circuit().h(0).cnot(0, 1)
    >>> task = device.run(bell, s3_folder, shots=100)
    >>> result = task.result()
    >>> print(result.measurement_counts)

In addition, create a directory called "~/.qlazy/" in your home
directory and set 'config.ini' under this directory as follows.

    $ cat ~/.qlazy/config.ini
    [backend_braket]
    backet_name = amazon-braket-xxxx

For the 'amazon-braket-xxxx', write the S3 backet name created to use
Amazon Braket.  If you want to change 'poll_timeout_seconds' from the
default value (5 days), specify as follows.

    [backend_braket]
    backet_name = amazon-braket-xxxx
	poll_timeout_seconds = 86400

The above example is to set 1 day (= 86400 sec).

#### Usage

Specify 'product' and 'device' options when generating a backend
instance.  Available products are 'braket_local'(local simulator),
'braket_aws'(simulator working on AWS), 'braket_ionq'(quantum computer
of IonQ), 'braket_rigetti'(quantum computer of Rigetti),
'braket_oqc'(quantum computer of Oxford Quantum Circuits).  The
'device' that can be used for each 'product' is as follows.

- braket_local
    - braket_sv (state vector simulator)
- braket_aws
    - sv1 (state vector simulator)
    - tn1 (tensor network simulator)
    - dm1 (density matrix simulator)
- braket_ionq
    - ionq (IonQ)
- braket_rigetti
    - aspen_11 (Aspen-11)
    - aspen_m_1 (Aspen-M-1)
- braket_oqc
    - lucy (Lucy)

In the case of using local state vector simulator:

    >>> bk = Backend(product='braket_local', device='braket_sv')

In the case of using state vector simulator on AWS:

    >>> bk = Backend(product='braket_aws', device='sv1')

In the case of using quantum computer of IonQ:

    >>> bk = Backend(product='braket_ionq', device='ionq')

In the case of using quantum computer, Aspen-M-1 of Rigetti:

    >>> bk = Backend(product='braket_rigetti', device='aspnen_m_1')

In the case of using quantum computer, Lucy of OQC:

    >>> bk = Backend(product='braket_oqc', device='lucy')

Then, add quantum gates and 'run' as follows.

    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
    >>> result = bk.run(qcic=qc, shots=100)

#### Notes

It seems that Amazon Braket only accepts quantum circuits where the
measurement is last.  Therefore, the 'ctrl' option that is turned on
or off according to the measured value cannot be used.  In addition,
'product' other than 'braket_local' is charged.  Please refer to the
following page.

[Amazon Braket Pricing](https://aws.amazon.com/jp/braket/pricing/)


## How to use GPU version

High-speed quantum circuit execution using GPU is possible without
'qulacs' (from V0.3.0).  To use it, you need to install a GPU version
of qlazy from the source code as follows.

    $ git clone https://github.com/samn33/qlazy.git
    $ cd qlazy
    $ python setup_gpu.py install --user

It is assumed that the NVIDIA CUDA11 environment is in place for installation.

To see if the GPU version was installed, execute the folloing command.

    $ qlazy -v

If the installation is successful, it will display as follows.

    * Version: 0.3.0-cuda

If displayed as follows, your qlazy is CPU version, sorry.

    * Version: 0.3.0

Now, if the GPU version is installed, it can be used very easily.

In the case of using the CPU version, the backend was set and the
quantum circuit was executed as follows.

    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

In the case of using the GPU version, just set the device to
'qstate_gpu_simulator' when creating a backend instance.

    >>> from qlazy import QCirc, Backend
    >>> bk = Backend(product='qlazy', device='qstate_gpu_simulator')
    >>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcic=qc, shots=100)

There is no need to import like 'qlazy-gpu'.  We don't have such
package, only have 'qlazy'.  However, in the current version, only the
quantum circuit calculation using the state vector simulator is
available in the GPU version.  GPU version of QState, DensOp,
Stabilizer, MPState class is not available.
