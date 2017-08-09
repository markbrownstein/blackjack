from logging import *
from shoe import Shoe

class Deck(Shoe):
	def __init__(self, log):
		Shoe.__init__(self, log, 1)
