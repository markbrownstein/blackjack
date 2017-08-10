from logging import *
from blackjack_game_framework import BlackjackGameFramework

class BlackjackAutoGame(BlackjackGameFramework):
	def __init__(self, log):
		# Initialize log
		self.log = log
		
		# Initialize framework
		BlackjackGameFramework.__init__(self, log, 500, 5)

	def run(self):
		self.log.warning("Starting auto game run")