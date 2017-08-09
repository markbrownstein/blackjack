import csv
from logging import *
from blackjack_rules import BlackjackRules
from blackjack_game import BlackjackGame

class BlackjackAutoGame:
	STANDARD_STRATEGY = "standard_strategy"
	
	STANDARD_BETTING_STRATEGY = "standard_betting_strategy"
	FIVE_FOLD_BETTING_STRATEGY = "five_fold_betting_strategy"
	
	def __init__(self, log):
		self.log = log
		self.number_of_games = 1000
		self.number_of_hands = 100
		self.starting_bankroll = 500
		self.starting_bet = 1
		self.strategy_filenames = { }
		self.strategy_filenames[self.STANDARD_STRATEGY] = "standard_strategy.csv"
		self.strategies = { }
		self.betting_strategy = self.STANDARD_BETTING_STRATEGY
		self.ending_bankrolls = []
		
	def load_strategy(self, filename):
		strategy = {}
		with open(filename, newline='') as file:
			reader = csv.reader(file, delimiter='\t')
			for row in reader:
				if row[0].isdigit() and len(row) == 11:
					key = int(row[0])
					value = []
					for i in range(10):
						if row[i + 1] == '1':
							value.append(True)
						else:
							value.append(False)
					strategy[key] = value
		return strategy
	
	def run_hand(self, game, strategy, bet, hand_number):
		self.log.info("   Starting hand #" + str(hand_number) + ", bet: $" + str(bet) + " ...")
		game.deal_hand(bet)
		dealer_up_rank = game.calc_rank(game.get_dealer_hand()[0])
		player_total = game.calc_highest_total(game.get_player_hand())
		self.log.info("      Dealer up card: " + str(dealer_up_rank) + ", Player total: " + str(player_total))	
		if game.is_hand_over() == False:
			while True:
				hit = False
				if player_total < 12:
					hit = True
				else:
					hit = strategy[player_total][dealer_up_rank - 1]
				if hit == True:
					game.deal_card_to_player()
					player_total = game.calc_highest_total(game.get_player_hand())
					self.log.info("      Dealer up card: " + str(dealer_up_rank) + ", Player total: " + str(player_total))
				else:
					break
				if game.is_hand_over() == True:
					break
			while True:
				dealer_total = game.calc_highest_total(game.get_dealer_hand())
				self.log.info("      Dealer total: " + str(dealer_total) + ", Player total: " + str(player_total))
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
		self.log.info("   ... Finished hand #" + str(hand_number) + ", reseult: " + result_text + ", bankroll: $" + str(game.get_bankroll()))
		return result

	def run_game(self, strategy, game_number):
		self.log.info("Starting game #" + str(game_number) + " ...")
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
				self.log.info("   Almost out of money, bankroll: $" + str(game.get_bankroll()))				
				break
		self.log.info("... Finished game #" + str(game_number) + ", bankroll: $" + str(game.get_bankroll()))
		self.ending_bankrolls.append(game.get_bankroll())

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
			
		# Print results
		print("Average ending bankroll: $" + str(sum(self.ending_bankrolls) / len(self.ending_bankrolls)))