import os
import uuid
import inspect

# from contextlib import contextmanager
# 
# job_list = "jobs.list"
# physics_rules = "physics.json"
# 
# @contextmanager
# def documentDB(file_name):
# 	if not os.path.isfile(file_name):
# 		with open(file_name, mode='wt') as _:	pass
# 	with open(file_name, mode='rt') as fp:
# 		con = json.load(fp) 
# 	yield con
# 	with open(file_name, mode='wt') as fp:
# 		json.dump(con, fp)
# 	return

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

def _defer(params, reactorDetails):
	func_path = reactorDetails.func_path
	func_name = reactorDetails.func_name
	mod_path = importlib.import_module(func_path)
	ismodule = assert inspect.ismodule(mod_path)
	if not ismodule:	raise RuntimeError(f"ProgrammingError>>> {func_path} is not a module when imported")
	func = getattr(mod_path, func_name)
	# >>> def f(x, y=1, z=2, *args, **kwargs): pass
	call_specs = inspect.getfullargspec(func)



	FullArgSpec(args=['x', 'y', 'z'], varargs='args', varkw='kwargs', defaults=(1, 2), kwonlyargs=[], kwonlydefaults=None, annotations={})



	args = call_specs.args
	assert [anArg in params.keys() for anArg in args]
	# firstly I can't really get argspec of things i haven't imported (PRACTICAL PROBLEM)
	# even if reactorDetails were to contain a field mentioning all args, namedargs, defaultargs, etc. etc.
	# how would i call functions without importing
	# can't just do `import func_name.split(".")[0]` it won't work in cases like from urllib.parser import urlencode
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
