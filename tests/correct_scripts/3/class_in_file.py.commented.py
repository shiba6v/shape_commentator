class A():
    pass

class B(A):
    def __init__(self):
        super(B, self).__init__()

a = A()  #_ A
b = B()  #_ B

