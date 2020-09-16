import random

""" Class to implement sentence generation using an unweighted Markov Chain """
class Markov_Chain( object ):
	def __init__( self ):
		self.data = {}

	# add data to Markov chain
	def feed( self, sentence ):
		words = sentence.split()

		for i in range( len( words ) ):
			if words[i] not in self.data:
				self.data[words[i]] = set()
			# sentence-termination character
			if i == len( words ) - 1:
				self.data[words[i]].add( 0 )
			else:
				self.data[words[i]].add( words[i + 1] )

	# generate string using given data
	def generate( self, char_limit ):
		last_word = random.choice( list( self.data ) )
		generated_str = last_word
		while len( generated_str ) < char_limit:
			last_word = random.choice( tuple( self.data[last_word] ) )
			# special end-sentence     mmmnnnm,./ character
			if last_word == 0:
				break
			generated_str += " " + last_word

		generated_str = generated_str[:char_limit]
		return generated_str


""" Class to implement sentence generation using ngrams """
class Ngram( object ):
	def __init__( self, N=1 ):
		self.n = N
		self.data = {}

	# add data 
	def feed( self, sentence ):
		words = sentence.split()

		if len( words ) <= self.n:
			pass

		for i in range( len( words ) + 1 - self.n ):
			#print("feed: {}".format(i))
			last_ngram = ' '.join( words[i:i + self.n] )
			if ' '.join( words[i:i + self.n] ) not in self.data:
				self.data[last_ngram] = set()
			if i == len( words ) - self.n:
				self.data[last_ngram].add( 0 )
			else:
				self.data[last_ngram].add( words[i + self.n] )

	def generate( self, char_limit ):
		last_word = random.choice( list( self.data ) ).split()
		generated_str = " ".join( last_word )
		while len( generated_str ) < char_limit:
			last_word.append( random.choice( tuple( self.data[' '.join( last_word )] ) ) )
			last_word.pop( 0 )

			if last_word[-1] == 0:
				break
			generated_str += " " + last_word[-1]

		generated_str = generated_str[:char_limit]
		return generated_str