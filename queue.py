import os
import uuid
import json
import inspect
import importlib
import itertools
from contextlib import contextmanager
from typing import  Tuple, Optional, List, NewType, Generator


JOB_LIST = "jobs.list"
PHYSICS_RULES = "physics.json"



# PathLike = NewType('PathLike', str)
# creating a lot of beyond-my-understanding problems with mypy

class ConfigError(Exception):
	""" shows error in configuration file """
	def __init__(self, msg: str) -> None:
		self.msg = msg
		return

class PhysicsRule():
	""" struct for storing a rule i.e. details of a reactor
	TODO: in future add support for marking this reactor info as async
	capable (?bool flag)
	"""
	def __init__(self, func_path: str, func_name: str, expectedAns: object,
			onerror: str) -> None:
		self.func_path = func_path
		self.func_name = func_name
		self.expectedAns = expectedAns
		self.onerror = onerror

	@staticmethod
	def _make(argTuple: Tuple[str, str, object, str]) -> 'PhysicsRule':
		a, b, c, d = argTuple
		return PhysicsRule(a, b, c, d)

class RuleEncoder(json.JSONEncoder):
	""" add-on to the standard json library to help properly encode (i.e. \
	dump py obj to file) a physics rule
	"""
	def default(self, theRule: PhysicsRule) -> dict:
		if isinstance(theRule, PhysicsRule):
			return \
			{ "func_path": theRule.func_path
			, "func_name": theRule.func_name
			, "onerror": theRule.onerror
			, "expectedAns": theRule.expectedAns }
		# return json.JSONEncoder.default(self, theRule)
		return super(RuleEncoder, self).default(theRule)

class RuleDecoder(json.JSONDecoder):
	""" add-on to the standard json library to help properly decode (i.e. \
	make python object from dict (which is in turn (internally) derived \
	from json.load)) a physics rule
	SEE: 'Lambda' para on bit.ly/2vCwlSQ
	"""
	def __init__(self):
		# json.JSONDecoder.__init__(self, object_hook=self.dict2obj)
		super(RuleDecoder, self).__init__(object_hook=self.dict2obj)

	def dict2obj(self, dicn: dict) -> PhysicsRule:
		keys = dicn.keys()
		if len(keys) == len(self.NECESSARY_TRAITS) and \
			all(  [trait in keys for trait in self.NECESSARY_TRAITS]  ):
			# NOTE: the following (seemingly shortcut)
			# won't work because dicn keys' positions are not fixed
			# return PhysicsRule._make(tuple(dicn.values())) 
			w = dicn["func_path"]
			x = dicn["func_name"]
			y = dicn["expectedAns"]
			z = dicn["onerror"]
			tup = w, x, y, z
			return PhysicsRule._make(tup)
		else:
			# the case when file is just created and dicn is  == {}
			return dicn
			# raise ConfigError("")

	NECESSARY_TRAITS = ["func_path", "func_name", "expectedAns", "onerror"]



@contextmanager
def documentDB(file_name: str) -> Generator:
	if not os.path.isfile(file_name):
		# with open(file_name, mode='wt') as _: pass
		raise ConfigError(f"configuration file '{file_name}' not found")
	with open(file_name, mode='rt') as fp:
		con = json.load(fp, cls=RuleDecoder)
	yield con
	with open(file_name, mode='wt') as fp:
		json.dump(con, fp, cls=RuleEncoder)
	return "success"

