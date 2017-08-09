queue.push(message)
	# implicitly knows about sender
	# assigns a message_id
	# raises some alert, so everyone becomes concious
	# # ans.stimulus()
queue.pop(message_id)
	# when all subscribers have reported success
queue.know_that(sender, [func_list])
	# has the responsibility of calling pop()
	# # ans.subscribe(speaker)	# does this go into setup.py
	# # ans.set(reaction, stimulant)	# one stimulant can have many reactions





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


