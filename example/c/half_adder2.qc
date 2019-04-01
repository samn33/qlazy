# calculate a+b (a,b={0,1})
# - set binary number on 0,1-qubit, measure 2,3-qubit

init 4

x 0
x 1

@ == initial state ==
show

ccx 0 1 2
cx 0 3
cx 1 3

@ == final state ==
show

@ == measurement ==
m(50) 0 1 2 3