def _defer(all_params: dict, func: object, onerror: str, expectedAns) -> str:
	# STEP-1: get argument-related details of the function
	call_specs = inspect.getfullargspec(func)
	# TRY: >>> def f(x, y=1, z=2, *args, **kwargs): pass
	# FullArgSpec(args=['x', 'y', 'z'], varargs='args', varkw='kwargs',
	#   defaults=(1, 2), kwonlyargs=[], kwonlydefaults=None, annotations={})
	# NOTE: I really don't know how to use kwonlyargs & kwonlydefaults IF i
	#   can get a good use case I will implement it
	# dev-stage-1 >> currently only working with args and defaults
	# TODO: dev-stage-2 >> support for varargs added (for functions like
	#   math('product', *args))

	# STEP-2: filter out necessary details from all_params to get func_params
	# why filter? cuz we gonna need it in the eval-thingy, its string black
	# magic
	req_args = call_specs.args
	# NOTE: req_args is in the calling order that func naturally expects
	if call_specs.defaults:
		# it might be the case that the user didn't supply k-v pairs for
		#   defaults
		lastN = len(call_specs.defaults)
		names = call_specs.args[-1*lastN:]  # get last n elements of list
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

	# STEP-3: and now, finally, we call the function
	the_args = ", ".join([f"func_params['{anArg}']" for anArg in req_args])
	# NOTE: it's not smart to ". ".join(corresponding values) because then we
	#   will have to take care about stringifying int and class names properly
	#   SO we insert values at eval-runtime only by doing dict_name[key] as 
	#   done above. Also, the `'` before and after {anArg} are crucial for
	#   eval to work as expected
	try:
		runtimeAns = eval("{}({})".format("func", the_args))
	except Exception as e:
		if onerror == "ignore": pass
		else:          			raise e
	if runtimeAns == expectedAns:
		# inform pop
		pass
	else:
		errMsg = f"{func.__name__} didn't return expected value"
		if onerror == "ignore": print(errMsg)
		else:          			raise RuntimeError(errMsg)
	return "success"

def detectNameCollision(reactors: List[PhysicsRule]) -> None:
	""" designed to be ruthless on functions, the primary purpose of this
	function is to make sure no 2 functions have the same argument name,
	because such a case would create ambiguity, as in, that commonArg is
	targeted to which func exactly
	As a part of its operations, it naturally needs to revive the functions
	and SO if all goes well (i.e. no collisions detected) then instead of
	having another function rebuild live versions of these functions we
	return them at the end; remember return happens IFF no NameCollisions were
	found
	"""
	def _revive_func(reactorDetails: PhysicsRule):
		""" convert reactorDetails to a live function and return the live 
		function (since functions are first class citizens in python and can
		be passed around like objects) along with details 'onerror' &
		'expectedAns'
		"""
		func_path = reactorDetails.func_path
		func_name = reactorDetails.func_name
		mod_path = importlib.import_module(func_path)
		if not inspect.ismodule(mod_path):
			raise ConfigError(f"{func_path} is not a module when imported")
		func = getattr(mod_path, func_name)
		onerror = reactorDetails.onerror
		expectedAns = reactorDetails.expectedAns
		return func, onerror, expectedAns
	# ------------------------------------------------------------------------
	# NOTE: name collision are detected at runtime not at compile time (i.e.
	# when # making physics.json) because it is possible for two functions to
	# have (partially)-identical argument names, in real life the 2 might not
	# be called at the same time (i.e. be in the same reactor_list for an
	# arbitary stimulant), and if they do get called THEN AND ONLY THEN the
	# programmer sees an error otherwise no need to make his/her life extra
	# difficult by forcing 'em to come up with unique var names THROUGHOUT
	# the project 
	# ------------------------------------------------------------------------
	# why not just provide pre-packed info to queue.push, like
	# {"funcName": **kwds, "funcName2": **kwds} it defeats the design
	# philosopy that stimulant (one who calls queue.push, aka the popular
	# girl/guy that everyone listens to) shouldn't have to worry about knowing
	# its followers, it just provides all info it can (like giving it all in
	# a block buster performance), fans (reactors) pick what details they want
	# form `all_params`
	live_funcs = list()
	all_all_args = list()
	for aReactor in reactors:
		func, onerror, expectedAns = _revive_func(aReactor)
		live_funcs.append({
			"func": func,
			"onerror": onerror,
			"expectedAns": expectedAns
		})
		req_args = inspect.getfullargspec(func).args		# NOTE: bang!!!
		all_all_args.append(req_args)
		# NOTE: although live_funcs and all_all_args are 2 seperate lists but
		# because they are built parallely, any (legal) index `i` of live_funcs
		# has its corresponding req_args at all_all_args[i] only, this fact
		# is used below for deriving names of functions when a name collision
		# occours
	for a_combo in itertools.combinations(all_all_args, 2):
		list1, list2 = a_combo
		set1, set2 = set(list1), set(list2)
		ans = set1.intersection(set2)
		if ans:
			# i.e. set is not empty
			commonArg = ans.pop()
			# derive the the function names to give an informative error
			# message
			i1 = all_all_args.index(list1)
			i2 = all_all_args.index(list2)
			func_1_name = live_funcs[i1]["func"].__name__
			func_2_name = live_funcs[i2]["func"].__name__
			raise RuntimeError(f"NameCollision detected: 2 functions `{func_1_name}` and `{func_2_name}` have `{commonArg}` as a common argument name, this creates ambiguity (`{commonArg}` is target to whom exactly) at runtime. Please refactor the code to remove such ambiguity")
	return live_funcs

