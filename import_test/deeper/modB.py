import sys

class Alphabet:
    def __init__(self, x):
        self.x = x
        return

    @staticmethod
    def sm():
        x = "I am always here"
        print(x)
        return x


def f1():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def f2():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def f3():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def f4():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def f5():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def f6():
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    return

def func_w_defaults(x, y=10, z=20):
    print(__name__, end="\t")
    print(f"Hi! This is {sys._getframe().f_code.co_name}, from modB")
    print(f"x is {x} of type {type(x)}")
    print(f"y is {y} of type {type(y)}")
    print(f"z is {z} of type {type(z)}")
    return
