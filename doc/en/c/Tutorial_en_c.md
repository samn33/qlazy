Command Line Tool
=================

## Executing quantum circuit file

We will get started to show a simple example. Prepare the following
files (foo.qc).

    $ cat foo.qc
    init 2
    h 0
    cx 0 1
    m

If you execute this with qlazy command, you can get a measurement
result as follows

    $ qlazy -qc foo.qc
    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00

In the foo.qc file,

- 1st line: Initialize 2-qubit system.
- 2nd line: Operate a hadamard gate on the 0th qubit.
- 3rd line: Operate a control not gate on the 0th and the 1st qubit.
- 4th line: Measure the all qubit.

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

If you insert 'show' command after the 'cx' gate (controlled-X gate),

    init 2
    h 0
    cx 0 1
    show

the quantum state at this point can be displayed as follows.

    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++

Since the quantum state is superposition of eigenstates |00>, |01>, |10>, |11>
in 2-qubit system, the state can be expressed in four complex numbers
(called complex amplitudes or probability amplitudes) correspond to each eigenstate.
The "c[00] = +0.7071+0.0000*i : ..." shows the complex amplitude correspond to the eigenstate |00> etc.
Here, note that qubit order is from left to right in qlazy,
so |01> means |0> at the 0th qubit and |1> at the 1st qubit.
Real number on the right of complex amplitude (0.5000 or 0.0000) is
absolute value of each complex, that is probability of the eigenstate.
The "++++++" displayed on the right is a stick graph to make
visually easy to understand each probability value.

## Executing in dialogue mode (quantum calculator)

You can also calculate in dialogue mode as follows:

    $ qlazy
	>> init 2
	>> h 0
	>> cx 0 1
	>> show
    c[00] = +0.7071+0.0000*i : 0.5000 |++++++
    c[01] = +0.0000+0.0000*i : 0.0000 |
    c[10] = +0.0000+0.0000*i : 0.0000 |
    c[11] = +0.7071+0.0000*i : 0.5000 |++++++
	>> m
    direction of measurement: z-axis
    frq[00] = 49
    frq[11] = 51
    last state => 00
	>> quit

In the dialogue mode, when help,

	>> help
    [commands]
    * initialize quantum state: %,init
    * print quantum circuitt:   &,circ                                                       
    * print quantum gates:      !,gates
    * print quantum state:      -,show
    * print bloch angles:       |,bloch
    * echo input string:        @,echo
    * output quantum gates:     >,output
    * quit:                     .,quit
    * help:                     ?,help
    [quantum gates]
    * 1-qubit gates:            x,y,z,xr,xr_dg,h,s,s_dg,t,t_dg,p,rx,ry,rz
    * 2-qubit gates:            cx,cy,cz,cxr,cxr_dg,ch,cs,cs_dg,cp,crx,cry,crz,sw,rxx,ryy,rzz
    * measurement:              m,mx,my,mz,mb
    * reset:                    reset
    [notes]
    * see 'help <item>', for more information

is obtained.  You can see the available commands and quantum gates.
If you want to refer the command or quantum gate details, use "help ..." as follows.

    >> help x
    == X gate ==
    [description]
      X gate is 1-qubit gate called 'pauli X gate'.
      - matrix expression:
        | 0 1 |
        | 1 0 |
    [usage]
      >> x <qubit_id>
