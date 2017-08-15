import sys

class A:
	"""docstring for A"""
	def __init__(self, x):
		self.x = x
		return

	def func(self):
		"""call this func from .."""
		return self.x

def func():
	return "something"

def f1():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def f2():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def f3():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def f4():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def f5():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def f6():
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	return

def func_w_defaults_partially_overRidden(a, b, c="abcd", d=10, e=5.5):
	print(__name__, end="\t")
	print(f"Hi! This is {sys._getframe().f_code.co_name}, from modA")
	print(f"a is {a} of type {type(a)}")
	print(f"b is {b} of type {type(b)}")
	print(f"c is {c} of type {type(c)}")
	print(f"d is {d} of type {type(d)}")
	print(f"e is {e} of type {type(e)}")
	return
