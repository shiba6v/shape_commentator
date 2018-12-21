class A():
    pass

class B(A):
    def __init__(self):
        super(B, self).__init__()

a = A()  #_ <class '__main__.A'>,
b = B()  #_ <class '__main__.B'>,

