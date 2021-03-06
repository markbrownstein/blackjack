import csv

from common_logging import *
from blackjack_constants import *
from card_counting import CardCounting
from blackjack_game import BlackjackGame

class BlackjackGameFramework(BlackjackGame):
	STANDARD_STRATEGY_FILENAME = "standard_strategy.csv"

	def __init__(self, log, bankroll, starting_bet, rules_section = "Blackjack"):
		self.log = log
		BlackjackGame.__init__(self, log, bankroll, rules_section)
		self.starting_bet = starting_bet
		self.current_bet = self.starting_bet
		self.bet_multiplier = 1.0
		self.card_counting_strategy = None

	def get_starting_bet(self):
		return self.starting_bet
		
	def set_starting_bet(self, starting_bet):
		self.starting_bet = starting_bet
	
	def get_current_bet(self):
		return self.current_bet
		
	def set_current_bet(self, current_bet):
		self.current_bet = current_bet
	
	def get_bet_multiplier(self):
		return self.bet_multiplier
		
	def set_bet_multiplier(self, bet_multiplier):
		self.bet_multiplier = bet_multiplier
	
	def get_result_text(self, result):
		result_text = ""
		if result == BLACKJACK_RESULT:
			result_text = "Blackjack! Player WINS!"
		elif result == WIN_RESULT:
			result_text = "Player WINS!"
		elif result == PUSH_RESULT:
			result_text = "PUSH!"
		elif result == LOSS_RESULT:
			result_text = "Player LOSES!"
		elif result == SURRENDER_RESULT:
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
		self.card_counting_strategy = CardCounting(self.log, self.get_rules().get_decks(), card_counting_strategy)
		self.set_event_listener(self.card_counting_strategy)
		self.log.finer("... finished loading card counting strategy: " + card_counting_strategy)
		

	def parse_decision(self, key, dealer_up_rank):
		# Index 0 is dealer up card (?, # or #-#), index 1 is count, index 2 is what to do. Ex: 14-16_?_+10_stand
		decision_array = self.get_card_counting_strategy().get_decision(key)
		if decision_array != None:
			self.log.fine("Card counting playing strategy found: " + key + ' ' + str(decision_array))
			if len(decision_array) == 3:
				if decision_array[0] == '?' or dealer_up_rank in self.get_card_counting_strategy().parse_range(decision_array[0]):
					try:
						if self.get_card_counting_strategy().used_count() >= int(decision_array[1]):
							self.log.fine("Card counting playing strategy used: " + key + ' ' + str(decision_array))
							return decision_array[2]
					except:
						pass
		return None

	def advise_hand(self, strategy, choices):
		has_playing_method = self.get_card_counting_strategy() != None and self.get_card_counting_strategy().has_playing_method()
		dealer_up_rank = self.calc_rank(self.get_dealer_hand()[1])
		if self.get_player_hand()[0][0] == self.get_player_hand()[1][0] and SPLIT in choices:
			player_rank = self.calc_rank(self.get_player_hand()[0])
			self.log.finest("Possible auto split: player rank=" + str(player_rank) + ", dealer up rank=" + str(dealer_up_rank))
			if has_playing_method:
				# See if the pair is in the playing strategy
				key = str(player_rank) + ',' + str(player_rank)
				decision = self.parse_decision(key, dealer_up_rank)
				if decision != None:
					return decision
			action = strategy[200 + player_rank][dealer_up_rank - 1]
			if action == ADVISE_SPLIT:
				return SPLIT
		player_total = self.calc_highest_total(self.get_player_hand())
		if player_total < 21:
			if player_total != self.calc_lowest_total(self.get_player_hand()):
				# See if the soft total is in the playing strategy
				key = "soft" + str(player_total)
				decision = self.parse_decision(key, dealer_up_rank)
				if decision != None:
					return decision				
				action = strategy[100 + player_total][dealer_up_rank - 1]
			else:
				# See if the hard total is in the playing strategy
				key = "hard" + str(player_total)
				decision = self.parse_decision(key, dealer_up_rank)
				if decision != None:
					return decision				
				# See if the total is in the playing strategy
				key = str(player_total)
				decision = self.parse_decision(key, dealer_up_rank)
				if decision != None:
					return decision				
				
				# Continue with normal playing strategyu
				if player_total < 9:
					action = ADVISE_HIT
				else:
					action = strategy[player_total][dealer_up_rank - 1]
					self.log.finest("Strategy action=" + str(action))
			if action > ADVISE_STAND:
				if action > ADVISE_HIT and DOUBLE in choices:
					return DOUBLE
				return HIT
			elif action == ADVISE_SURRENDER:
				if SURRENDER in choices:
					return SURRENDER
				return HIT
		return STAND

	def show_hand(self, dealer_hand, show_all_cards = True):
		pass
		
	def decide_insurance(self):
		return NO
		
	def decide_insurance_amount(self):
		return 0
		
	def decide_hand(self, choices):
		return STAND
		
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
			if self.decide_insurance() == YES:
				insurance = self.decide_insurance_amount()
				if insurance > 0:
					self.buy_insurance(insurance)

		# Does the player or dealer have blackjack?
		if self.is_player_hand_over() == False and self.is_blackjack(self.get_dealer_hand()) == False:
			self.show_hand(False)
			self.show_hand(True)
			# Play each hand
			while True:
				# TODO: What if split is blackjack? No need to ask player.
				# Play hand until stand, bust or double
				while True:
					choices = [ STAND, HIT ]
					if self.can_double_down(self.get_player_hand(), self.get_current_bet()) == True:
						choices.append(DOUBLE)
					if self.can_split(self.get_player_hand(), self.get_current_bet()) == True:
						choices.append(SPLIT)
					#else:
					#	choices.append(SPLIT)
					if self.can_surrender():
						choices.append(SURRENDER)
					action = self.decide_hand(choices)
					if action == STAND:
						break
					if action == HIT:
						self.deal_card_to_player()
						if self.is_player_hand_over() == True:
							break
						self.show_hand(False)
						self.show_hand(True)					
					if action == DOUBLE:
						self.deal_card_to_player()
						self.double_bet()
						self.show_hand(False)
						self.show_hand(True)					
						break
					if action == SPLIT:
						self.split_hand()
						if self.is_player_hand_over() == True:
							break
						self.show_hand(False)
						self.show_hand(True)
					if action == SURRENDER:
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