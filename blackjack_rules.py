from common_logging import *
from configuration import Configuration

class BlackjackRules(Configuration):
	def __init__(self, log, rules_section = "Blackjack"):
		# Initialize and read INI file
		Configuration.__init__(self, log, "rules.ini", rules_section)
			
		# Read section
		self.decks = Configuration.read_int(self, "Decks", 4)
		self.minimum_bet = Configuration.read_int(self, "MinimumBet", 1)
		self.maximum_bet = Configuration.read_int(self, "MaximumBet", 100)
		self.blackjack_payout = Configuration.read_double(self, "BlackjackPayout", 1.5)
		self.double_down_on_all = Configuration.read_boolean(self, "DoubleDownOnAll", False)
		self.push_goes_to_dealer = Configuration.read_boolean(self, "PushGoesToDealer", False)
		self.dealer_hits_on_soft_17 = Configuration.read_boolean(self, "DealerHitsOnSoft17", False)
		self.insurance_allowed = Configuration.read_boolean(self, "InsuranceAllowed", False)
		self.surrender_allowed = Configuration.read_boolean(self, "SurrenderAllowed", False)

	def get_decks(self):
		return self.decks

	def get_minimum_bet(self):
		return self.minimum_bet

	def get_maximum_bet(self):
		return self.maximum_bet

	def get_blackjack_payout(self):
		return self.blackjack_payout

	def can_double_down_on_all(self):
		return self.double_down_on_all

	def does_push_goes_to_dealer(self):
		return self.push_goes_to_dealer

	def does_dealer_hits_on_soft_17(self):
		return self.dealer_hits_on_soft_17

	def is_insurance_allowed(self):
		return self.insurance_allowed

	def is_surrender_allowed(self):
		return self.surrender_allowed

		