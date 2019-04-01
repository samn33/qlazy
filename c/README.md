qlazy
=====

command and library of quantum computer simulator

## Description

'qlazy' is a command of quantum computer simulator. 'libqlazy.so' is
the library used by 'qlazy' that supports fundamental quantum gates
and measurement.
 
## Usage

### qlazy command

    qlazy - quantum computer simulator ==
    [option]
    -qc FILE : quantum circuit file name (default:interactive mode)
    -sd SEED : seed of randam generation for measurement (default:time)
    -tm      : output processing time 
    -pr      : print circuit and exit (don't run) 
    -h       : print this usage and exit
    -V       : print this version and exit
    [example]
    $ cat foo.qc
	init 2
    h 0
    cx 0 1
    m
    $ qlazy -qc foo.qc
    => run circuit
    $ qlazy -qc foo.qc -pr
    => print circuit (don't run)
    $ qlazy
    => interactive mode

## Operateors

    [commands]
    initialize quantum state: %,init
    print quantum circuitt:   &,circ
    print quantum gates:      !,gates
    print quantum state:      -,show
    echo input string:        @,echo
    output quantum gates:     >,output
    quit:                     .,quit
    help:                     ?,help
    [quantum gates]
    1-qubit gates:            X,Y,Z,XR,XR+,H,S,S+,T,T+,RX,RY,RZ
    2-qubit gates:            CX,CZ
    3-qubit gates:            CCX
    measurement:              M
    [notes]
    see 'help <item>', for more information

### init(%) - initialize quantum state

    [description]
    This command makes all qubits to set |0>.
    You must initialize before operating any quantum gate.
    [usage]
    >> input <qubit_num>
    >> % <qubit_num>
    [example]
    >> input 4
    >> % 3

### circ(&) - print quantum circuit

    [description]
    This command visualize quantum circuit with text.
    [usage]
    >> circ
    >> &
    [example]
    >> circ
    0 -H-*--M---
    1 ---CX---M-

### gates(!) - print quantum gates

    [description]
    This command print quantum gates in order of operation.
    [usage]
    >> gates
    >> !
    [example] 
    >> gates 
    % 2 
    H 0 
    CX 0 1 

### show(-) - print quantum state

    [description] 
    This command shows the probability amplitude for each eigen state 
    [usage] 
    >> show 
    >> - 
    [example] 
    >> show 
    c[00] = +0.7071+0.0000*i : 0.5000 |+++++ 
    c[01] = +0.0000+0.0000*i : 0.0000 | 
    c[10] = +0.0000+0.0000*i : 0.0000 | 
    c[11] = +0.7071+0.0000*i : 0.5000 |+++++ 

### echo(@) - echo strings

    [description] 
    This command print any strings you set folloing to 'echo' 
    [usage] 
    >> echo <strings>
    >> @ <strings>
    [example] 
    >> echo hello world. 
    hello world.

### output(>) - output quantum gates

    [description] 
    This command outputs current quantum gates to quantum gates file.
    [usage] 
    >> output <file>
    >> > <file>
    [example] 
    >> output foo 
    >> quit 
    $ cat foo 
    % 2 
    H 0 
    CX 0 1 

### quit(.) - quit interactive mode

    [description] 
    This command is to quit interactive mode and return to your shell. 
    [usage] 
    >> quit
    >> .
    [example] 
    >> quit 
    $

### M - M gate

    [description] 
    M gate is to measure the current quantum state.
    You can set number of mesurements (=shots), and set qubit id you want to measure.
    Default shots is %d, and default qubit id's are all
    (all of the qubit id's are measured).
    [usage] 
    >> M
    >> M(<shots>)
    >> M(<shots>) <qubit_id> ...
    [example] 
    >> M 
    frq[00] = 53 
    frq[11] = 47 
    last state => 11
    >> M(10) 
    frq[00] = 4 
    frq[11] = 6 
    last state => 00
    >> M(10) 1 
    frq[0] = 5 
    frq[1] = 5 
    last state => 0

### X

    [description] 
    X gate is 1-qubit gate called 'pauli X gate'. 
    - matrix expression:
        | 0 1 | 
        | 1 0 | 
    [usage] 
    >> X <qubit_id>
    [example] 
    >> X 0 

### Y

    [description] 
    Y gate is 1-qubit gate called 'pauli Y gate'. 
    - matrix expression:
        |  0 i | 
        | -i 0 | 
    [usage] 
    >> Y <qubit_id>
    [example] 
    >> Y 0 

### Z

    [description] 
    Z gate is 1-qubit gate called 'pauli Z gate'. 
    - matrix expression:
        | 1  0 | 
        | 0 -1 | 
    [usage] 
    >> Z <qubit_id>
    [example] 
    >> Z 0 

### XR

    [description] 
    XR gate is 1-qubit gate called 'root pauli X gate', satisfied X=XR*XR. 
    - matrix expression:
    | (1+i)/2 (1-i)/2 | 
    | (1-i)/2 (1+i)/2 | 
    [usage] 
    >> XR <qubit_id>
    [example] 
    >> XR 0 

### XR+

    [description] 
    XR+ gate is 1-qubit gate called 'hermitian conjugate of root pauli X gate'. 
    - matrix expression:
        | (1-i)/2 (1+i)/2 | 
        | (1+i)/2 (1-i)/2 | 
    [usage] 
    >> XR+ <qubit_id>
    [example] 
    >> XR+ 0 

### H

    [description] 
    H gate is 1-qubit gate called 'hadamard gate'. 
    - matrix expression:
        | 1/sqrt(2)  1/sqrt(2) | 
        | 1/sqrt(2) -1/sqrt(2) | 
    [usage] 
    >> H <qubit_id>
    [example] 
    >> H 0 

### S

    [description] 
    S gate is 1-qubit gate called 'phase shift gate'.
    It rotate through PI/2 around z-axis in bloch shpere. 
    - matrix expression:
        | 1 0 | 
        | 0 i | 
    [usage] 
    >> S <qubit_id>
    [example] 
    >> S 0 

### S+

    [description] 
    S+ gate is 1-qubit gate, hermitian conjugate of S gate. 
    - matrix expression:
        | 1  0 | 
        | 0 -i | 
    [usage] 
    >> S+ <qubit_id>
    [example] 
    >> S+ 0 

### T

    [description] 
    T gate is 1-qubit gate called 'phase shift gate'.
    It rotate through PI/4 around z-axis in bloch shpere. 
    - matrix expression:
        | 1 0             | 
        | 0 (1+i)/sqrt(2) | 
    [usage] 
    >> T <qubit_id>
    [example] 
    >> T 0 

### T+

    [description] 
    T+ gate is 1-qubit gate, hermitian conjugate of T gate. 
    - matrix expression:
        | 1 0             | 
        | 0 (1-i)/sqrt(2) | 
    [usage] 
    >> T+ <qubit_id>
    [example] 
    >> T+ 0 

### RX

    [description] 
    RX gate is 1-qubit gate. It rotate through any phase around x-axis in bloch spere. 
    - matrix expression:
        |  cos(phase*PI/2)   -i*sin(phase*PI/2) | 
        | -i*sin(phase*PI/2)  cos(phase*PI/2)   | 
    [usage] 
    >> RX(<phase>) <qubit_id>
    [example] 
    >> RX(0.5) 0 

### RY

    [description] 
    RY gate is 1-qubit gate. It rotate through any phase around y-axis in bloch spere. 
    - matrix expression:
        | cos(phase*PI/2) -sin(phase*PI/2) | 
        | sin(phase*PI/2)  cos(phase*PI/2) | 
    [usage] 
    >> RY(<phase>) <qubit_id>
    [example] 
    >> RY(0.5) 0 

### RZ

    [description] 
    RZ gate is 1-qubit gate, It rotate through any phase around z-axis in bloch spere.
    - matrix expression:
        | 1 0                             | 
        | 0 cos(phase*PI)+i*sin(phase*PI) | 
    [usage] 
    >> RZ(<phase>) <qubit_id>
    [example] 
    >> RZ(0.5) 0 

### CX

    [description] 
    CX gate is 2-qubit gate called 'controlled X gate' or 'controlled NOT (CNOT) gate'.
    It flips the second qubit if and only if the first qubit is |1>.
    - matrix expression:
    | 1 0 0 0 | 
    | 0 1 0 0 | 
    | 0 0 0 1 | 
    | 0 0 1 0 | 
    [usage] 
    >> CX <qubit_id> <qubit_id>
    [example] 
    >> CX 0 1 

### CZ

    [description] 
    CZ gate is 2-qubit gate called 'controlled Z gate'.
    It operate Z gate to the second qubit if and only if the first qubit is |1>.
    - matrix expression:
        | 1 0 0  0 | 
        | 0 1 0  0 | 
        | 0 0 1  0 | 
        | 0 0 0 -1 | 
    [usage] 
    >> CZ <qubit_id> <qubit_id>
    [example] 
    >> CZ 0 1 

### CCX

    [description] 
    CCX gate is 3-qubit gate called 'controlled-controlled-X gate' or 'toffoli gate'.
    It flips the third qubit if and only if the first and second qubit are both |1>.
    - quantum circuit expresson:
        0 --*---- 
        1 --*---- 
        2 --CCX-- 
    - equivalent another expresson:
        0 ----------*----------*--------*--T----*--- 
        1 ----*----------*--------T-----CX---T+-CX-- 
        2 --H-CX-T+-CX-T-CX-T+-CX---T-H------------- 
    [usage] 
    >> CCX <qubit_id> <qubit_id> <qubit_id>
    [example] 
    >> CCX 0 1 2
