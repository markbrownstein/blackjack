import math

from common_logging import *
from blackjack_constants import *
from configuration import Configuration
from card_counting import CardCounting

from blackjack_game_framework import BlackjackGameFramework

class BlackjackAutoGame(BlackjackGameFramework):
	STANDARD_STRATEGY = "standard_strategy"
	
	INSURANCE_DECISION = "insurance"
	
	def __init__(self, log, auto_section = "Blackjack"):
		# Initialize log
		self.log = log
		
		# Initialize and read INI file
		configuration = Configuration(log, "auto.ini", auto_section)
		self.number_of_games = configuration.read_int("NumberOfGames", 1000)
		self.number_of_hands = configuration.read_int("NumberOfHands", 100)
		self.starting_bankroll = configuration.read_int("StartingBankroll", 500)
		self.starting_bet = configuration.read_int("StartingBet", 1)
		self.rules_name = configuration.read_string("BlackJackRules", "Blackjack")
		self.strategy_file = configuration.read_string("StrategyFile", self.STANDARD_STRATEGY_FILENAME)
		self.card_counting_strategy_name = configuration.read_string("CardCountingStrategy", "Blackjack")
		
		# Stats
		self.ending_bankrolls = []
		self.max_ending_bankroll = -1
		self.min_ending_bankroll = -1
		
		# Initialize variables
		self.hand_number = 0

		# Load strategies
		self.strategy = self.load_strategy(self.strategy_file)

		# Initialize framework
		BlackjackGameFramework.__init__(self, log, self.starting_bankroll, self.starting_bet, self.rules_name)
		
		# Load counting strategy
		self.load_card_counting_strategy(self.card_counting_strategy_name)

	def show_hand(self, dealer_hand, show_all_cards = False):
		if dealer_hand == False:
			player_total = self.calc_highest_total(self.get_player_hand())
			soft_player_total = self.calc_lowest_total(self.get_player_hand())
			if player_total == soft_player_total:
				player_total_string = str(player_total)
			else:
				player_total_string = str(soft_player_total) + " or " + str(player_total)
			if show_all_cards == True:
				self.log.finer("      Dealer total: " + str(self.calc_highest_total(self.get_dealer_hand())) + ", Player total: " + player_total_string)
			else:
				self.log.finer("      Dealer up card: " + str(self.calc_rank(self.get_dealer_hand()[1])) + ", Player total: " + player_total_string)
	
	def decide_insurance(self):
		if self.get_card_counting_strategy() != None and self.get_card_counting_strategy().has_playing_method():
			decision = self.get_card_counting_strategy().get_decision(self.INSURANCE_DECISION)
			if decision != None:
				self.log.finest("Insurance decision: " + str(decision))
				if self.get_card_counting_strategy() != None and self.get_card_counting_strategy().has_counting_method():
					count = self.get_card_counting_strategy().get_used_count()
					try:
						threshold = float(decision[0])
						if count >= threshold and (decision[1].lower() == "yes" or decision[1].lower() == "true"):
							return YES
					except:
						self.log.warning("Bad decision threshold: " + decision[0])
		return NO

	def decide_insurance_amount(self):
		max = self.get_current_bet() / 2
		if max > self.get_bankroll() - self.get_current_bet():
			max = self.get_bankroll() - self.get_current_bet()
		if max <= 0:
			return 0.0
		self.log.fine("Insurance purchased: $" + str(max))
		return max
		
	def decide_hand(self, choices):
		return self.advise_hand(self.strategy, choices)

	def start_hand(self):
		current_bet = self.get_starting_bet()
		if self.get_card_counting_strategy() != None and self.get_card_counting_strategy().has_counting_method():
			count = self.get_card_counting_strategy().get_used_count()
			count_stats = "   Count: " + str(count)
			if count >= self.get_card_counting_strategy().get_count_threshold():
				# If this is a multiplier,
				if self.get_card_counting_strategy().get_betting_type() == MULTIPLIER:
					# Calc the multiplier by dividing the count by the threshold and multiplying by the step
					multiplier = self.get_card_counting_strategy().get_betting_step() * math.floor(count / self.get_card_counting_strategy().get_count_threshold())
					if multiplier > self.get_card_counting_strategy().get_betting_high():
						multiplier = self.get_card_counting_strategy().get_betting_high()
					# Apply the multiplier
					current_bet = self.get_starting_bet() * multiplier
					count_stats = count_stats + ", Multiplier: " + str(multiplier)
				# If this is a incremental,
				elif self.get_card_counting_strategy().get_betting_type() == INCREMENT:
					# Calc the increment by subtracting the count by the threshold plus one and multiplying by the step
					increment = self.get_card_counting_strategy().get_betting_step() * math.floor(count - self.get_card_counting_strategy().get_count_threshold() + 1.0)
					if increment > self.get_card_counting_strategy().get_betting_high():
						increment = self.get_card_counting_strategy().get_betting_high()
					# Apply the increment
					current_bet = self.get_starting_bet() + increment
					count_stats = count_stats + ", Increment: " + str(increment)
			self.log.fine(count_stats)
		if current_bet > self.get_bankroll():
			current_bet = self.get_bankroll()
		self.set_current_bet(current_bet)
		self.log.fine("   Starting hand #" + str(self.hand_number) + ", bet: $" + str(self.get_current_bet()) + " ...")
		
	def end_hand(self, results):
		for result in results:
			self.log.fine("   ... Finished hand #" + str(self.hand_number) + ", result: " + self.get_result_text(result) + ", bankroll: $" + str(self.get_bankroll()))
		
	def run(self):
		# Start games
		for game_number in range(self.number_of_games):
			self.log.fine("Starting game #" + str(game_number + 1) + " ...")
			
			# If we're counting cards, reset count and multiplier
			if self.get_card_counting_strategy() != None:
				self.get_card_counting_strategy().reset_count()
				
			# Reset other variables	
			self.bankroll = self.starting_bankroll
			self.set_current_bet(self.get_starting_bet())
			
			# Play the hands
			for hand_number in range(self.number_of_hands):
				self.hand_number = hand_number + 1
				if self.get_current_bet() <= self.bankroll:
					result = self.play_hand()
					self.set_current_bet(self.get_starting_bet())
					#if self.betting_strategy == self.FIVE_FOLD_BETTING_STRATEGY and result > 0:
					#	self.set_current_bet(self.get_starting_bet() * 5)
				else:
					self.log.fine("   Almost out of money, bankroll: $" + str(self.get_bankroll()))				
					break
			self.log.fine("... Finished game #" + str(game_number + 1) + ", bankroll: $" + str(self.get_bankroll()))
			ending_bankroll = self.get_bankroll();
			self.ending_bankrolls.append(ending_bankroll)
			if self.min_ending_bankroll == -1 or ending_bankroll < self.min_ending_bankroll:
				self.min_ending_bankroll = ending_bankroll
			if self.max_ending_bankroll == -1 or ending_bankroll > self.max_ending_bankroll:
				self.max_ending_bankroll = ending_bankroll
		
		# Log variables
		self.log.info("Number of games: " + str(self.number_of_games))
		self.log.info("Number of hands: " + str(self.number_of_hands))
		self.log.info("Starting bankroll: " + str(self.starting_bankroll))
		self.log.info("Starting bet: " + str(self.starting_bet))
		self.log.info("Rules: " + str(self.rules_name))
		self.log.info("Strategy file: " + str(self.strategy_file))
		self.log.info("Card counting strategy: " + str(self.card_counting_strategy.get_section()))
		self.log.info("Average ending bankroll: $" + str(sum(self.ending_bankrolls) / len(self.ending_bankrolls)))
		self.log.info("Minimum ending bankroll: $" + str(self.min_ending_bankroll))
		self.log.info("Maximum ending bankroll: $" + str(self.max_ending_bankroll))
		
		# Print results
		print("Average ending bankroll: $" + str(sum(self.ending_bankrolls) / len(self.ending_bankrolls)))
		print("Minimum ending bankroll: $" + str(self.min_ending_bankroll))
		print("Maximum ending bankroll: $" + str(self.max_ending_bankroll))
