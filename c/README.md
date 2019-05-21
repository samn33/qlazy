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
    measurement:              M,MX,MY,MZ
    [notes]
    see 'help <item>', for more information

### init - initialize quantum state

    [description]
      This command makes all qubits to set |0>.
      You must initialize before operating any quantum gate.
    [usage]
      >> input <qubit_num>
    [alias]
      %
    [examle]
      >> input 2

### circ - print quantum circuit

    [description]
      This command visualize quantum circuit with text.
    [usage]
      >> circ
    [alias]
      &
    [example]
      >> circ
      0 -H-*--M---
      1 ---CX---M-

### gates - print quantum gates

    [description]
      This command print quantum gates in order of operation.
    [usage]
      >> gates
    [example] 
      >> gates
      % 2
      H 0
      CX 0 1
    [alias]
      !

### show - print quantum state

    [description] \n\
      This command shows the probability amplitudes of current quantum state.
    [note]
      - Normalize that amplitude of |00..0> is real and positive value,
        and eliminate the phase factor.
      - If 'show' the qubit that entangled to other qubits,
        then 'show' result is probabilistic.
    [usage] 
      >> show 
      >> show <qubit_id>...
    [alias]
      - 
    [example] 
      >> show 
      c[00] = +0.7071+0.0000*i : 0.5000 |+++++ 
      c[01] = +0.0000+0.0000*i : 0.0000 | 
      c[10] = +0.0000+0.0000*i : 0.0000 | 
      c[11] = +0.7071+0.0000*i : 0.5000 |+++++ 

### bloch - print bloch angles

    [description]
      This command prints the bloch angles of current quantum state.
    [note]
      If no arguments are set, it prints the angles of 0-th qubit.
    [usage]
      >> bloch
      >> bloch <qubit_id>
    [alias]
      |

### echo - echo strings

    [description] 
      This command print any strings you set folloing to 'echo' 
    [usage] 
      >> echo <strings>
    [alias]
      @
    [example] 
      >> echo hello world. 
      hello world.

### output - output quantum gates

    [description] 
      This command outputs current quantum gates to quantum gates file.
    [usage] 
      >> output <file>
    [alias]
      >
    [example] 
      >> output foo 
      >> quit 
      $ cat foo 
      % 2 
      H 0 
      CX 0 1 

### quit - quit interactive mode

    [description] 
      This command is to quit interactive mode and return to your shell. 
    [usage] 
      >> quit
    [alias]
      .
    [example] 
      >> quit 
      $

### M - M gate

    [description]
      M gate is to measure the current quantum state from any direction.
      You can set number of mesurements (=shots), mesurement direction (=angle,phase),
      and set qubit id you want to measure.
      Default shots is 100, default angle,phase is 0.0 (z-axis),
      and default qubit id's are all (all of the qubit id's are measured).
    [note]
      Definition of 'angle' and 'phase' ...
      - angle ... angle formed by z-axis in bloch sphere (unit: PI radian) 
      - phase ... angle around z-axis in bloch sphere (unit: PI radian)
      If angle,phase aren't zero value, then measured state is u/d instead of 0/1.
    [usage] 
      >> M
      >> M <qubit_id> ...
      >> M(<shots>)
      >> M(<shots>) <qubit_id> ...
      >> M(<shots>,<angle>,<phase>) <qubit_id> ...
    [alias]
      m
    [example] 
      >> M 
      direction of measurement: x-axis
      frq[00] = 53 
      frq[11] = 47 
      last state => 11
      >> M(10) 
      direction of measurement: x-axis
      frq[00] = 4 
      frq[11] = 6 
      last state => 00
      >> M(10) 1 
      direction of measurement: x-axis
      frq[0] = 5 
      frq[1] = 5 
      last state => 0
      >> M(10,0.3,0.2) 1 
      direction of measurement: RX(0.300*PI),RZ(0.200*PI)
      frq[u] = 5 
      frq[d] = 5 
      last state => u

