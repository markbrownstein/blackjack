from logging import *
from blackjack_game import BlackjackGame

class BlackjackGameFramework(BlackjackGame):
	def __init__(self, log, bankroll, starting_bet):
		self.log = log
		BlackjackGame.__init__(self, log, bankroll)
		self.starting_bet = starting_bet

	def get_starting_bet(self):
		return self.starting_bet
		
	def set_starting_bet(self, starting_bet):
		self.starting_bet = starting_bet
	
	def start_hand(self):
		bet = self.get_starting_bet()
		self.log.warning("Bet: " + str(bet))
		
	def run(self):
		pass