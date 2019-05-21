init 1
@ == north pole ==
bloch
show

@ == X-dir (plus) ==
h 0
bloch
show

@ == Rotation_Z (+0.25) ==
rz(0.25) 0
bloch
show

@ == Rotation_Z (+0.5) ==
rz(0.5) 0
bloch
show

@ == Rotation_Z (+0.5) ==
rz(0.5) 0
bloch
show

@ == Rotation_Z (0.25) ==
rz(0.25) 0
bloch 0
show 0
