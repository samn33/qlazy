from qlazypy import QStateTest

def test_tenspro():

    qs1 = QStateTest(1)
    qs2 = QStateTest(2)
    qs3 = qs1.tenspro(qs2)
    
    print(type(qs3))

    qs3.hadamard(id=[0,1,2])

    qs3.show()
    
    qs1.free()
    qs2.free()
    qs3.free()

def test_clone():

    qs = QStateTest(2)
    qs1 = qs.clone()

    print(type(qs1))
    
    qs1.hadamard(id=[0,1])
    qs1.show()

    qs.free()
    qs1.free()

def test_simple():

    qs = QStateTest(2)
    print(type(qs))

    qs.h(0)
    qs.hadamard(id=[0,1])
    print(type(qs))
    
    qs.show()

    qs.free()

    
if __name__ == '__main__':

    test_simple()
    test_clone()
    test_tenspro()
