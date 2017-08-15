import random

from common_logging import *
from shoe import Shoe

class TestShoe(Shoe):
	def __init__(self, log, decks):
		Shoe.__init__(self, log, decks)
		
	def shuffle(self):
		self.random_deck = [ 'A1', '91', 'A1', 'A1', 'T1', '41', 'T1', 'J1', 'T2', '92', 'T2', 'K2', '43', 'Q3', '43', 'Q3', 'K3', '44', 'T4', '44', '64', 'K4', '74', 'K4', 'K4', '95', '55', '75', 'A5', '55' ]
		self.red_card = 0
		
