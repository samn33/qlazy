@ == U1,U2,U3 ==

init 2

h 1
u1(0.1) 1
u2(0.2,0.3) 1
u3(0.3,0.4,0.5) 1

show 1

@ == controlled U1,U2,U3 ==

init 2

x 0
h 1
cu1(0.1) 0 1
cu2(0.2,0.3) 0 1
cu3(0.3,0.4,0.5) 0 1

show 1
