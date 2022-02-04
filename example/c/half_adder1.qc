init 3

x 0

@ == initial state ==
show

cxr 1 2
cx 0 1
cxr_dg 1 2
cx 0 1
cxr 0 2

cx 0 1

@ == final state ==
show

@ == measurement ==
m(100)