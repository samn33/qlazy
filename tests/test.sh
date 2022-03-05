#!/bin/bash

py_list=`ls *.py`
for py in ${py_list[@]}; do
    echo "***** ${py} *****"
    python3 -m unittest ${py}
    echo ""
done
