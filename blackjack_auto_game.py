from common_logging import *
from configuration import Configuration
from card_counting import CardCounting

from blackjack_game_framework import BlackjackGameFramework

class BlackjackAutoGame(BlackjackGameFramework):
	STANDARD_STRATEGY = "standard_strategy"
	
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
				self.log.fine("      Dealer total: " + str(self.calc_highest_total(self.get_dealer_hand())) + ", Player total: " + player_total_string)
			else:
				self.log.fine("      Dealer up card: " + str(self.calc_rank(self.get_dealer_hand()[1])) + ", Player total: " + player_total_string)
	
	def decide_hand(self, choices):
		return self.advise_hand(self.strategy, choices)

	def start_hand(self):
		self.log.fine("   Starting hand #" + str(self.hand_number) + ", bet: $" + str(self.get_current_bet()) + " ...")
		
	def end_hand(self, results):
		for result in results:
			self.log.fine("   ... Finished hand #" + str(self.hand_number) + ", result: " + self.get_result_text(result) + ", bankroll: $" + str(self.get_bankroll()))
		
	def run(self):
		# Start games
		for game_number in range(self.number_of_games):
			self.log.fine("Starting game #" + str(game_number + 1) + " ...")
			self.bankroll = self.starting_bankroll
			self.set_current_bet(self.get_starting_bet())
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
		
		# Print results
		print("Average ending bankroll: $" + str(sum(self.ending_bankrolls) / len(self.ending_bankrolls)))
		print("Minimum ending bankroll: $" + str(self.min_ending_bankroll))
		print("Maximum ending bankroll: $" + str(self.max_ending_bankroll))
