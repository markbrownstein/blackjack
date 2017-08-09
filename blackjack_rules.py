#from configparser import ConfigParser
from logging import *
from configuration import Configuration

class BlackjackRules(Configuration):
	def __init__(self, log, rules = "DEFAULT"):
		# Initialize and read INI file
		Configuration.__init__(self, log, "rules.ini", rules)
			
		# Read section
		self.minimum_bet = Configuration.readInt(self, "MinimumBet", 1)
		self.maximum_bet = Configuration.readInt(self, "MaximumBet", 100)
		self.blackjack_payout = Configuration.readDouble(self, "BlackjackPayout", 1.5)
		self.push_goes_to_dealer = Configuration.readBoolean(self, "PushGoesToDealer", False)
		self.dealer_hits_on_soft_17 = Configuration.readBoolean(self, "DealerHitsOnSoft17", False)

	def get_minimum_bet(self):
		return self.minimum_bet

	def get_maximum_bet(self):
		return self.maximum_bet

	def get_blackjack_payout(self):
		return self.blackjack_payout

	def does_push_goes_to_dealer(self):
		return self.push_goes_to_dealer

	def does_dealer_hits_on_soft_17(self):
		return self.dealer_hits_on_soft_17

		