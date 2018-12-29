class A():
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        A.__init__(self)

a = A()  #_ <type 'instance'>,
b = B()  #_ <type 'instance'>,

