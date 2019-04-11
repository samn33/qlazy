from qlazypy.basic import QState

# initialize
qs = QState(1)

print("== initial state ==")
qs.show()

md = qs.mx()
md.show()

md = qs.mx()
md.show()

md = qs.mz()
md.show()

print("== state ==")
qs.show()

md.free()
qs.free()
