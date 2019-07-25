init 3

x 0
x 1

@ == initial state ==
show

# toffoli gate
# ccx 0 1 2

cxr 1 2
cx 0 1
cxr+ 1 2
cx 0 1
cxr 0 2

@ == final state ==
show

@ == measurement ==
m
