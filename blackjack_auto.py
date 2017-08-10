import csv
from logging import *
from blackjack_rules import BlackjackRules
from blackjack_game import BlackjackGame
from configuration import Configuration

class BlackjackAuto(Configuration):
	STANDARD_STRATEGY = "standard_strategy"
	
	STANDARD_BETTING_STRATEGY = "standard_betting_strategy"
	FIVE_FOLD_BETTING_STRATEGY = "five_fold_betting_strategy"
	
	def __init__(self, log, section = "DEFAULT"):
		self.log = log

		# Initialize and read INI file
		Configuration.__init__(self, log, "auto.ini", section)

		# Read from INI file
		self.number_of_games = Configuration.readInt(self, "NumberOfGames", 1000)
		self.number_of_hands = Configuration.readInt(self, "NumberOfHands", 100)
		self.starting_bankroll = Configuration.readInt(self, "StartingBankroll", 500)
		self.starting_bet = Configuration.readInt(self, "StartingBet", 1)
		self.rules = Configuration.readString(self, "BlackJackRules", "DEFAULT")
		self.strategy_file = Configuration.readString(self, "StrategyFile", "standard_strategy.csv")
		self.betting_strategy = Configuration.readString(self, "BettingStrategy", self.STANDARD_BETTING_STRATEGY)

		# Initialize strategies
		self.strategy_filenames = { }
		self.strategy_filenames[self.STANDARD_STRATEGY] = "standard_strategy.csv"
		self.strategies = { }
		
		# Stats
		self.ending_bankrolls = []
		self.max_ending_bankroll = -1
		self.min_ending_bankroll = -1
		
	def load_strategy(self, filename):
		strategy = {}
		with open(filename, newline='') as file:
			reader = csv.reader(file, delimiter='\t')
			for row in reader:
				if row[0].isdigit() and len(row) == 11:
					key = int(row[0])
					value = []
					for i in range(10):
						if row[i + 1].isdigit():
							value.append(int(row[i + 1]))
						else:
							value.append(0)
					strategy[key] = value
		return strategy
	
	def run_hand(self, game, strategy, bet, hand_number):
		self.log.fine("   Starting hand #" + str(hand_number) + ", bet: $" + str(bet) + " ...")
		game.deal_hand(bet)
		dealer_up_rank = game.calc_rank(game.get_dealer_hand()[0])
		player_total = game.calc_highest_total(game.get_player_hand())
		self.log.fine("      Dealer up card: " + str(dealer_up_rank) + ", Player total: " + str(player_total))	
		if game.is_hand_over() == False:
			while True:
				hit = False
				double = False
				player_soft_total = game.calc_lowest_total(game.get_player_hand())
				if player_total != player_soft_total:
					action = strategy[100 + player_total][dealer_up_rank - 1]
				else:
					if player_total < 9:
						action = 1
					else:
						action = strategy[player_total][dealer_up_rank - 1]
				if action > 0:
					hit = True
					if action > 1 and game.can_double_down(game.get_player_hand(), bet):
						bet = bet * 2
						double = True
				if hit == True:
					game.deal_card_to_player()
					player_total = game.calc_highest_total(game.get_player_hand())
					self.log.fine("      Dealer up card: " + str(dealer_up_rank) + ", Player total: " + str(player_total))
					if double == True:
						break
				else:
					break
				if game.is_hand_over() == True:
					break
			while True:
				dealer_total = game.calc_highest_total(game.get_dealer_hand())
				self.log.fine("      Dealer total: " + str(dealer_total) + ", Player total: " + str(player_total))
				if game.is_hand_over(True):
					break
				game.deal_card_to_dealer()
		result = game.finish_hand(bet)
		if result == 2:
			result_text = "Blackjack! Player WINS!"
		elif result == 1:
			result_text = "Player WINS!"
		elif result == 0:
			result_text = "PUSH!"
		elif result == -1:
			result_text = "Player LOSES!"
		self.log.fine("   ... Finished hand #" + str(hand_number) + ", reseult: " + result_text + ", bankroll: $" + str(game.get_bankroll()))
		return result

	def run_game(self, strategy, game_number):
		self.log.fine("Starting game #" + str(game_number) + " ...")
		game = BlackjackGame(self.log, self.starting_bankroll)
		bet = self.starting_bet
		for hand_number in range(self.number_of_hands):
			if bet <= self.starting_bankroll:
				result = self.run_hand(game, strategy, bet, hand_number + 1)
				if self.betting_strategy == self.FIVE_FOLD_BETTING_STRATEGY:
					if result > 0:
						bet = self.starting_bet * 5
					else:
						bet = self.starting_bet
			else:
				self.log.fine("   Almost out of money, bankroll: $" + str(game.get_bankroll()))				
				break
		self.log.fine("... Finished game #" + str(game_number) + ", bankroll: $" + str(game.get_bankroll()))
		ending_bankroll = game.get_bankroll();
		self.ending_bankrolls.append(ending_bankroll)
		if self.min_ending_bankroll == -1 or ending_bankroll < self.min_ending_bankroll:
			self.min_ending_bankroll = ending_bankroll
		if self.max_ending_bankroll == -1 or ending_bankroll > self.max_ending_bankroll:
			self.max_ending_bankroll = ending_bankroll

	def run(self):
		# Load strategies
		for strategy_name in self.strategy_filenames.keys():
			filename = self.strategy_filenames[strategy_name]
			strategy = self.load_strategy(filename)
			self.strategies[strategy_name] = strategy
					
		self.strategy = self.strategies[self.STANDARD_STRATEGY]

		# Start games
		for game_number in range(self.number_of_games):
			self.run_game(self.strategy, game_number + 1)
		
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
		