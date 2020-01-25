#!/bin/bash

directories=(
    QuantumTeleportation
    MeasureSpin
    OneWayQC
    CHSHInequality
    LamorPrecession
    HadamardTest
    QFT
    PEA
    VQE
    DeutschJozsa
    LogicalFunction
    Shor
    Grover
    Toffoli
    DensityOperator
    PartialTrace
    POVM
    Schmidt
    Purification
    TraceDistance
    Fidelity
    QChannel
    Entropy
    Holevo
    QuantumTomography
    DataCompression
)
for dir in ${directories[@]}; do

    cd ${dir}

    py_list=`ls *.py`
    for py in ${py_list[@]}; do
	echo "***** ${dir}/${py} *****"
	python ${py}
	read -p "Hit enter: "
	echo ""
    done

    cd ..
    
done

	   



# py_list=`ls *.py`
# for py in ${py_list[@]}; do
#     echo "***** ${py} *****"
#     python ${py}
#     read -p "Hit enter: "
#     echo ""
# done


