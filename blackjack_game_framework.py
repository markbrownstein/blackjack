from logging import *
from blackjack_game import BlackjackGame

class BlackjackGameFramework(BlackjackGame):
	STAND = "stand"
	HIT = "hit"
	DOUBLE = "double down"
	SPLIT = "split"
	
	def __init__(self, log, bankroll, starting_bet):
		self.log = log
		BlackjackGame.__init__(self, log, bankroll)
		self.starting_bet = starting_bet
		self.current_bet = self.starting_bet

	def get_starting_bet(self):
		return self.starting_bet
		
	def set_starting_bet(self, starting_bet):
		self.starting_bet = starting_bet
	
	def get_current_bet(self):
		return self.current_bet
		
	def set_current_bet(self, current_bet):
		self.current_bet = current_bet
	
	def show_hand(self, dealer_hand, show_all_cards = True):
		pass
		
	def decide_hand(self, choices):
		return self.STAND
		
	def start_hand(self):
		pass
		
	def end_hand(self, result):
		pass
		
	def play_hand(self):
		self.start_hand()
		self.deal_hand(self.get_current_bet())
		self.show_hand(False)
		self.show_hand(True)
		# TODO: Insurance goes here
		if self.is_hand_over() == False:
			# TODO: Surrender goes here
			# Play each hand
			while True:
				# Play hand until stand, bust or double
				while True:
					choices = [ self.STAND, self.HIT ]
					if self.can_double_down(self.get_player_hand(), self.get_current_bet()) == True:
						choices.append(self.DOUBLE)
					if self.can_split(self.get_player_hand(), self.get_current_bet()) == True:
						choices.append(self.SPLIT)
					#else:
					#	choices.append(self.SPLIT)
					action = self.decide_hand(choices)
					if action == self.STAND:
						break
					if action == self.HIT:
						self.deal_card_to_player()
						if self.is_hand_over() == True:
							break
						self.show_hand(False)
						self.show_hand(True)					
					if action == self.DOUBLE:
						self.deal_card_to_player()
						self.double_bet()
						self.show_hand(False)
						self.show_hand(True)					
						break
					if action == self.SPLIT:
						self.split_hand()
						if self.is_hand_over() == True:
							break
						self.show_hand(False)
						self.show_hand(True)
				# Mark current hand as done and go to next hand unless all are done
				if self.next_hand() == True:
					self.show_hand(False)
					self.show_hand(True)
				else:
					break				
		while True:
			self.show_hand(False, True)
			self.show_hand(True, True)					
			if self.is_hand_over(True):
				break
			self.deal_card_to_dealer()
		result = self.finish_hand()
		self.end_hand(result)
		
	def run(self):
		pass