### MX - MX gate

    [description]
      MX gate is to measure the current quantum state from x-direction in bloch sphere.
      You can set number of mesurements (=shots) and set qubit id you want to measure.
      Default shots is 100, and default qubit id's are all
      (all of the qubit id's are measured).
    [note]
      Measured state is u/d instead of 0/1.
    [usage]
      >> MX
      >> MX <qubit_id>...
      >> MX(<shots>)
      >> MX(<shots>) <qubit_id>...
    [alias]
      mx
    [example] 
      >> MX
      direction of measurement: x-axis
      frq[uu] = 53 
      frq[dd] = 47 
      last state => dd
      >> MX(10) 
      direction of measurement: x-axis
      frq[uu] = 4 
      frq[dd] = 6 
      last state => uu
      >> MX(10) 1 
      direction of measurement: x-axis
      frq[u] = 5 
      frq[d] = 5 
      last state => u
  
### MY - MY gate

    [description]
      MY gate is to measure the current quantum state from y-direction in bloch sphere.
      You can set number of mesurements (=shots) and set qubit id you want to measure.
      Default shots is 100, and default qubit id's are all
      (all of the qubit id's are measured).
    [note]
      Measured state is u/d instead of 0/1.
    [usage]
      >> MY
      >> MY <qubit_id>...
      >> MY(<shots>)
      >> MY(<shots>) <qubit_id>...
    [alias]
      my
    [example] 
      >> MY
      direction of measurement: y-axis
      frq[uu] = 53 
      frq[dd] = 47 
      last state => dd
      >> MY(10) 
      direction of measurement: y-axis
      frq[uu] = 4 
      frq[dd] = 6 
      last state => uu
      >> MY(10) 1 
      direction of measurement: y-axis
      frq[u] = 5 
      frq[d] = 5 
      last state => u
  
### MZ - MZ gate

    [description]
      MZ gate is to measure the current quantum state from z-direction in bloch sphere.
      You can set number of mesurements (=shots) and set qubit id you want to measure.
      Default shots is 100, and default qubit id's are all
      (all of the qubit id's are measured).
    [note]
      Measured state is u/d instead of 0/1.
    [usage]
      >> MZ
      >> MZ <qubit_id>...
      >> MZ(<shots>)
      >> MZ(<shots>) <qubit_id>...
    [alias]
      mz
    [example] 
      >> MZ
      direction of measurement: z-axis
      frq[00] = 53 
      frq[11] = 47 
      last state => 11
      >> MY(10) 
      direction of measurement: z-axis
      frq[00] = 4 
      frq[11] = 6 
      last state => uu
      >> MY(10) 1 
      direction of measurement: z-axis
      frq[0] = 5 
      frq[1] = 5 
      last state => 0

### MB - MB gate

    [description]
      MB gate is to execute 2-qubit Bell-measurement.
      You can set number of mesurements (=shots) 
      and set 2 qubit id's you want to bell-measure. Default shots is 100.\n\
    [usage] \n\
      >> MB <qubit_id> <qubit_id>
      >> MB(<shots>) <qubit_id> <qubit_id>
    [alias] \n\
      mb \n\

### X

    [description] 
      X gate is 1-qubit gate called 'pauli X gate'. 
      - matrix expression:
          | 0 1 | 
          | 1 0 | 
    [usage] 
      >> X <qubit_id>
    [alias]
      x
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
    [alias]
      y
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
    [alias]
      z
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
    [alias]
      xr
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
    [alias]
      xr+
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
    [alias]
      h
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
    [alias]
      s
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
    [alias]
      s+
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
    [alias]
      t
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
    [alias]
      t+
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
    [alias]
      rx
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
    [alias]
      ry
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
    [alias]
      rz
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
    [alias]
      cx
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
    [alias]
      cz
    [example] 
      >> CZ 0 1 

### CCX

    [description] 
      CCX gate is 3-qubit gate called 'controlled-controlled-X gate' or 'toffoli gate'.
      It flips the third qubit if and only if the first and second qubit are both |1>.
      - quantum circuit expresson:
          q00 --*---- 
          q01 --*---- 
          q02 --CCX-- 
      - equivalent another expresson:
          q00 ----------*----------*--------*--T----*--- 
          q01 ----*----------*--------T-----CX---T+-CX-- 
          q02 --H-CX-T+-CX-T-CX-T+-CX---T-H------------- 
    [usage] 
      >> CCX <qubit_id> <qubit_id> <qubit_id>
    [alias]
      ccx
    [example] 
      >> CCX 0 1 2
