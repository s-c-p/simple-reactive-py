import os
import uuid
import json
import inspect
import contextlib

?job_list = "jobs.list"
?physics_rules = "physics.json"

@contextlib.contextmanager
def documentDB(file_name):
	if not os.path.isfile(file_name):
		with open(file_name, mode='wt') as _:	pass
	with open(file_name, mode='rt') as fp:
		con = json.load(fp) 
	yield con
	with open(file_name, mode='wt') as fp:
		json.dump(con, fp)
	return

class ConfigError(Error):
	""" shows error in configuration file """
	def __init__(self, msg):
		self.msg = msg
		return
	def __str__(self):
		print(self.msg)

class PhysicsRule():
	"""docstring for PhysicsRule"""
	def __init__(self, func_path, func_name, expectedAns, onerror):
		self.func_path = func_path
		self.func_name = func_name
		self.expectedAns = expectedAns
		self.onerror = onerror
		return
	@staticmethod
	def _make(argTuple):
		a, b, c, d = argTuple
		return PhysicsRule(a, b, c, d)

# sample
job_list = list()
physics_rules = {
	"sender_name_1": [
		("func_path_1", "func_name_1", "expected value on success", "log OR raise", "async?"),
		("func_path_2", "func_name_2", "expected value on success", "log OR raise", "async?"),
		("func_path_3", "func_name_3", "expected value on success", "log OR raise", "async?")
	],
	"sender_name_2": [
		("func_path_1", "func_name_1", "expected value on success", "log OR raise", "async?"),
		("func_path_2", "func_name_2", "expected value on success", "log OR raise", "async?")
	]
}

def _defer(all_params, reactorDetails):
	# PART-1: create a copy (instantiate) of the function
	func_path = reactorDetails.func_path
	func_name = reactorDetails.func_name
	mod_path = importlib.import_module(func_path)
	ismodule = assert inspect.ismodule(mod_path)
	if not ismodule:
		raise ConfigError(f"{func_path} is not a module when imported")
	func = getattr(mod_path, func_name)

	# STEP-2: get argument-related details of the function
	call_specs = inspect.getfullargspec(func)
	# TRY: >>> def f(x, y=1, z=2, *args, **kwargs): pass
	# FullArgSpec(args=['x', 'y', 'z'], varargs='args', varkw='kwargs', 
	#   defaults=(1, 2), kwonlyargs=[], kwonlydefaults=None, annotations={})
	# NOTE: I really don't know how to use kwonlyargs & kwonlydefaults IF i
	#   can get a good use case I will implement it
	# dev-stage-1 >> currently only working with args and defaults
	# TODO: dev-stage-2 >> support for varargs added (for functions like
	#   math('product', *args))

	# STEP-3: filter out necessary details from all_params to get func_params
	req_args = call_specs.args
	# NOTE: req_args is in the calling order that func naturally expects
	if call_specs.defaults:
		# it might be the case that the user didn't supply k-v pairs for
		#   defaults
		lastN = len(call_specs.defaults)
		names = call_specs.args[-1*lastN:]	# get last n elements of list
		temp = dict(zip(names, call_specs.defaults))
		# temp is like {"default arg name": "default arg value"}
	func_params = dict()
	for anArg in req_args:
		try:
			value = all_params[anArg]
		except KeyError:
			try:
				value = temp[anArg]
			except KeyError:
				raise RuntimeError(f"Required argument {anArg} for \
				{func.__name__} not provided in 'all_params' i.e.\n\
				{all_params}")
		func_params[anArg] = value

	# STEP-4: and now, finally, we call the function
	the_args = ", ".join([f"func_params['{anArg}']" for anArg in req_args])
	# NOTE: it's not smart to ". ".join(corresponding values) because then we
	#   will have to take care about stringifying int and class names properly
	#   SO we insert values at eval-runtime only by doing dict_name[key] as done
	#   above
	try:
		runtimeAns = eval("{}({})".format("func", the_args))
	except Exception as e:
		if reactorDetails.onerror:	pass
		else:						raise e
 	if runtimeAns == reactorDetails.expectedAns:
		# inform pop
	else:
		errMsg = f"{func.__name__} didn't return expected value"
		if reactorDetails.onerror:	print(errMsg)
		else:						raise RuntimeError(errMsg)
	return

def defer(params, reactors):
	"""	async await
	https://hackernoon.com/asynchronous-python-45df84b82434
	https://gist.github.com/nhumrich/b53cc1e0482411e4b53d74bd12a485c1#file-gevent_example-py
	https://medium.freecodecamp.org/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6
	https://github.com/ask/flask-celery/
	"""
	for aReactor in reactors:
		_defer(message, aReactor)
	return

def push(message, sender):
	"""
	x -- implicitly knows about sender (because it violates the defn of pure functional...)
	assigns a message_id
	raises some alert, so everyone becomes concious
	now the functions which care about message m from sender s
	do their thing and acknowledge queue about success or failure
	  failure is logged unless explicitly programmed to halt (using know_that)
	  all successes are checked against know_that's own list of reactors
	  any unexpected success raises programmingErr
	# ans.stimulus()
	"""
	message_id = str(uuid.uuid4())
	jobs.append({message_id: message})
	wake_everyone()	# HAHA
	reactor_list = physics_rules[sender]
	defer(message, reactor_list)
	return

def pop(message_id):
	""" when all subscribers have reported success """
	return

def _know_that(sender, reactor_list):
	"""	has the responsibility of calling pop()
	ans.subscribe(speaker)  # does this go into setup.py
	ans.set(reaction, stimulant)    # one stimulant can have many reactions
	"""
	return
