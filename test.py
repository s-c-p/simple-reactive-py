"""
TREE-ish
	import_test/
	│   modA.py
	│       >> func()
	│       >> A(x).func()
	│
	└───deeper/
			modB.py
				>> Alphabet(x)
				>> Alphabet.sm()

>>> import import_test.modA
>>> import_test.modA.func()
'something'
>>> import_test.modA.A(5)
<import_test.modA.A object at 0x0000000001FFAEB8>
>>> import_test.modA.A(5).func()
5
>>> import import_test.deeper.modB
>>> import_test.deeper.modB.Alphabet.sm()
I am always here
'I am always here'
"""

import queue
# import pytest

# queue.define_rules("sender_name",
#     [ queue.PhysicsRule(1, 2, 3, 4)
#     , queue.PhysicsRule('a', 'b', 'c', 'd')
#     ])

def setup():
	queue.define_rules("flow_test",
		[ queue.PhysicsRule("import_test.modA", "f1", None, "ignore")
		, queue.PhysicsRule("import_test.modA", "f2", None, "ignore")
		, queue.PhysicsRule("import_test.modA", "f6", None, "ignore")
		])
	queue.define_rules("flow_test",
		[ queue.PhysicsRule("import_test.deeper.modB", "f4", None, "ignore")
		, queue.PhysicsRule("import_test.deeper.modB", "f5", None, "ignore")
		])
	queue.define_rules("pump_test",
		[ queue.PhysicsRule("import_test.modA", "func_w_defaults_partially_overRidden", None, "ignore")
		, queue.PhysicsRule("import_test.deeper.modB", "func_w_defaults", None, "ignore")
		])	
	return

def flow_test():
	""" no parameters are passed
	test on functions that don't take argument and simply return a value
	"""
	print("when I run, I expect f1, f2 and f6 of modA to say hi")
	print("when I run, I expect f4 and f5 of modB to say hi")
	queue.push({}, "flow_test")
	return

def pump_test():
	""" this time we pass parameters
	test on simple to very complex function
	"""
	all_params = \
	{ "a": 0.11
	, "b": None
	, "c": {"_": 1, "__": 2}
	# , "d": ""
	, "e": [1, 2, 3, 4]
	, "x": "a string"
	, "useless": 1
	# , "useless": lambda x: x >>> TypeError: Object of type 'function' is not JSON serializable OCCOURS when contextmgr tries to serialize joblist to save on disk
	}
	queue.push(all_params, "pump_test")
	return

def main():
	setup()
	flow_test()
	input(" flow_test done, commencing pump_test ".center(79, "-"))
	pump_test()
	return

if __name__ == '__main__':
	main()
