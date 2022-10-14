Useful tools
============

## Register related tools

If you want to do a quantum programming with a large-scale quantum
circuit, register related tools are useful.

To use these, you should import 'CreateRegister' and 'InitRegister'
functions from 'qlazy.tools.Register' first.

    >>> from qlazy.tools.Register import CreateRegister,InitRegister

The typical usage is as follows.

    >>> dat = CreateRegister(3)
    >>> anc = CreateRegister(2)
    >>> qubit_num = InitRegister(dat, anc)

This is an example of preparing three data qubits ('dat') and two
ancilla qubits ('anc').  Print the 'dat' and the 'anc', you will get
following list.

    >>> print(dat)
    [0,1,2]
	>>> print(anc)
    [3,4]
    >>> print(qubit_num)
    5

In this way, by using the 'CreateRegister' and the 'InitRegister'
functions, you can get the qubit id list for data qubits and ancilla
qubits so that the qubit id's do not overlap.  Besides the total
number of qubits is returned as a result of the 'InitRegister'
function.

Other example is as follows.

    >>> qid = CreateRegister(3,3)
	>>> qubit_num = InitRegister(qid)

You can get 3x3 registers arrays like as follows.

    >>> print(qid)
    [[0,1,2],[3,4,5],[6,7,8]]
    >>> print(qubit_num)
    9

Similarly, you can get arrays of 3-dimensional or more as follows.

    >>> qid = CreateRegister(2,3,4)
    >>> qubit_num = InitRegister(qid)
    >>> print(qid)
    [[[0,1,2,3],[4,5,6,7],[8,9,10,11]],[[12,13,14,15],[16,17,18,19],[20,21,22,23]]]
    >>> print(qubit_num)
    24

When you want to set both quantum registers and classical registers, do as follows.

    >>> # quantum register
    >>> qid = CreateRegister(2)
    >>> qubit_num = InitRegister(qid)
	>>> 
    >>> # classical register (classical memory)
    >>> cid = CreateRegister(2)
    >>> cmem_num = InitRegister(cid)
	>>> 
	>>> # prepare a quantum computer as a backend
    >>> bk = Backend(product='qlazy', device='qstate_simulator')
	>>> 
	>>> # setting and execution of quantum circuit
    >>> qc = QCirc().h(qid[0]).cx(qid[0],qid[1]).measure(qid=qid[0], cid=cid[0])
    >>> ...
    >>> result = bk.run(qcirc=qc, shots=10)
    >>> ...


## Probability distribution related tools

When you execute a quantum circuit including measurements, the result
contains measurement frequencies.  For example,

    >>> from qlazy import QCirc, Backend
	>>> bk = Backend()
	>>> qc = QCirc().h(0).cx(0,1).measure(qid=[0,1], cid=[0,1])
	>>> result = bk.run(qcirc=qc, shots=100)
	>>> print(result.frequency)
	Counter({'00': 52, '11': 48})

Here, you might like to compare and evaluate several different
measurement results obtained in this way.  In such a case, probability
distribution related tools are useful.

To use these, you should import some functions from 'qlazy.tools.Probability' first.

    >>> from qlazy.tools.Probability import freq2prob, entropy, kl_divergence, cross_entropy

The 'freq2prob' function is to convert a frequency distribution like
Counter({'00': 52, '11': 48}) to a probability distribution like
Counter({'00': 0.52, '11': 0.48}).

You should get probability distributions with this function to use the
'entropy', 'kl_divergence' and 'cross_entropy' functions.  For
example, do as follows.

    >>> prob = freq2prob(freq)
	>>> print(prob)
	{'00': 0.52, '11': 0.48}

If you want to know an entropy for the probability distribution,
use the 'entropy' function.

    >>> ent = entropy(prob)
	>>> print(ent)
    0.9988455359952018
	
To get the KL-divergence of two probability distributions ('prob_0' and 'prob_1'),
use the 'kl_divergince' function as follows.

	>>> kl_div = kl_divergence(prob_0, prob_1)

To get the cross entropy of the two probability distributions ('prob_0' and 'prob_1'),
use the 'cross_entropy' function as follows.

	>>> c_ent = cross_entropy(prob_0, prob_1)
