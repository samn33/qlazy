init 2

x 0

@ == initial state ==
show

# swap gate
cx 0 1
cx 1 0
cx 0 1

@ == circuit ==
circ

@ == final state ==
show

@ == measurement ==
m
