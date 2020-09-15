import random

class Markov_Chain(object):
	""" Class to implement sentence generation using an unweighted Markov Chain """
	def __init__( self ):
		self.data = {}

	# add data to Markov chain
	def feed( self, sentence ):
		words = sentence.split()

		for i in range( 0, len( words ) ):
			if words[i] not in self.data:
					self.data[words[i]] = set()
			# sentence-termination character
			if i == len( words ) - 1:
				self.data[words[i]].add(0)
			else:
				self.data[words[i]].add( words[i + 1] )

	# generate string using given data
	def generate( self, char_limit ):
		last_word = random.choice( list( self.data ) )
		generated_str = last_word
		while len( generated_str ) < char_limit:
			last_word = random.choice( tuple( self.data[last_word] ) )
			# special end-tweet character
			if last_word == 0:
				break
			generated_str += " " + last_word

		generated_str = generated_str[:280]
		return generated_str