def defer(all_params: dict, reactors: List[PhysicsRule]) -> str:
	""" async await
	https://hackernoon.com/asynchronous-python-45df84b82434
	https://gist.github.com/nhumrich/b53cc1e0482411e4b53d74bd12a485c1#file-gevent_example-py
	https://medium.freecodecamp.org/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6
	https://github.com/ask/flask-celery/
	"""
	live_funcs = detectNameCollision(reactors)
	for a_live_func in live_funcs:
		_defer(
			all_params,
			a_live_func["func"],
			a_live_func["onerror"],
			a_live_func["expectedAns"]
		)
	return "success"

def push(message: dict, sender: str) -> str:
	"""
	assigns a message_id
	raises some alert, so everyone becomes concious
	now the functions which care about message m from sender s
	do their thing and acknowledge queue about success or failure
	  failure is logged unless explicitly programmed to halt (using know_that)
	  all successes are checked against know_that's own list of reactors
	  any unexpected success raises programmingErr
	# ANS.stimulus()
	NOTE: take a look at bit.ly/2vBgw0F to understand why 2 lines end with ';'
	"""
	message_id = str(uuid.uuid4())
	jobs: List[dict];
	with documentDB(JOB_LIST) as jobs:
		jobs.append({message_id: message})
	# wake_everyone() # HAHA
	physics_rules: dict;
	with documentDB(PHYSICS_RULES) as physics_rules:
		reactor_list = physics_rules[sender]
	defer(message, reactor_list)
	return "success"

def define_rules(sender: str, reactor_list: List[PhysicsRule]) -> str:
	""" binds reactions to a sender and stores that data in a json file
	ideal scenario-- QUEUE.subscribe(speaker)  # called by anyone anywhere
	current scenario-- ANS.set(reaction, stimulant)	# done only at setup time
	NOTE: one stimulant can have many reactions
	"""
	def cautious_writer(dicn, key, list_item):
		""" exploits the benefits of call-by-sharing """
		try:
			_ = dicn[key]
		except KeyError:
			dicn[key] = list()
		finally:
			dicn[key].append(list_item)
		return
	physics_rules: dict;
	with documentDB(PHYSICS_RULES) as physics_rules:
		for reactorDetails in reactor_list:
			cautious_writer(physics_rules, sender, reactorDetails)
		# just_add_water = functools.partial(cautious_writer, physics_rules,\
		# sender)
		# list(  map(just_add_water, reactor_list)  )
	return "success"

def jobs_tracker():
	""" has the responsibility of calling pop()
	necessitates class-like design
	to imple,emtn in future when async is possible
	"""
	return NotImplemented

def pop(message_id: str):
	""" when all subscribers have reported success """
	return NotImplemented
