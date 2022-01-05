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
    Arithmetic
    Shor
    Grover
    Toffoli
    DensityOperator
    PartialTrace
    POVM
    SchmidtDecomp
    Purification
    TraceDistance
    Fidelity
    QChannel
    Entropy
    Holevo
    QuantumTomography
    DataCompression
    ErrorCorrection
    SurfaceCode
    LatticeSurgery
)
for dir in ${directories[@]}; do

    cd ${dir}

    py_list=`ls *.py`
    for py in ${py_list[@]}; do
	echo "***** ${dir}/${py} *****"
	python3 ${py}
	read -p "Hit enter: "
	echo ""
    done

    cd ..
    
done
