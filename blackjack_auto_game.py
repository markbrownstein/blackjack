import csv

from logging import *
from configuration import Configuration

from blackjack_game_framework import BlackjackGameFramework

class BlackjackAutoGame(BlackjackGameFramework):
	AUTO_DOUBLE = 2
	AUTO_HIT = 1
	AUTO_STAND = 0
	AUTO_SURRENDER = -1
	AUTO_SPLIT = 1
	
	STANDARD_STRATEGY = "standard_strategy"
	
	STANDARD_BETTING_STRATEGY = "standard_betting_strategy"
	FIVE_FOLD_BETTING_STRATEGY = "five_fold_betting_strategy"
	
	def __init__(self, log, auto_section = "DEFAULT"):
		# Initialize log
		self.log = log
		
		# Initialize and read INI file
		configuration = Configuration(log, "auto.ini", auto_section)
		self.number_of_games = configuration.readInt("NumberOfGames", 1000)
		self.number_of_hands = configuration.readInt("NumberOfHands", 100)
		self.starting_bankroll = configuration.readInt("StartingBankroll", 500)
		self.starting_bet = configuration.readInt("StartingBet", 1)
		self.rules = configuration.readString("BlackJackRules", "DEFAULT")
		self.strategy_file = configuration.readString("StrategyFile", "standard_strategy.csv")
		self.betting_strategy = configuration.readString("BettingStrategy", self.STANDARD_BETTING_STRATEGY)
		
		# Stats
		self.ending_bankrolls = []
		self.max_ending_bankroll = -1
		self.min_ending_bankroll = -1
		
		# Initialize variables
		self.hand_number = 0

		# Initialize strategies
		self.strategy_filenames = { }
		self.strategy_filenames[self.STANDARD_STRATEGY] = "standard_strategy.csv"
		self.strategies = { }

		# Load strategies
		for strategy_name in self.strategy_filenames.keys():
			filename = self.strategy_filenames[strategy_name]
			strategy = self.load_strategy(filename)
			self.strategies[strategy_name] = strategy				
		self.strategy = self.strategies[self.STANDARD_STRATEGY]

		# Initialize framework
		BlackjackGameFramework.__init__(self, log, self.starting_bankroll, self.starting_bet)

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
	
	def decide_insurance(self):
		return self.NO
		
	def decide_surrender(self):
		return self.NO
		
	def decide_hand(self, choices):
		dealer_up_rank = self.calc_rank(self.get_dealer_hand()[1])
		if self.get_player_hand()[0][0] == self.get_player_hand()[1][0] and self.SPLIT in choices:
			player_rank = self.calc_rank(self.get_player_hand()[0])
			self.log.finest("Possible auto split: player rank=" + str(player_rank) + ", dealer up rank=" + str(dealer_up_rank))
			action = self.strategy[200 + player_rank][dealer_up_rank - 1]
			if action == self.AUTO_SPLIT:
				return self.SPLIT
		player_total = self.calc_highest_total(self.get_player_hand())
		if player_total < 21:
			if player_total != self.calc_lowest_total(self.get_player_hand()):
				action = self.strategy[100 + player_total][dealer_up_rank - 1]
			else:
				if player_total < 9:
					action = self.AUTO_HIT
				else:
					action = self.strategy[player_total][dealer_up_rank - 1]
					self.log.finest("Strategy action=" + str(action))
			if action > self.AUTO_STAND:
				if action > self.AUTO_HIT and self.DOUBLE in choices:
					return self.DOUBLE
				return self.HIT
			elif action == self.AUTO_SURRENDER:
				if self.SURRENDER in choices:
					return self.SURRENDER
				return self.HIT
		return self.STAND

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
					if self.betting_strategy == self.FIVE_FOLD_BETTING_STRATEGY and result > 0:
						self.set_current_bet(self.get_starting_bet() * 5)
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
		self.log.info("Rules: " + str(self.rules))
		self.log.info("Strategy file: " + str(self.strategy_file))
		self.log.info("Betting strategy: " + str(self.betting_strategy))
		
		# Print results
		print("Average ending bankroll: $" + str(sum(self.ending_bankrolls) / len(self.ending_bankrolls)))
		print("Minimum ending bankroll: $" + str(self.min_ending_bankroll))
		print("Maximum ending bankroll: $" + str(self.max_ending_bankroll))
