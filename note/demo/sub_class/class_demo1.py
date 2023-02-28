class A():

    def __init__(self):
        print("class A")

class C():
    def __init__(self):
        print("class C")

class B(A, C):

    pass


if __name__ == '__main__':
    b = B()
    print(isinstance(b, A))
    print(isinstance(b, C))