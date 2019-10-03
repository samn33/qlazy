init 3

x 0
x 1

@ == initial state ==
show

# fredkin
cx 2 1

cxr 1 2
cx 0 1
cxr+ 1 2
cx 0 1
cxr 0 2

cx 2 1

@ == final state ==
show

@ == measurement ==
m 0 1 2
