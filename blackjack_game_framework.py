from logging import *
from blackjack_game import BlackjackGame

class BlackjackGameFramework(BlackjackGame):
	STAND = "stand"
	HIT = "hit"
	DOUBLE = "double down"
	SPLIT = "split"
	YES = "yes"
	NO = "no"
	
	def __init__(self, log, bankroll, starting_bet, rules_section = "DEFAULT"):
		self.log = log
		BlackjackGame.__init__(self, log, bankroll, rules_section)
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
	
	def get_result_text(self, result):
		result_text = ""
		if result == self.BLACKJACK_RESULT:
			result_text = "Blackjack! Player WINS!"
		elif result == self.WIN_RESULT:
			result_text = "Player WINS!"
		elif result == self.PUSH_RESULT:
			result_text = "PUSH!"
		elif result == self.LOSS_RESULT:
			result_text = "Player LOSES!"
		elif result == self.SURRENDER_RESULT:
			result_text = "Player SURRENDERS!"
			
		return result_text

	def show_hand(self, dealer_hand, show_all_cards = True):
		pass
		
	def decide_insurance(self):
		return self.NO
		
	def decide_insurance_amount(self):
		return 0
		
	def decide_hand(self, choices):
		return self.STAND
		
	def start_hand(self):
		pass
		
	def end_hand(self, result):
		pass
		
	def play_hand(self):
		self.start_hand()
		self.deal_hand(self.get_current_bet())

		# Insurance
		if self.can_buy_insurance():
			self.show_hand(False)
			self.show_hand(True)
			if self.decide_insurance() == self.YES:
				insurance = self.decide_insurance_amount()
				if insurance > 0:
					self.buy_insurance(insurance)

		# Does the player or dealer have blackjack?
		if self.is_player_hand_over() == False and self.is_blackjack(self.get_dealer_hand()) == False:
			self.show_hand(False)
			self.show_hand(True)
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
					if self.can_surrender():
						choices.append(self.SURRENDER)
					action = self.decide_hand(choices)
					if action == self.STAND:
						break
					if action == self.HIT:
						self.deal_card_to_player()
						if self.is_player_hand_over() == True:
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
						if self.is_player_hand_over() == True:
							break
						self.show_hand(False)
						self.show_hand(True)
					if action == self.SURRENDER:
						self.surrender_hand()
						break
				# Mark current hand as done and go to next hand unless all are done
				if self.next_hand() == True:
					self.show_hand(False)
					self.show_hand(True)
				else:
					break				
		# See if dealer needs cards
		while True:
			if self.is_dealer_hand_over():
				break
			self.deal_card_to_dealer()
		
		# Reveal dealer's hand
		self.show_hand(False, True)
		self.show_hand(True, True)

		# Finish and end hand(s)
		result = self.finish_hand()
		self.end_hand(result)
		
	def run(self):
		pass