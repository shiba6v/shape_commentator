class A():
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        A.__init__(self)

a = A()
b = B()
