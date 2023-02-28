class A(object):

    @staticmethod
    def d(fun):
        def _d():
            fun()
        return _d

    @A.d
    def b(self):