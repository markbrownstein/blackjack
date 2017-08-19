import math

from common_logging import *
from test_shoe import TestShoe

from blackjack_auto_game import BlackjackAutoGame

class BlackjackTestGame(BlackjackAutoGame):
	STANDARD_STRATEGY = "standard_strategy"
	
	def __init__(self, log, auto_section = "Test"):
		BlackjackAutoGame.__init__(self, log, auto_section)
		
		self.shoe = TestShoe(log, self.rules.get_decks())

