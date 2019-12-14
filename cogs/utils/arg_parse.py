import shlex

def parse(message):
	return shlex.split(message)[1:]