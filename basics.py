@watcher	# use this decorator to single instantiate and include in list of steram
def func(a, b, c):
	return


reactors, alias

queue.push(message)
	new message arrived, put its signal {sender: message_id} in stream
		stream ... I don't know how to implement it but I'll be passing
	assigns a message_id
	now the functions which care about message m from sender s
	do their thing and acknowledge queue about success or failure
		# failure is logged unless explicitly programmed to halt (using know_that)
		# all successes are checked against know_that's own list of reactors
		# any unexpected success raises programmingErr
	# ans.stimulus()
queue.pop(message_id)
	# when all subscribers have reported success
queue.know_that(sender, [func_list])
	# has the responsibility of calling pop()
	# # ans.subscribe(speaker)	# does this go into setup.py
	# # ans.set(reaction, stimulant)	# one stimulant can have many reactions

async await

http://reactivex.io/
http://bit.ly/2vn83wa



class Reactions():
	@staticmethod
	def of_git(on, data):
		stimulus = on
		filePath = data["file-path"]
		if stimulus is "new-file":
		elif stimulus is "file-changed":
		else:
			raise ValueError('Unknown stimulus "{}" for "{}"'.format(stimulus, filePath))
		return "success"

	@staticmethod
	def of_ux(on, data):
		return


