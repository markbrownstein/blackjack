import csv

from logging import *
from card_counting import CardCounting
from blackjack_game import BlackjackGame

class BlackjackGameFramework(BlackjackGame):
	STANDARD_STRATEGY_FILENAME = "standard_strategy.csv"

	STAND = "stand"
	HIT = "hit"
	DOUBLE = "double down"
	SPLIT = "split"

	YES = "yes"
	NO = "no"
	
	ADVISE_DOUBLE = 2
	ADVISE_HIT = 1
	ADVISE_STAND = 0
	ADVISE_SURRENDER = -1
	ADVISE_SPLIT = 1
	
	def __init__(self, log, bankroll, starting_bet, rules_section = "Blackjack"):
		self.log = log
		BlackjackGame.__init__(self, log, bankroll, rules_section)
		self.starting_bet = starting_bet
		self.current_bet = self.starting_bet
		self.card_counting_strategy = None

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

	def get_card_counting_strategy(self):
		return self.card_counting_strategy

	def load_strategy(self, filename):
		strategy = {}
		with open(filename, newline='') as file:
			reader = csv.reader(file, delimiter='\t')
			for row in reader:
				if row[0].isdigit() and len(row) == 11:
					key = int(row[0])
					value = []
					for i in range(10):
						try:
							value.append(int(row[i + 1]))
						except ValueError:
							value.append(0)
					strategy[key] = value
		return strategy

	def load_card_counting_strategy(self, card_counting_strategy):
		self.log.finer("Loading card counting strategy: " + card_counting_strategy + " ...")
		self.card_counting_strategy = CardCounting(self.log, card_counting_strategy)
		self.set_event_listener(self.card_counting_strategy)
		self.log.finer("... finished loading card counting strategy: " + card_counting_strategy)
		
	def advise_hand(self, strategy, choices):
		dealer_up_rank = self.calc_rank(self.get_dealer_hand()[1])
		if self.get_player_hand()[0][0] == self.get_player_hand()[1][0] and self.SPLIT in choices:
			player_rank = self.calc_rank(self.get_player_hand()[0])
			self.log.finest("Possible auto split: player rank=" + str(player_rank) + ", dealer up rank=" + str(dealer_up_rank))
			action = strategy[200 + player_rank][dealer_up_rank - 1]
			if action == self.ADVISE_SPLIT:
				return self.SPLIT
		player_total = self.calc_highest_total(self.get_player_hand())
		if player_total < 21:
			if player_total != self.calc_lowest_total(self.get_player_hand()):
				action = strategy[100 + player_total][dealer_up_rank - 1]
			else:
				if player_total < 9:
					action = self.ADVISE_HIT
				else:
					action = strategy[player_total][dealer_up_rank - 1]
					self.log.finest("Strategy action=" + str(action))
			if action > self.ADVISE_STAND:
				if action > self.ADVISE_HIT and self.DOUBLE in choices:
					return self.DOUBLE
				return self.HIT
			elif action == self.ADVISE_SURRENDER:
				if self.SURRENDER in choices:
					return self.SURRENDER
				return self.HIT
		return self.STAND

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
		# Make sure dealer card is flagged as visible
		self.make_dealer_hole_card_visible()
		
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