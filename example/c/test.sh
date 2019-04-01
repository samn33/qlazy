#!/bin/bash

qc_list=`ls *.qc`
for qc in ${qc_list[@]}; do
    echo "***** ${qc} *****"
    qlazy -qc ${qc} -tm
    read -p "Hit enter: "
    echo ""
done
